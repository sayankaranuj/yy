from datetime import datetime, timezone

from backend.api.findings import FindingRecord, FindingUpdate
from backend.repositories import ActiveApiRepository


def test_finding_dedup_key_normalizes_scanner_variation():
    first = ActiveApiRepository.finding_dedup_key(
        title="  SQL   Injection ", source_tool="Nuclei", category="Web", asset="HTTPS://EXAMPLE.test", parameter=" id "
    )
    second = ActiveApiRepository.finding_dedup_key(
        title="sql injection", source_tool=" nuclei ", category="web", asset="https://example.test", parameter="id"
    )
    assert first == second


def test_finding_record_exposes_quality_and_workflow_fields():
    finding = FindingRecord(
        id=1,
        title="Issue",
        confidence=0.9,
        verification_state="verified",
        due_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        risk_acceptance=True,
    )
    assert finding.confidence == 0.9
    assert finding.verification_state == "verified"
    assert finding.risk_acceptance is True


def test_finding_update_only_serializes_explicit_changes():
    update = FindingUpdate(verification_state="false_positive", analyst_notes="Reviewed")
    assert update.model_dump(exclude_unset=True) == {
        "verification_state": "false_positive",
        "analyst_notes": "Reviewed",
    }
