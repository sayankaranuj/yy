
from backend.orchestrator.orchestrator import run_scan_workflow


def test_run_scan_workflow_enqueues_expected_tasks(monkeypatch):
    called = []

    def fake_send(task_name, args=(), queue=None, **kwargs):
        called.append((task_name, args, queue, kwargs))

    monkeypatch.setattr("backend.orchestrator.orchestrator.celery_app.send_task", fake_send)

    wf = run_scan_workflow(scan_id=42, target="example.com")
    # Dispatch returns a running workflow; workers persist terminal state.
    assert wf["status"] == "running"
    # confirm we attempted to enqueue recon as first stage
    assert len(called) == 1
    assert called[0][0] == "workers.recon.run"
    assert called[0][3]["link"] is not None
    assert [signature.task for signature in called[0][3]["link"].tasks] == [
        "workers.enum.run",
        "workers.vuln.run",
        "workers.report.run",
    ]


def test_fallback_run_retries(monkeypatch):
    attempts = {"count": 0}

    def flaky_send(task_name, args=(), queue=None, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("broker down")
        return True

    monkeypatch.setattr("backend.orchestrator.orchestrator.celery_app.send_task", flaky_send)

    wf = run_scan_workflow(scan_id=99, target="example.org")
    assert wf["status"] == "running"
    # flaky_send should have been retried at least twice
    assert attempts["count"] >= 2


def test_event_handlers_update_scanstore(monkeypatch):
    # ensure send_task is no-op
    monkeypatch.setattr("backend.orchestrator.orchestrator.celery_app.send_task", lambda *a, **k: True)
    # create a scan record via ScanStore and run workflow
    from backend.storage import ScanStore

    ss = ScanStore()
    record = ss.create_record("EvTest", "example.org", status="queued")
    run_scan_workflow(scan_id=record["id"], target=record["target"])
    # scan store remains running until workers report terminal state
    updated = ss._read()
    found = [r for r in updated if r.get("id") == record["id"]][0]
    assert found["status"] == "running"
