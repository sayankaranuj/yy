"""Validation logic adapted from claude-bug-bounty for unit tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ValidationResult:
    finding: Dict[str, Any]
    is_valid: bool
    confidence: float
    false_positive_reason: str | None
    validation_notes: str


class VulnValidator:
    async def validate_all(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen = set()
        for f in findings:
            key = (f.get("title"), f.get("affected_url"))
            if key in seen:
                continue
            seen.add(key)
            vr = await self.validate_single(f)
            if vr.is_valid:
                # attach confidence into finding dict for processor
                f["_confidence"] = vr.confidence
                results.append(f)
        return results

    async def validate_single(self, finding: Dict[str, Any]) -> ValidationResult:
        # simplistic gates
        has_request = bool(finding.get("evidence"))
        reproducible = 0.3 if has_request else 0.0
        impact = {"CRITICAL": 1.0, "HIGH": 0.8, "MEDIUM": 0.6, "LOW": 0.4, "INFO": 0.2}.get(
            finding.get("severity", "INFO"), 0.2
        )
        evidence_quality = 0.5 if len(str(finding.get("evidence", ""))) > 10 else 0.2
        fp_score = 1.0
        if finding.get("title", "").lower().startswith("nuclei") and finding.get("severity") == "INFO":
            fp_score = 0.3

        confidence = min(1.0, (reproducible + impact + evidence_quality + fp_score) / 4.0)
        is_valid = confidence > 0.4
        reason = None if is_valid else "low_confidence"
        notes = "validated by simple gates"
        return ValidationResult(finding=finding, is_valid=is_valid, confidence=confidence, false_positive_reason=reason, validation_notes=notes)
