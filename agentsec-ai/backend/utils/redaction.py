"""Redact secret-like values before they are persisted or rendered."""

from __future__ import annotations

import re
from typing import Any

SECRET_KEY_PATTERN = re.compile(
    r"(?i)\b(aws_access_key_id|api[_-]?key|secret|password|token)\b"
    r"(\s*[:=]\s*)([A-Za-z0-9_./+=-]{8,})"
)


def redact_text(value: str) -> str:
    """Replace values assigned to common secret keys while keeping evidence useful."""

    return SECRET_KEY_PATTERN.sub(r"\1\2[REDACTED]", value)


def redact_mapping(value: Any) -> Any:
    """Recursively redact strings in JSON-compatible structures."""

    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_mapping(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_mapping(item) for key, item in value.items()}
    return value


__all__ = ["redact_mapping", "redact_text"]
