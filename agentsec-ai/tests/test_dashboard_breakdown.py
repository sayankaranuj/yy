from fastapi.testclient import TestClient

from backend.config.settings import settings
from backend.main import create_app
from backend.storage import FindingsStore


def test_dashboard_breakdown_endpoint_returns_severity_summary() -> None:
    client = TestClient(create_app())

    response = client.get("/api/dashboard/breakdown")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_findings"] >= 1
    assert payload["severity_breakdown"]["medium"] >= 1
    assert payload["severity_breakdown"]["high"] >= 0


def test_dashboard_breakdown_reads_postgres_findings(monkeypatch) -> None:
    async def list_postgres_findings(self):
        return [
            {"id": 1, "title": "Actual critical result", "severity": "critical", "status": "open"},
            {"id": 2, "title": "Actual low result", "severity": "low", "status": "open"},
        ]

    monkeypatch.setattr(settings, "storage_backend", "postgres")
    monkeypatch.setattr(FindingsStore, "list_records_async", list_postgres_findings)
    response = TestClient(create_app()).get("/api/dashboard/breakdown")

    assert response.status_code == 200
    assert response.json() == {
        "total_findings": 2,
        "severity_breakdown": {"critical": 1, "high": 0, "medium": 0, "low": 1},
    }
