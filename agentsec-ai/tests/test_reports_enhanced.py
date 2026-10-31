from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import create_app
from backend.reports.report_builder import build_report_artifacts


def test_reports_endpoint_returns_richer_summary_payload() -> None:
    client = TestClient(create_app())

    response = client.get("/api/reports")

    assert response.status_code == 200
    payload = response.json()
    summary = payload[0]["summary"]
    assert summary["steps"] >= 0
    assert summary["findings_count"] >= 0
    assert summary["target"]


def test_reports_endpoint_includes_artifact_exports() -> None:
    client = TestClient(create_app())

    response = client.get("/api/reports")

    assert response.status_code == 200
    payload = response.json()
    summary = payload[0]["summary"]
    artifacts = summary["artifacts"]
    assert isinstance(artifacts, list)
    assert any(item["format"] == "markdown" for item in artifacts)
    assert any(item["format"] == "json" for item in artifacts)


def test_build_report_artifacts_returns_markdown_and_json() -> None:
    artifacts = build_report_artifacts(target="example.com")

    assert isinstance(artifacts, list)
    assert any(artifact["format"] == "markdown" for artifact in artifacts)
    assert any(artifact["format"] == "json" for artifact in artifacts)


def test_build_report_artifacts_sanitizes_url_for_windows_filenames() -> None:
    """Ensure URL targets with Windows-reserved filename characters still export."""

    artifacts = build_report_artifacts(target="http://localhost:5173/scans/67?tab=report")

    assert len(artifacts) == 2
    assert all(
        not any(character in artifact["name"] for character in '<>:"/\\|?*')
        for artifact in artifacts
    )
    assert all(Path(artifact["path"]).is_file() for artifact in artifacts)
