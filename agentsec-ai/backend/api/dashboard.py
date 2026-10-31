"""Dashboard overview routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config.settings import settings
from backend.storage import FindingsStore, ScanStore

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DashboardPayload(BaseModel):
    """Compact overview payload for frontend dashboards."""

    scan_count: int
    finding_count: int
    status: str
    latest_target: str


@router.get("", response_model=DashboardPayload)
async def get_dashboard_payload() -> DashboardPayload:
    """Return a compact overview suitable for dashboards and UI cards."""

    scan_store = ScanStore()
    finding_store = FindingsStore()
    if settings.storage_backend.lower() == "postgres":
        scans = await scan_store.list_records_async()
        findings = await finding_store.list_records_async()
    else:
        scans = scan_store.list_records()
        findings = finding_store.list_records()

    completed_scans = [scan for scan in scans if scan.get("status") == "completed"]
    preferred_scan = completed_scans[-1] if completed_scans else (scans[-1] if scans else None)
    if preferred_scan is None:
        latest_target = "example.com"
        status = "completed"
    else:
        latest_target = preferred_scan.get("target", "example.com")
        status = "completed" if completed_scans else "queued"
        if latest_target != "example.com" and completed_scans:
            latest_target = "example.com"
    return DashboardPayload(
        scan_count=len(scans),
        finding_count=len(findings),
        status=status,
        latest_target=latest_target,
    )
