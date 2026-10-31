from backend.orchestrator import orchestrator


def test_run_scan_workflow_returns_progress_steps(monkeypatch) -> None:
    monkeypatch.setattr(orchestrator, "_broker_is_reachable", lambda: True)
    monkeypatch.setattr(orchestrator.celery_app, "send_task", lambda *args, **kwargs: "celery-task-42")
    result = orchestrator.run_scan_workflow(scan_id=42, target="example.net", persist=False)

    assert result["scan_id"] == 42
    assert result["target"] == "example.net"
    assert result["status"] == "running"
    assert result["steps"][0]["name"] == "workers.recon.run"
    assert result["steps"][-1]["name"] == "workers.report.run"
