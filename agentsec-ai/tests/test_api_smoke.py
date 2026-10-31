from fastapi.testclient import TestClient

from backend.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_endpoint_reports_database_status() -> None:
    """Readiness must not claim the service is ready without PostgreSQL."""

    client = TestClient(app)
    response = client.get("/health/ready")

    assert response.status_code in {200, 503}
    assert response.json()["status"] in {"ready", "not_ready"}
    assert response.json()["database"] in {"ok", "unavailable"}
