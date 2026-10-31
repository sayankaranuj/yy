"""Workflow orchestration for AgentSec AI scans."""

from __future__ import annotations

from celery import chain
from typing import Any

from backend.workflow_store import WorkflowStore
from backend.storage import ScanStore
from backend.workers.celery_app import celery_app
from backend.core.eventbus import EventBus
from backend.core.state_machine import StateMachine
from backend.core.fallback import FallbackManager
from backend.core.decision_engine import DecisionEngine
from backend.orchestrator.event_bus import event_bus as redis_event_bus
import logging
import os
import socket
from uuid import uuid4
from urllib.parse import urlparse

from backend.config.settings import settings


_store = WorkflowStore()
# Lightweight in-process event bus for orchestration
event_bus = EventBus()
# Fallback manager for retrying transient failures when enqueueing tasks
fallback = FallbackManager(retries=3, backoff=0.5)


def _publish_live_event(scan_id: int, payload: dict[str, Any]) -> None:
    """Best-effort bridge from synchronous orchestration to Redis events."""

    try:
        redis_event_bus.publish_to_websocket_sync(str(scan_id), payload)
    except Exception:
        logging.getLogger(__name__).debug(
            "Live event publication unavailable for scan %s",
            scan_id,
            exc_info=True,
        )

# Decision engine for routing rules
decision_engine = DecisionEngine()

# Simple decision mapping for which stages to run per scan type
STAGE_MAP = {
    "FULL": ["workers.recon.run", "workers.enum.run", "workers.vuln.run", "workers.report.run"],
    "RECON_ONLY": ["workers.recon.run", "workers.report.run"],
    "VULN_ONLY": ["workers.vuln.run", "workers.report.run"],
    "QUICK": ["workers.recon.run", "workers.vuln.run", "workers.report.run"],
}

# Default simple rules: target string matching for quick or recon-only scans
decision_engine.register_rule(lambda ctx: "recon-only" in (ctx.get("target") or ""), STAGE_MAP["RECON_ONLY"])
decision_engine.register_rule(lambda ctx: "quick" in (ctx.get("target") or ""), STAGE_MAP["QUICK"])


