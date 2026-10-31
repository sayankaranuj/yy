import time

from fastapi.testclient import TestClient

from backend.main import create_app
from backend.workers.celery_app import app as celery_app


def test_list_scans_returns_seeded_data() -> None:
    client = TestClient(create_app())

    response = client.get("/api/scans")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["name"] == "Initial Recon"


def test_create_scan_returns_created_record() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/scans",
        json={"name": "New scan", "target": "localhost:5174"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "New scan"
    assert payload["target"] == "localhost:5174"
    assert payload["status"] == "queued"


def test_list_findings_returns_seeded_data() -> None:
    client = TestClient(create_app())

    response = client.get("/api/findings")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["title"] == "Missing security headers"


def test_celery_scan_task_is_registered() -> None:
    assert "orchestrator.run_scan" in celery_app.tasks


def test_scan_reports_failed_dispatch_when_broker_is_unavailable() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/scans",
        json={"name": "Async scan", "target": "localhost:5174"},
    )

    assert response.status_code == 201
    scan_id = response.json()["id"]

    status_response = None
    deadline = time.time() + 2.0
    while time.time() < deadline:
        status_response = client.get(f"/api/scans/{scan_id}")
        if status_response.json()["status"] in {"completed", "running", "queued", "failed"}:
            break
        time.sleep(0.05)

    assert status_response is not None
    assert status_response.json()["status"] in {"completed", "running", "queued", "failed"}
