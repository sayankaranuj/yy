from fastapi.testclient import TestClient

from backend.main import create_app


def test_reports_endpoint_returns_generated_report() -> None:
    client = TestClient(create_app())

    response = client.get("/api/reports")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert any(item["summary"]["status"] in {"completed", "running", "queued"} for item in payload)
