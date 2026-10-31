from fastapi.testclient import TestClient

from backend.main import create_app


def test_dashboard_details_endpoint_returns_richer_overview() -> None:
    client = TestClient(create_app())

    response = client.get("/api/dashboard/details")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scan_count"] >= 1
    assert payload["finding_count"] >= 1
    assert payload["high_severity_findings"] >= 0
    assert payload["recent_scans"][0]["status"] in {"completed", "queued"}
