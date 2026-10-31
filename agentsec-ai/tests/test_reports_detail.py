from fastapi.testclient import TestClient

from backend.api import reports
from backend.main import create_app
from backend.storage import FindingsStore, ScanStore
from backend.workflow_store import WorkflowStore


def test_report_detail_contains_scan_scoped_worker_commands_and_findings(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("backend.config.settings.settings.storage_backend", "json")
    scans = ScanStore(tmp_path / "scans.json")
    scan = scans.create_record("Scoped report", "example.com", "completed")
    workflows = WorkflowStore(tmp_path / "workflows.json")
    workflows.upsert_workflow(
        scan["id"],
        {
            "target": "example.com",
            "status": "completed",
            "steps": [{"name": "workers.recon.run", "status": "completed"}],
        },
    )
    workflows.update_task(
        scan["id"],
        "workers.recon.run",
        "task-actual-17",
        "completed",
        {
            "tools": [
                {
                    "plugin": "amass",
                    "command_executed": "amass enum -passive -d example.com",
                    "parsed": [{"subdomain": "www.example.com"}],
                }
            ]
        },
    )
    findings = FindingsStore(tmp_path / "findings.json")
    findings.create_record(
        "Unexpected test finding",
        "high",
        scan_id=scan["id"],
        task_id="task-actual-17",
        affected_url="https://www.example.com",
        description="Returned by the real worker.",
        evidence={"source": "worker"},
    )
    monkeypatch.setattr(reports, "_scan_store", scans)
    monkeypatch.setattr(reports, "_workflow_store", workflows)
    monkeypatch.setattr(reports, "_findings_store", findings)

    with TestClient(create_app()) as client:
        response = client.get(f"/api/reports/{scan['id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scan_id"] == scan["id"]
    assert payload["steps"][0]["commands"] == ["amass enum -passive -d example.com"]
    assert payload["steps"][0]["result"]["tools"][0]["parsed"][0]["subdomain"] == "www.example.com"
    assert payload["findings"][0]["title"] == "Unexpected test finding"
