from fastapi.testclient import TestClient

from backend.main import create_app


def test_assets_endpoint_returns_host_and_endpoint_data() -> None:
    client = TestClient(create_app())

    response = client.get("/api/assets")

    assert response.status_code == 200
    payload = response.json()
    assert payload["hosts"][0]["host"] == "example.com"
    assert payload["endpoints"][0]["path"] == "/"


def test_assets_endpoint_includes_service_and_risk_metadata() -> None:
    client = TestClient(create_app())

    response = client.get("/api/assets")

    assert response.status_code == 200
    payload = response.json()
    host = payload["hosts"][0]
    assert host["service"] == "http"
    assert host["risk"] == "medium"
