"""Integration-like test: verify orchestrator enqueues Celery tasks."""


from backend.orchestrator.orchestrator import run_scan_workflow


def test_run_scan_enqueues_tasks(monkeypatch):
    sent = []

    def fake_send_task(name, args=None, queue=None, **kwargs):
        sent.append((name, args, queue, kwargs))

    # Patch the celery_app.send_task used by the orchestrator module
    monkeypatch.setattr("backend.orchestrator.orchestrator.celery_app.send_task", fake_send_task)

    wf = run_scan_workflow(123, "example.com")

    assert wf["scan_id"] == 123
    assert len(sent) == 1
    assert sent[0][0] == "workers.recon.run"
    assert [signature.task for signature in sent[0][3]["link"].tasks] == [
        "workers.enum.run",
        "workers.vuln.run",
        "workers.report.run",
    ]