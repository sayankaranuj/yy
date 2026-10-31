"""Phase 14 API contract tests using the existing local store backend."""

import pytest
from fastapi.testclient import TestClient

from backend.main import create_app


@pytest.mark.api
def test_health_and_inventory_routes() -> None:
    """Health, scan, finding, and plugin routes return usable JSON."""

    client = TestClient(create_app())
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/scans").status_code == 200
    assert client.get("/api/findings").status_code == 200
    assert client.get("/api/plugins").status_code == 200


@pytest.mark.api
def test_create_scan_returns_workflow_contract() -> None:
    """Creating a scan returns an identifier and queued state."""

    response = TestClient(create_app()).post(
        "/api/scans", json={"name": "QA scan", "target": "localhost:5174"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["target"] == "localhost:5174"
    assert body["status"] == "queued"
    assert isinstance(body["id"], int)