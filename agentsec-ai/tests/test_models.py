"""Phase 14 model contract tests for the current SQLAlchemy models."""

import pytest

from backend.models.finding import Finding, FindingStatus
from backend.models.scan import Scan, ScanMode, ScanStatus, ScanType


@pytest.mark.unit
def test_scan_defaults_and_enums() -> None:
    """Scan exposes the lifecycle and scan-mode enums used by the API."""

    scan = Scan(target="example.com", scan_type=ScanType.FULL)
    assert scan.status is None or scan.status == ScanStatus.PENDING
    assert scan.scan_mode is None or scan.scan_mode == ScanMode.CLASSIC
    assert {item.value for item in ScanStatus} == {
        "PENDING", "RUNNING", "PAUSED", "COMPLETED", "FAILED", "CANCELLED"
    }
    assert {item.value for item in ScanMode} == {"CLASSIC", "HYBRID", "AUTONOMOUS"}


@pytest.mark.unit
def test_finding_defaults_and_status_values() -> None:
    """Finding defaults preserve the initial review state."""

    finding = Finding(title="Test", scan_id="00000000-0000-0000-0000-000000000001")
    assert finding.severity == "INFO"
    assert finding.status is None or finding.status == FindingStatus.NEW
    assert {item.value for item in FindingStatus} >= {"NEW", "CONFIRMED", "FALSE_POSITIVE"}