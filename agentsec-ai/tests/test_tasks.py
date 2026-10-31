import time
from pathlib import Path

from fastapi.testclient import TestClient

from backend.api import results as results_api
from backend.api import scans as scans_api
from backend.api import tasks as tasks_api
from backend.api import workflow as workflow_api
from backend.config.settings import settings
from backend.main import create_app
from backend.workflow_store import WorkflowStore


def test_tasks_endpoint_is_empty_without_a_persisted_workflow(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(settings, "storage_backend", "json")
    monkeypatch.setattr(tasks_api, "_store", WorkflowStore(tmp_path / "tasks.json"))
    client = TestClient(create_app())

    response = client.get("/api/tasks")

    assert response.status_code == 200
    payload = response.json()
    assert payload == []


def test_scan_without_dispatched_workers_has_no_fake_results(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(settings, "storage_backend", "json")
    store = WorkflowStore(tmp_path / "workflow.json")
    monkeypatch.setattr(scans_api, "_workflow_store", store)
    monkeypatch.setattr(tasks_api, "_store", store)
    monkeypatch.setattr(results_api, "_store", store)
    monkeypatch.setattr(workflow_api, "store", store)
    client = TestClient(create_app())

    create_response = client.post(
        "/api/scans",
        json={"name": "Workflow scan", "target": "localhost:5174"},
    )

    assert create_response.status_code == 201
    scan_id = create_response.json()["id"]

    deadline = time.time() + 2.0
    workflow_response = None
    while time.time() < deadline:
        workflow_response = client.get(f"/api/scans/{scan_id}/workflow")
        if (
            workflow_response.status_code == 200
            and workflow_response.json()["status"] == "failed"
        ):
            break
        time.sleep(0.05)

    tasks_response = client.get("/api/tasks")
    results_response = client.get("/api/results")
    scan_results_response = client.get(f"/api/scans/{scan_id}/results")

    assert workflow_response is not None
    assert workflow_response.status_code == 200
    assert workflow_response.json()["status"] == "failed"
    assert tasks_response.status_code == 200
    assert results_response.status_code == 200
    assert scan_results_response.status_code == 200
    assert any(
        task["task_name"] == "workers.recon.run" and task["status"] == "failed"
        for task in tasks_response.json()
    )
    assert results_response.json() == []
    assert scan_results_response.json() == []
