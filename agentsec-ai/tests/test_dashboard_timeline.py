from fastapi.testclient import TestClient

from backend.main import create_app


def test_dashboard_timeline_endpoint_returns_recent_activity() -> None:
    client = TestClient(create_app())

    response = client.get("/api/dashboard/timeline")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["event_type"] in {"scan_started", "scan_completed", "finding_created"}
    assert payload[0]["message"]