def _broker_is_reachable() -> bool:
    """Check the configured broker quickly before publishing a task."""

    parsed = urlparse(settings.celery.broker_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (6379 if parsed.scheme.startswith("redis") else 5672)
    if os.name == "nt" and host not in {"localhost", "127.0.0.1", "::1"}:
        return False
    try:
        with socket.create_connection((host, port), timeout=0.1):
            return True
    except OSError:
        return False



def run_scan_workflow(
    scan_id: int,
    target: str,
    scan_type: str | None = None,
    *,
    persist: bool = True,
    selected_attack_categories: list[str] | None = None,
    git_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute a lightweight workflow for a scan request, enqueue worker tasks, and persist its state.

    This function enqueues Celery tasks for recon, enum, vuln, and report stages. Tasks are enqueued
    to named queues (recon_queue, enum_queue, vuln_queue, report_queue).
    """

    # transition to running and publish start event
    sm = StateMachine("pending")
    sm.add_transition("pending", "running")
    sm.add_transition("running", "completed")
    sm.trigger("running")
    event_bus.publish("scan.started", {"scan_id": scan_id, "target": target})
    _publish_live_event(
        scan_id,
        {"event": "scan.started", "scan_id": scan_id, "target": target},
    )

    # Enqueue asynchronous tasks for each stage.
    # Decide which stages to run. Default to FULL pipeline if scan_type not provided.
    if not scan_type:
        scan_type = "FULL"

    # Allow decision engine to override stages based on context
    ctx = {"scan_id": scan_id, "target": target, "scan_type": scan_type}
    decided = decision_engine.decide(ctx)
    stages = list(decided if decided is not None else STAGE_MAP.get(scan_type, STAGE_MAP["FULL"]))
    if selected_attack_categories is not None:
        selected = set(selected_attack_categories)
        if "secrets.git_scan" in selected and "workers.git.run" not in stages:
            stages.insert(-1, "workers.git.run")
        stage_categories = {
            "workers.recon.run": "recon",
            "workers.enum.run": "enum",
            "workers.vuln.run": "vuln",
            "workers.git.run": "secrets",
        }
        stages = [
            task
            for task in stages
            if task not in stage_categories
            or any(category.startswith(stage_categories[task] + ".") for category in selected)
        ]

    # Map task name -> queue
    queue_map = {
        "workers.recon.run": "recon_queue",
        "workers.enum.run": "enum_queue",
        "workers.vuln.run": "vuln_queue",
        "workers.git.run": "secrets_queue",
        "workers.report.run": "report_queue",
    }

    task_signatures = []
    for task_name in stages:
        if task_name == "workers.enum.run":
            task_args = (scan_id, target, selected_attack_categories)
        elif task_name == "workers.git.run":
            task_args = (scan_id, target, git_options or {})
        else:
            task_args = (scan_id, target)
        task_signatures.append(
            celery_app.signature(task_name, args=task_args, immutable=True).set(
                queue=queue_map.get(task_name, "orchestrator_queue"),
                task_id=str(uuid4()),
            )
        )

    steps = [
        {
            "name": task_name,
            "task_id": signature.options["task_id"],
            "status": "queued",
            "details": "",
        }
        for task_name, signature in zip(stages, task_signatures)
    ]
    workflow = {
        "scan_id": scan_id,
        "target": target,
        "status": "running",
        "steps": steps,
    }
    if persist:
        _store.upsert_workflow(scan_id, workflow)

    if task_signatures:
        first_task = stages[0]
        first_args = task_signatures[0].args
        first_queue = queue_map.get(first_task, "orchestrator_queue")
        continuation = chain(*task_signatures[1:]) if len(task_signatures) > 1 else None
        try:
            sender = celery_app.send_task
            if getattr(sender, "__self__", None) is celery_app and not _broker_is_reachable():
                raise ConnectionError("Celery broker is unavailable; scan tasks were not dispatched")
            else:
                def publish_task() -> Any:
                    send_options = {"link": continuation} if continuation is not None else {}
                    try:
                        return celery_app.send_task(
                            first_task,
                            args=first_args,
                            queue=first_queue,
                            task_id=task_signatures[0].options["task_id"],
                            retry=False,
                            **send_options,
                        )
                    except TypeError as exc:
                        if "retry" not in str(exc):
                            raise
                        return celery_app.send_task(
                            first_task,
                            args=first_args,
                            queue=first_queue,
                            task_id=task_signatures[0].options["task_id"],
                            **send_options,
                        )

                fallback.run_with_retry_sync(publish_task)
        except Exception as exc:
            logging.getLogger(__name__).exception(
                "Failed to enqueue scan %s workflow", scan_id
            )
            raise RuntimeError("Unable to dispatch scan tasks") from exc

    return workflow


# Register simple event handlers to keep ScanStore in sync with workflow events
_scan_store = ScanStore()


async def _on_scan_started(event_or_payload, payload: dict[str, Any] | None = None) -> None:
    """Accept either (event, payload) or (payload,) signatures."""
    try:
        if payload is None:
            payload = event_or_payload
        scan_id = payload.get("scan_id")
        if scan_id:
            _scan_store.update_status(scan_id, "running")
    except Exception:
        pass


async def _on_scan_completed(event_or_payload, payload: dict[str, Any] | None = None) -> None:
    """Accept either (event, payload) or (payload,) signatures."""
    try:
        if payload is None:
            payload = event_or_payload
        scan_id = payload.get("scan_id")
        workflow = payload.get("workflow")
        if scan_id and workflow:
            _scan_store.update_status(scan_id, "completed")
            _store.upsert_workflow(scan_id, workflow)
    except Exception:
        pass


event_bus.subscribe("scan.started", _on_scan_started)
event_bus.subscribe("scan.completed", _on_scan_completed)


__all__ = ["run_scan_workflow"]