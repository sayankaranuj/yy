"""Shared API schemas and the authoritative attack catalog."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


ATTACK_CATALOG: dict[str, dict[str, Any]] = {
    "recon": {
        "label": "Reconnaissance",
        "items": {
            "recon.subdomain_enum": "Subdomain Enumeration",
            "recon.dns_enum": "DNS Record Enumeration",
            "recon.whois": "WHOIS Lookup",
            "recon.asn": "ASN & IP Range Discovery",
            "recon.cert_transparency": "Certificate Transparency Mining",
            "recon.osint": "AI OSINT",
        },
    },
    "enum": {
        "label": "Enumeration",
        "items": {
            "enum.port_scan": "Port Scanning",
            "enum.live_hosts": "Live Host Detection",
            "enum.tech_fingerprint": "Technology Fingerprinting",
            "enum.crawling": "Web Crawling",
            "enum.directory_bruteforce": "Directory Brute-forcing",
            "enum.js_discovery": "JavaScript File Discovery",
        },
    },
    "vuln": {
        "label": "Vulnerability Testing",
        "items": {
            "vuln.nuclei_scan": "Nuclei Template Scan",
            "vuln.sqli": "SQL Injection",
            "vuln.xss": "Cross-Site Scripting",
            "vuln.ssrf": "SSRF",
            "vuln.lfi_rfi": "LFI / RFI",
            "vuln.ssti": "Server-Side Template Injection",
            "vuln.cmdi": "Command Injection",
            "vuln.cors": "CORS Misconfiguration",
            "vuln.idor": "IDOR / Broken Access Control",
            "vuln.graphql": "GraphQL Security Testing",
            "vuln.cms": "CMS-Specific Testing",
        },
    },
    "auth": {
        "label": "Authentication & Authorization",
        "items": {
            "auth.session": "Session Cookie Security",
            "auth.oauth": "OAuth Flow Testing",
            "auth.rate_limit": "Rate Limit Testing",
        },
    },
    "secrets": {
        "label": "Secret & Cloud",
        "items": {
            "secrets.js_extraction": "JS Secret Extraction",
            "secrets.git_scan": "Git Repository Scanning",
            "secrets.file_scan": "Config/Backup File Scanning",
            "secrets.cloud_buckets": "Cloud Bucket Exposure",
        },
    },
    "exploit": {
        "label": "Exploitation (Gated)",
        "items": {
            "exploit.poc_generation": "Proof-of-Concept Generation",
        },
    },
}


class AttackCatalogResponse(BaseModel):
    """Return the catalog in the same shape used by the selector UI."""

    catalog: dict[str, dict[str, Any]]


def valid_attack_categories() -> set[str]:
    """Return all selectable leaf category keys."""

    return {
        key
        for group in ATTACK_CATALOG.values()
        for key in group["items"]
    }
