"""Recon agent Celery tasks.

This task runs a set of recon plugins via the central plugin executor,
deduplicates subdomain results and persists them via the ReconResultProcessor.
The implementation intentionally keeps DB interactions out of scope and uses
the processor helper for persistence to keep unit tests simple.
"""

from typing import Any, Dict, List
import asyncio
import logging

from backend.workers.celery_app import celery_app
from backend.plugins.executor import executor
from backend.plugins.registry import registry
from backend.plugins.base_plugin import PluginInput
from backend.config.settings import settings
from backend.core.cancellation import is_scan_cancelled


@celery_app.task(bind=True, name="workers.recon.run", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def start(self, scan_id: str, target: str, tool_decisions: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """Entrypoint Celery task for running reconnaissance.

    `tool_decisions` is expected to be a list of plugin names or dicts describing
    which plugins to run. If omitted, the registry is autodiscovered and all
    plugins with category 'recon' are executed.
    """

    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "target": target, "status": "cancelled", "tools": []}
    # Run synchronous wrapper for the async orchestration
    return asyncio.run(_async_start(scan_id, target, tool_decisions, self.request.id))


async def _async_start(
    scan_id: str,
    target: str,
    tool_decisions: List[Dict[str, Any]] | None = None,
    task_id: str | None = None,
) -> Dict[str, Any]:
    # Ensure registry has entries
    registry.auto_discover()

    # Resolve plugin names to run
    if tool_decisions:
        names = [t if isinstance(t, str) else t.get("name") for t in tool_decisions]
    else:
        names = [m["name"] for m in registry.list_all() if m.get("category") == "recon"]

    results = []
    failures = []
    for name in names:
        if not name:
            continue
        if is_scan_cancelled(scan_id):
            return {"scan_id": scan_id, "target": target, "status": "cancelled", "tools": results}
        try:
            inp = PluginInput(
                scan_id=scan_id,
                target=target,
                task_id=task_id,
                timeout=settings.scan.tool_timeout_seconds,
            )
            out = executor.run(name, inp)
            results.append(
                {
                    "plugin": name,
                    "success": out.success,
                    "record_count": out.record_count,
                    "parsed": out.parsed,
                    "raw_output": out.raw_output,
                    "command_executed": out.command_executed,
                    "execution_time": out.execution_time,
                    "error": out.error_message,
                }
            )
            if not out.success:
                failures.append({"plugin": name, "error": out.error_message or "tool execution failed"})
        except Exception as exc:
            logging.getLogger(__name__).exception("Recon plugin %s failed for scan %s", name, scan_id)
            failures.append({"plugin": name, "error": str(exc)})

    # Deduplicate subdomains across all results
    subs = set()
    for r in results:
        for item in r.get("parsed", []):
            sub = (
                item.get("subdomain")
                or item.get("host")
                or item.get("url")
                or item.get("value")
            )
            if sub:
                subs.add(sub)

    # persist via lightweight processor
    from backend.workers.processors.recon_processor import ReconResultProcessor

    proc = ReconResultProcessor()
    count = await proc.store_subdomains(scan_id, list(subs))

    return {
        "scan_id": scan_id,
        "target": target,
        "discovered_count": count,
        "tools": results,
        "tool_errors": failures,
    }
