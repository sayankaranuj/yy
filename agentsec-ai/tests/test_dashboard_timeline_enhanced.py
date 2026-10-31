from fastapi.testclient import TestClient

from backend.main import create_app


def test_dashboard_timeline_endpoint_returns_timestamps_and_ids() -> None:
    client = TestClient(create_app())

    response = client.get("/api/dashboard/timeline")

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["id"] >= 0
    assert payload[0]["timestamp"]
    assert payload[0]["event_type"] in {"scan_started", "scan_completed", "finding_created"}
