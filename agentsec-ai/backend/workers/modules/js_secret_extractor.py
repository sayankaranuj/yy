from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


PLACEHOLDERS = {
    "your_secret_here",
    "your_password_here",
    "changeme",
    "password123",
    "secret123",
    "example",
    "placeholder",
    "test",
    "todo",
    "change_this",
    "xxxx",
}


@dataclass
class SecretFinding:
    secret_type: str
    title: str
    severity: str
    raw_match: str
    context_snippet: str
    source_url: str
    line_number: int | None
    tool_found_by: str
    is_verified: bool = False
    verification_result: str | None = None


class JSSecretExtractor:
    """Extract common secret patterns from JavaScript bundles and related files."""

    SECRET_PATTERNS = {
        "aws_access_key": {
            "pattern": r"AKIA[0-9A-Z]{16}",
            "severity": "CRITICAL",
            "title": "AWS Access Key ID Exposed",
        },
        "aws_secret_key": {
            "pattern": r"[0-9a-zA-Z/+]{40}",
            "context_required": "aws_access_key nearby",
            "severity": "CRITICAL",
            "title": "AWS Secret Access Key Exposed",
        },
        "google_api_key": {
            "pattern": r"AIza[0-9A-Za-z\-_]{35}",
            "severity": "HIGH",
            "title": "Google API Key Exposed",
        },
        "firebase_url": {
            "pattern": r"https://[a-z0-9-]+\.firebaseio\.com",
            "severity": "HIGH",
            "title": "Firebase Database URL Exposed",
        },
        "jwt_token": {
            "pattern": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
            "severity": "HIGH",
            "title": "JWT Token Hardcoded",
        },
        "private_key": {
            "pattern": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
            "severity": "CRITICAL",
            "title": "Private Key Exposed",
        },
        "generic_api_key": {
            "pattern": r"(?i)(api[_-]?key|apikey|api[_-]?secret)['\"\s:=]+([A-Za-z0-9_\-]{20,})",
            "severity": "HIGH",
            "title": "Generic API Key Exposed",
        },
        "generic_password": {
            "pattern": r"(?i)(password|passwd|pwd)['\"\s:=]+([A-Za-z0-9@#$%^&*!_\-]{8,})",
            "severity": "HIGH",
            "title": "Hardcoded Password Found",
        },
        "generic_secret": {
            "pattern": r"(?i)(secret|token)['\"\s:=]+([A-Za-z0-9_\-]{20,})",
            "severity": "MEDIUM",
            "title": "Hardcoded Secret Found",
        },
        "basic_auth_url": {
            "pattern": r"https?://[^:]+:[^@]+@[^\s/]+",
            "severity": "CRITICAL",
            "title": "Credentials in URL",
        },
        "stripe_key": {
            "pattern": r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}",
            "severity": "CRITICAL",
            "title": "Stripe API Key Exposed",
        },
        "github_token": {
            "pattern": r"gh[pousr]_[A-Za-z0-9_]{36,255}",
            "severity": "CRITICAL",
            "title": "GitHub Token Exposed",
        },
    }

    async def run(self, scan_id: str, js_file_list: list[str], context: dict | None = None, db: Any | None = None) -> list[SecretFinding]:
        """Fetch JS files and detect secrets in them."""
        out: list[SecretFinding] = []
        seen_hashes: set[str] = set()
        base_dir = Path("/tmp") / f"agentsec_{scan_id}_js"
        base_dir.mkdir(parents=True, exist_ok=True)

        for index, js_url in enumerate(js_file_list):
            if not js_url:
                continue
            try:
                async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                    resp = await client.get(js_url, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code >= 400 or len(resp.text) > 5_000_000:
                    continue
            except Exception:
                continue

            content = resp.text
            digest = hashlib.md5(content.encode("utf-8")).hexdigest()
            if digest in seen_hashes:
                continue
            seen_hashes.add(digest)
            (base_dir / f"{index}.js").write_text(content, encoding="utf-8")
            out.extend(self._regex_extract(content, js_url))

        return out

    def _regex_extract(self, content: str, source_url: str) -> list[SecretFinding]:
        findings: list[SecretFinding] = []
        for key, cfg in self.SECRET_PATTERNS.items():
            pattern = cfg["pattern"]
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                raw = self._extract_match_value(match)
                if self._looks_like_placeholder(raw):
                    continue
                context_snippet = self._context_around(content, match.start(), match.end())
                findings.append(
                    SecretFinding(
                        secret_type=key,
                        title=cfg["title"],
                        severity=cfg["severity"],
                        raw_match=self._truncate(raw),
                        context_snippet=context_snippet,
                        source_url=source_url,
                        line_number=self._line_number(content, match.start()),
                        tool_found_by="regex_extractor",
                    )
                )
        seen: set[tuple[str, str]] = set()
        deduped: list[SecretFinding] = []
        for item in findings:
            key = (item.secret_type, item.raw_match[:8])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        return deduped

    @staticmethod
    def _extract_match_value(match: re.Match[str]) -> str:
        groups = [group for group in match.groups() if group is not None]
        if groups:
            value = groups[-1]
            if isinstance(value, str) and value.strip():
                return value.strip().strip("'\"` ")
        return match.group(0).strip().strip("'\"` ")

    @staticmethod
    def _line_number(content: str, pos: int) -> int | None:
        return content.count("\n", 0, pos) + 1

    @staticmethod
    def _context_around(content: str, start: int, end: int, window: int = 80) -> str:
        s = max(0, start - window)
        e = min(len(content), end + window)
        snippet = content[s:e].replace("\n", " ")
        return snippet.strip()[:180]

    @staticmethod
    def _truncate(raw: str) -> str:
        if len(raw) <= 8:
            return raw
        return f"{raw[:8]}..."

    @staticmethod
    def _looks_like_placeholder(raw: str) -> bool:
        value = raw.strip().lower().strip("'\"` ")
        if not value:
            return True
        if value in PLACEHOLDERS:
            return True
        if value.startswith("your_") or value.startswith("change_"):
            return True
        if value in {"changeme", "example", "placeholder", "todo", "xxxx"}:
            return True
        if value.startswith("example") and len(value) < 16:
            return True
        return False


__all__ = ["JSSecretExtractor", "SecretFinding"]
