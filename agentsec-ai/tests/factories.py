"""Small dependency-free factories for store-backed and unit tests."""

from __future__ import annotations

from itertools import count
from uuid import uuid4

_ids = count(1)


def scan_payload(target: str = "example.com", **overrides: object) -> dict:
    """Build a scan payload using the public API contract."""

    payload = {
        "name": f"Test scan {next(_ids)}",
        "target": target,
        "status": "queued",
        "id": uuid4().hex,
    }
    payload.update(overrides)
    return payload


def finding_payload(title: str = "Missing security headers", **overrides: object) -> dict:
    """Build a finding payload using the public API contract."""

    payload = {
        "id": uuid4().hex,
        "title": title,
        "severity": "medium",
        "status": "open",
    }
    payload.update(overrides)
    return payload