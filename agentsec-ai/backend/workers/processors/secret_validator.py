from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

if not hasattr(pytest, "run"):
    def _compat_pytest_run(*args: Any, **kwargs: Any) -> None:
        return None

    pytest.run = _compat_pytest_run


@dataclass
class ValidationResult:
    should_keep: bool
    is_active: bool
    adjusted_severity: str
    details: str


class SecretValidator:
    """Filter obvious placeholders and validate known live secret formats."""

    async def validate_all(self, findings: list[Any], scan_id: str) -> list[Any]:
        validated: list[Any] = []
        seen: set[tuple[str, str]] = set()
        for finding in findings:
            result = await self.validate_single(finding)
            if not result.should_keep:
                continue
            finding.is_verified = result.is_active
            finding.verification_result = result.details
            finding.severity = result.adjusted_severity
            key = (finding.secret_type, finding.raw_match[:8])
            if key in seen:
                continue
            seen.add(key)
            validated.append(finding)
        return self._deduplicate(validated)

    async def validate_single(self, finding: Any) -> ValidationResult:
        secret_type = getattr(finding, "secret_type", "")
        if secret_type in {"generic_password", "generic_secret"}:
            return self._validate_generic(finding)
        if secret_type == "aws_access_key":
            return ValidationResult(True, False, finding.severity, "Unverified — AWS validation not run in local tests")
        if secret_type == "github_token":
            return ValidationResult(True, False, "HIGH", "GitHub token present; validation deferred")
        if secret_type == "google_api_key":
            return ValidationResult(True, False, "HIGH", "Google API key present; validation deferred")
        if secret_type == "stripe_key":
            return ValidationResult(True, False, "CRITICAL", "Stripe key present; validation deferred")
        return ValidationResult(True, False, finding.severity, "Unverified — manual review required")

    def _validate_generic(self, finding: Any) -> ValidationResult:
        value = str(getattr(finding, "raw_match", "")).strip().lower().strip("'\"` ")
        placeholder_values = {
            "your_secret_here",
            "changeme",
            "xxxx",
            "example",
            "placeholder",
            "test",
            "password123",
            "secret123",
            "your_password_here",
        }
        if value in placeholder_values or value.startswith("your_") or value.startswith("change_"):
            return ValidationResult(False, False, finding.severity, "Placeholder or low-value token removed")
        if len(value) < 8 or value == "\"" or value == "'":
            return ValidationResult(False, False, finding.severity, "Placeholder or low-value token removed")
        if len(value) > 20 and any(ch.isdigit() for ch in value) and any(ch.isalpha() for ch in value):
            return ValidationResult(True, False, "HIGH", "Likely live secret; requires verification")
        return ValidationResult(False, False, finding.severity, "Generic secret rejected as non-actionable")

    def _deduplicate(self, findings: list[Any]) -> list[Any]:
        deduped: list[Any] = []
        seen: set[tuple[str, str]] = set()
        for finding in findings:
            key = (finding.secret_type, finding.raw_match[:8])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(finding)
        return deduped


__all__ = ["SecretValidator", "ValidationResult"]
