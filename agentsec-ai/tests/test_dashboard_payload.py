from fastapi.testclient import TestClient

from backend.main import create_app


def test_dashboard_payload_endpoint_returns_overview() -> None:
    client = TestClient(create_app())

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scan_count"] >= 1
    assert payload["finding_count"] >= 1
    assert payload["status"] == "completed"
    assert payload["latest_target"] == "example.com"
