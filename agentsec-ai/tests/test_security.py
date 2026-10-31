"""Phase 14 security regression tests for input boundaries."""

import pytest
from fastapi.testclient import TestClient

from backend.main import create_app


@pytest.mark.security
@pytest.mark.parametrize("target", ["", "<script>alert(1)</script>", "'; DROP TABLE scans;--"])
def test_invalid_scan_payload_is_rejected(target: str) -> None:
    """The API rejects empty or obviously hostile scan payloads."""

    response = TestClient(create_app()).post(
        "/api/scans", json={"name": "security test", "target": target}
    )
    assert response.status_code in {400, 422}


@pytest.mark.security
def test_unknown_resource_does_not_disclose_data() -> None:
    """Unknown identifiers produce a generic not-found response."""

    response = TestClient(create_app()).get("/api/scans/999999999")
    assert response.status_code == 404
    assert "password" not in response.text.lower()