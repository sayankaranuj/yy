from fastapi.testclient import TestClient

from backend.main import create_app


def test_plugins_endpoint_returns_registered_plugins() -> None:
    client = TestClient(create_app())

    response = client.get("/api/plugins")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 24
    assert {item["name"] for item in payload} >= {"amass", "dnsx", "nuclei_plugin"}
    assert all(item["enabled"] is True for item in payload)


def test_plugins_endpoint_includes_category_and_version() -> None:
    client = TestClient(create_app())

    response = client.get("/api/plugins")

    assert response.status_code == 200
    payload = response.json()
    plugin = next(item for item in payload if item["name"] == "dnsx")
    assert plugin["category"] == "recon"
    assert plugin["version"] == "1.0.0"
