"""OWASP mapping helper for findings (simple rule-based)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OWASPMapping:
    owasp_category: str
    owasp_name: str
    cwe_id: str | None = None
    mitre_technique: str | None = None


class OWASPMapper:
    def map(self, finding: Dict[str, Any]) -> OWASPMapping:
        title = finding.get("title", "").lower()
        if "sql" in title:
            return OWASPMapping("A05:2025", "SQL Injection", "CWE-89", "T1190")
        if "xss" in title:
            return OWASPMapping("A05:2025", "Cross-Site Scripting", "CWE-79", "T1059.007")
        if "ssrf" in title:
            return OWASPMapping("A01:2025", "SSRF", "CWE-918", "T1090")
        if "auth" in title or "authz" in title:
            return OWASPMapping("A01:2025", "Broken Access Control", "CWE-639", "T1078")
        return OWASPMapping("A02:2025", "Security Misconfiguration", None, None)


owasp_mapper = OWASPMapper()
"""Map severity values to OWASP-style tags for report generation."""


def map_severity_to_owasp(severity: str) -> str:
    """Translate a simple severity label into an OWASP-style tag."""

    normalized = (severity or "info").lower()
    mapping = {
        "critical": "A01:2021-Broken Access Control",
        "high": "A03:2021-Injection",
        "medium": "A05:2021-Security Misconfiguration",
        "low": "A09:2021-Security Logging and Monitoring Failures",
    }
    return mapping.get(normalized, "A09:2021-Security Logging and Monitoring Failures")
