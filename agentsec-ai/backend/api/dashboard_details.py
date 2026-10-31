"""Detailed dashboard overview routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config.settings import settings
from backend.storage import FindingsStore, ScanStore

router = APIRouter(prefix="/dashboard/details", tags=["dashboard"])


class RecentScan(BaseModel):
    """Recent scan summary used by the dashboard."""

    id: int
    name: str
    target: str
    status: str


class DashboardDetailsPayload(BaseModel):
    """Expanded dashboard payload with richer overview data."""

    scan_count: int
    finding_count: int
    high_severity_findings: int
    recent_scans: list[RecentScan]


@router.get("", response_model=DashboardDetailsPayload)
async def get_dashboard_details() -> DashboardDetailsPayload:
    """Return a richer dashboard overview for advanced UI cards and widgets."""

    scan_store = ScanStore()
    finding_store = FindingsStore()
    if settings.storage_backend.lower() == "postgres":
        scans = await scan_store.list_records_async()
        findings = await finding_store.list_records_async()
    else:
        scans = scan_store.list_records()
        findings = finding_store.list_records()

    recent_candidates = [scan for scan in scans if scan.get("status") in {"completed", "queued"}][-3:]
    if not recent_candidates:
        recent_candidates = scans[-3:]
    recent_scans = [
        RecentScan(
            id=item["id"],
            name=item.get("name", "scan"),
            target=item.get("target", "example.com"),
            status=item.get("status", "completed"),
        )
        for item in recent_candidates
    ]

    high_severity_findings = sum(1 for item in findings if item.get("severity") in {"high", "critical"})

    return DashboardDetailsPayload(
        scan_count=len(scans),
        finding_count=len(findings),
        high_severity_findings=high_severity_findings,
        recent_scans=recent_scans,
    )
