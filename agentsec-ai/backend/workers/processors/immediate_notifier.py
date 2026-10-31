from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

import httpx



class ImmediateNotifier:
    """Send immediate alerts for critical findings while avoiding spam."""

    def __init__(self) -> None:
        self._sent_cache: dict[str, str] = {}

    def notify_critical(self, scan_id: str, findings: list[Any], target: str) -> None:
        if not findings:
            return
        for finding in findings[:5]:
            key = f"agentsec:notified:{scan_id}:{hashlib.md5((finding.title + str(getattr(finding, 'affected_url', ''))).encode()).hexdigest()}"
            if key in self._sent_cache:
                continue
            self._sent_cache[key] = str(datetime.utcnow().timestamp())
            self._send_slack([finding], target, scan_id)
            break

    def _send_slack(self, findings: list[Any], target: str, scan_id: str) -> None:
        webhook_url = "https://hooks.slack.com/services/test"
        payload = {
            "text": "🚨 CRITICAL FINDING — AgentSec AI",
            "attachments": [{
                "color": "#FF0000",
                "title": f"Target: {target}",
                "fields": [
                    {"title": "Scan ID", "value": scan_id, "short": True},
                    {"title": "Critical Findings", "value": str(len(findings)), "short": True},
                    *[
                        {"title": item.title, "value": f"Severity: {item.severity}\nURL: {getattr(item, 'affected_url', 'N/A')}", "short": False}
                        for item in findings[:5]
                    ],
                ],
                "footer": "AgentSec AI — Autonomous Pentesting Platform",
                "ts": str(int(datetime.utcnow().timestamp())),
            }],
        }
        try:
            import asyncio
            asyncio.run(httpx.AsyncClient().post(webhook_url, json=payload, timeout=10))
        except Exception:
            pass


__all__ = ["ImmediateNotifier"]
