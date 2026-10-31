"""Report generation agent Celery tasks."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

from backend.config.settings import settings
from backend.reports.report_builder import build_report_artifacts
from backend.storage import FindingsStore, ScanStore
from backend.workers.celery_app import celery_app
from backend.core.cancellation import is_scan_cancelled


async def _async_start_report(self: Any, scan_id: str) -> dict[str, Any]:
    """Write the supported Markdown and JSON report files for a scan target."""
    scan_store = ScanStore()
    findings_store = FindingsStore()
    scans = (
        await scan_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else scan_store.list_records()
    )
    findings = (
        await findings_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else findings_store.list_records()
    )
    scan = next(
        (item for item in scans if str(item["id"]) == str(scan_id)),
        None,
    )
    if scan is None:
        raise ValueError(f"Scan {scan_id} does not exist")
    scan_findings = [item for item in findings if item.get("scan_id") == int(scan_id)]
    artifacts = build_report_artifacts(
        target=scan["target"],
        findings=scan_findings,
        scan_id=scan_id,
    )
    findings_count = len(scan_findings)
    summary = {
        "scan_id": scan_id,
        "status": "complete",
        "artifacts": artifacts,
        "total_findings": findings_count,
        "generated_at": datetime.utcnow().isoformat(),
        "ai_enabled": False,
    }

    return summary


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
def start_report(self, scan_id: str) -> dict[str, Any]:
    """Trigger the report generation flow and return the resulting metadata."""
    return asyncio.run(_async_start_report(self, scan_id))


@celery_app.task(bind=True, name="workers.report.run", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def run(self, scan_id: int, target: str) -> dict[str, Any]:
    """Generate real Markdown and JSON artifacts for the target."""
    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "target": target, "status": "cancelled"}
    return asyncio.run(_async_start_report(self, str(scan_id)))
