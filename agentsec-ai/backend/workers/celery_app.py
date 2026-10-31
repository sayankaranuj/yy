"""Celery application configuration for AgentSec AI."""

from __future__ import annotations

from celery import Celery
from celery.signals import task_failure, task_postrun, task_prerun

from backend.config.settings import settings

celery_app = Celery("agentsec")
celery_app.conf.update(
    broker_url=settings.celery.broker_url,
    result_backend=settings.celery.result_backend,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_send_sent_event=True,
    worker_send_task_events=True,
    result_expires=86400,
    task_soft_time_limit=max(60, settings.scan.tool_timeout_seconds - 30),
    task_time_limit=max(60, settings.scan.tool_timeout_seconds),
    worker_max_tasks_per_child=50,
    beat_schedule={},
    task_default_queue="orchestrator_queue",
    broker_connection_timeout=1,
    broker_connection_retry_on_startup=False,
    task_publish_retry_policy={
        "max_retries": 0,
        "interval_start": 0,
        "interval_step": 0,
        "interval_max": 0,
    },
)

celery_app.conf.task_routes = {
    "recon.*": {"queue": "recon_queue"},
    "workers.recon.*": {"queue": "recon_queue"},
    "enum.*": {"queue": "enum_queue"},
    "workers.enum.*": {"queue": "enum_queue"},
    "vuln.*": {"queue": "vuln_queue"},
    "workers.vuln.*": {"queue": "vuln_queue"},
    "secrets.*": {"queue": "secrets_queue"},
    "exploit.*": {"queue": "exploit_queue"},
    "report.*": {"queue": "report_queue"},
    "orchestrator.*": {"queue": "orchestrator_queue"},
    "worker.recovery.*": {"queue": "workflow_recovery_queue"},
    "worker.dead_letter.*": {"queue": "workflow_dead_letter_queue"},
    "workers.preflight.run": {"queue": "recon_queue"},
}


def _task_scan_id(args: tuple[object, ...]) -> int | None:
    """Extract the integer scan identifier from task arguments."""

    if not args:
        return None
    try:
        return int(args[0])
    except (TypeError, ValueError):
        return None


@task_prerun.connect
def mark_task_started(task_id: str, task: object, args: tuple[object, ...], **_: object) -> None:
    """Persist a running state when a scan task starts."""

    scan_id = _task_scan_id(args)
    if scan_id is not None:
        from backend.workers.progress import update_task
        from backend.core.cancellation import is_scan_cancelled

        update_task(scan_id, task.name, task_id, "cancelled" if is_scan_cancelled(scan_id) else "running")


@task_postrun.connect
def mark_task_finished(
    task_id: str,
    task: object,
    args: tuple[object, ...],
    retval: object = None,
    state: str | None = None,
    **_: object,
) -> None:
    """Persist a successful or terminal Celery task state."""

    scan_id = _task_scan_id(args)
    if scan_id is not None:
        from backend.workers.progress import update_task

        task_status = {
            "SUCCESS": "completed",
            "FAILURE": "failed",
            "RETRY": "retrying",
        }.get(state or "", "failed")
        if isinstance(retval, dict) and retval.get("status") == "cancelled":
            task_status = "cancelled"
        update_task(scan_id, task.name, task_id, task_status, retval)


@task_failure.connect
def mark_task_failed(
    task_id: str,
    task: object,
    args: tuple[object, ...],
    exception: BaseException,
    **_: object,
) -> None:
    """Persist a failed Celery task state."""

    scan_id = _task_scan_id(args)
    if scan_id is not None:
        from backend.workers.progress import update_task

        update_task(scan_id, task.name, task_id, "failed", str(exception))

# Backwards-compatible alias expected by tests
app = celery_app


@celery_app.task(bind=True, name="orchestrator.run_scan")
def _orchestrator_run(self, scan_id=None, target=None):
    """Placeholder registration for tests and orchestration compatibility."""
    return {"scan_id": scan_id, "target": target}


@celery_app.task(name="workers.preflight.run", queue="recon_queue")
def run_preflight_task() -> list[dict]:
    """Run tool readiness checks in a worker image containing the binaries."""

    from backend.plugins.preflight import run_preflight

    return run_preflight()


@celery_app.task(
    bind=True,
    name="report.start",
    queue="report_queue",
    max_retries=2,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    soft_time_limit=1800,
    time_limit=2100,
)
def start_report(self, scan_id: str) -> dict:
    """Register the report generation task required by the Phase 9 workflow."""
    return {"scan_id": scan_id, "status": "queued"}


# Import task modules after the Celery application exists so workers register
# the task while avoiding a circular import during application construction.
from backend.workers import enum_agent as _enum_agent  # noqa: E402,F401
from backend.workers import recon_agent as _recon_agent  # noqa: E402,F401
from backend.workers import report_agent as _report_agent  # noqa: E402,F401
from backend.workers import vuln_agent as _vuln_agent  # noqa: E402,F401
from backend.workers import secret_agent as _secret_agent  # noqa: E402,F401
