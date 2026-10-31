from pathlib import Path

from fastapi.testclient import TestClient

from backend.api import results as results_api
from backend.api import workflow as workflow_api
from backend.config.settings import settings
from backend.main import create_app
from backend.workflow_store import WorkflowStore


def test_results_endpoint_returns_only_verified_structured_worker_results(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(settings, "storage_backend", "json")
    store = WorkflowStore(tmp_path / "workflow.json")
    store.upsert_workflow(
        42,
        {
            "target": "example.org",
            "status": "running",
            "steps": [{"name": "workers.enum.run", "status": "queued"}],
        },
    )
    store.update_task(42, "workers.enum.run", "celery-task-42", "running")
    result = {
        "scan_id": 42,
        "target": "example.org",
        "tools": [{"tool": "httpx_plugin", "success": True, "results": [{"url": "https://example.org"}]}],
    }
    store.update_task(42, "workers.enum.run", "celery-task-42", "completed", result)
    monkeypatch.setattr(results_api, "_store", store)
    monkeypatch.setattr(workflow_api, "store", store)
    client = TestClient(create_app())

    response = client.get("/api/scans/42/results")

    assert response.status_code == 200
    assert response.json() == [
        {
            "scan_id": 42,
            "task_id": "celery-task-42",
            "tool_name": "workers.enum.run",
            "status": "SUCCESS",
            "payload": result,
        }
    ]

    latest_response = client.get("/api/results")
    assert latest_response.status_code == 200
    assert latest_response.json() == response.json()


def test_workflow_store_persists_tasks_and_results(tmp_path: Path) -> None:
    store = WorkflowStore(tmp_path / "workflow.json")
    workflow = {
        "target": "example.org",
        "status": "running",
        "steps": [
            {"name": "workers.recon.run", "status": "queued"},
            {"name": "workers.enum.run", "status": "queued"},
        ],
    }

    persisted = store.upsert_workflow(42, workflow)

    assert persisted["tasks"][0]["task_name"] == "workers.recon.run"
    assert persisted["results"] == []

    store.update_task(
        42,
        "workers.recon.run",
        "real-celery-task",
        "completed",
        {"discovered_count": 2, "hosts": ["a.example.org", "b.example.org"]},
    )

    latest = store.get_latest_state()
    assert latest is not None
    assert latest["tasks"][0]["task_name"] == "workers.recon.run"
    assert store.get_results(42) == [
        {
            "scan_id": 42,
            "task_id": "real-celery-task",
            "tool_name": "workers.recon.run",
            "status": "SUCCESS",
            "payload": {
                "discovered_count": 2,
                "hosts": ["a.example.org", "b.example.org"],
            },
        }
    ]


def test_new_json_workflow_store_does_not_create_sample_results(tmp_path: Path) -> None:
    path = tmp_path / "new-workflow.json"
    WorkflowStore(path)

    assert path.read_text(encoding="utf-8") == '{\n  "workflows": []\n}'


def test_results_are_rejected_when_task_or_scan_provenance_does_not_match(
    tmp_path: Path,
) -> None:
    store = WorkflowStore(tmp_path / "workflow.json")
    store.upsert_workflow(
        43,
        {
            "target": "example.org",
            "status": "running",
            "steps": [{"name": "workers.enum.run", "status": "queued"}],
        },
    )
    store.update_task(43, "workers.enum.run", "celery-task-43", "completed", {"ok": True})
    state = store.get_state(43)
    assert state is not None
    state["results"][0]["payload"] = state["results"][0]["payload"].replace(
        '"scan_id":43', '"scan_id":44'
    )
    store._write({"workflows": [state]})

    assert store.get_results(43) == []
