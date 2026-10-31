"""Cached, attributed public payload and wordlist samples."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import logging
import random
from datetime import datetime, timezone

import httpx

logger = logging.getLogger(__name__)


@dataclass
class PayloadSource:
    """Metadata for a public source used for security-testing samples."""

    name: str
    repo_url: str
    raw_file_url: str
    category: str
    license: str
    cached_at: str | None = None
    entry_count: int = 0


class PayloadIntelService:
    """Fetch and cache small, attributed samples from public repositories."""

    SOURCES = [
        PayloadSource(
            "SecLists - Top Common Passwords",
            "https://github.com/danielmiessler/SecLists",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt",
            "credentials",
            "MIT",
        ),
        PayloadSource(
            "PayloadsAllTheThings - SQL Injection",
            "https://github.com/swisskyrepo/PayloadsAllTheThings",
            "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder/exploit/Generic_SQLI.txt",
            "sqli",
            "MIT",
        ),
        PayloadSource(
            "PayloadsAllTheThings - XSS Polyglots",
            "https://github.com/swisskyrepo/PayloadsAllTheThings",
            "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/Intruders/XSS_Polyglots.txt",
            "xss",
            "MIT",
        ),
        PayloadSource(
            "SecLists - Subdomains",
            "https://github.com/danielmiessler/SecLists",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
            "subdomains",
            "MIT",
        ),
    ]

    _cache: dict[str, tuple[PayloadSource, list[str]]] = {}

    async def fetch_and_cache(self, source: PayloadSource) -> list[str]:
        """Fetch one source with a bounded timeout and safe fallback."""

        cached = self._cache.get(source.category)
        if cached:
            return cached[1]
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(
                    source.raw_file_url,
                    headers={"User-Agent": "AgentSec-AI-Intel/1.0"},
                )
                response.raise_for_status()
                lines = [
                    line.strip()
                    for line in response.text.splitlines()[:2000]
                    if line.strip() and not line.startswith("#")
                ]
        except (httpx.HTTPError, OSError) as exc:
            logger.warning("Unable to fetch payload source %s: %s", source.name, exc)
            lines = self._fallback(source.category)
        source.cached_at = datetime.now(timezone.utc).isoformat()
        source.entry_count = len(lines)
        self._cache[source.category] = (source, lines)
        return lines

    async def sample(self, category: str, count: int) -> tuple[PayloadSource, list[str]]:
        """Return a bounded random sample and its attribution metadata."""

        source = next((item for item in self.SOURCES if item.category == category), None)
        if source is None:
            raise KeyError(category)
        values = await self.fetch_and_cache(source)
        return source, random.sample(values, min(count, len(values)))

    def sources(self) -> list[dict[str, object]]:
        """Return source metadata without triggering network access."""

        return [asdict(source) for source in self.SOURCES]

    @staticmethod
    def _fallback(category: str) -> list[str]:
        """Return safe representative values when the public source is offline."""

        return {
            "credentials": ["admin", "password", "welcome", "letmein"],
            "sqli": ["' OR '1'='1", "1' AND 1=1--", "') OR ('1'='1"],
            "xss": ["<script>alert(1)</script>", "\"><svg/onload=alert(1)>"],
            "subdomains": ["www", "api", "dev", "staging"],
        }.get(category, [])


payload_intel = PayloadIntelService()
