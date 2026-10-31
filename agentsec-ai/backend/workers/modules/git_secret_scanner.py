from __future__ import annotations

import re
from typing import Any

import httpx

from backend.workers.modules.js_secret_extractor import SecretFinding


class GitSecretScanner:
    """Perform repository and git exposure checks for secret-bearing material."""

    def __init__(self, executor: Any | None = None, event_bus: Any | None = None, db: Any | None = None) -> None:
        self.executor = executor
        self.event_bus = event_bus
        self.db = db

    async def run(self, scan_id: str, repo_urls: list[str], target: str, db: Any | None = None) -> list[SecretFinding]:
        findings: list[SecretFinding] = []
        for repo_url in repo_urls:
            findings.extend(await self._scan_github_repo(repo_url, scan_id))
        findings.extend(self._scan_exposed_git(target, scan_id))
        return findings

    async def _scan_github_repo(self, repo_url: str, scan_id: str) -> list[SecretFinding]:
        findings: list[SecretFinding] = []
        if not repo_url:
            return findings
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(repo_url, follow_redirects=True)
                if resp.status_code < 400:
                    findings.append(
                        SecretFinding(
                            secret_type="github_repo",
                            title="GitHub Repository Exposed",
                            severity="MEDIUM",
                            raw_match=repo_url[:8] + "...",
                            context_snippet=repo_url,
                            source_url=repo_url,
                            line_number=None,
                            tool_found_by="git_scanner",
                        )
                    )
        except Exception:
            pass
        return findings

    def _scan_exposed_git(self, target_url: str, scan_id: str) -> list[SecretFinding]:
        findings: list[SecretFinding] = []
        try:
            check_url = target_url.rstrip("/") + "/.git/config"
            try:
                import asyncio
                result = asyncio.run(httpx.AsyncClient(timeout=15).get(check_url))
            except Exception:
                result = httpx.get(check_url, timeout=15)
            if result.status_code == 200:
                content = result.text or ""
                if re.search(r"\[remote\s+\"origin\"\]|\[core\]", content, flags=re.I):
                    findings.append(
                        SecretFinding(
                            secret_type="git_exposed",
                            title="Exposed .git Repository",
                            severity="CRITICAL",
                            raw_match="gitconfig",
                            context_snippet=content[:200],
                            source_url=check_url,
                            line_number=None,
                            tool_found_by="git_scanner",
                        )
                    )
        except Exception:
            pass
        return findings


__all__ = ["GitSecretScanner"]
