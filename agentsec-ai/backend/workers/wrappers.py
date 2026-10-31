"""Thin Celery task wrappers matching orchestrator stage names.

These wrappers provide tasks named to match `STAGE_MAP` so the
orchestrator can enqueue them. They call into the concrete agent
start functions implemented elsewhere.
"""

from backend.workers.celery_app import celery_app
import asyncio

from backend.workers.enum_agent import _async_start_enum
from backend.workers.vuln_agent import _async_start_vuln


@celery_app.task(bind=True, name="workers.enum.run")
def enum_run(self, scan_id: str, target: str | None = None) -> dict:
    # target may be unused; call enum with scan_id and attempt to load context
    return asyncio.run(_async_start_enum(scan_id))


@celery_app.task(bind=True, name="workers.vuln.run")
def vuln_run(self, scan_id: str, target: str | None = None) -> dict:
    # Load a minimal context file if present
    import json
    import os

    data_dir = os.path.join(os.getcwd(), "backend", "data")
    ctx_path = os.path.join(data_dir, f"context_{scan_id}.json")
    ctx = {}
    if os.path.exists(ctx_path):
        with open(ctx_path, "r", encoding="utf-8") as f:
            ctx = json.load(f)
    return asyncio.run(_async_start_vuln(scan_id, ctx))
