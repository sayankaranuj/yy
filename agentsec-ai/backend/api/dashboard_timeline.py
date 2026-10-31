"""Activity timeline routes for AgentSec AI dashboard."""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config.settings import settings
from backend.storage import FindingsStore, ScanStore

router = APIRouter(prefix="/dashboard/timeline", tags=["dashboard"])


class TimelineEvent(BaseModel):
    """A single recent activity event for the dashboard timeline."""

    id: int
    event_type: str
    message: str
    timestamp: str


@router.get("", response_model=list[TimelineEvent])
async def get_dashboard_timeline() -> list[TimelineEvent]:
    """Return a compact activity timeline for recent scan and finding activity."""

    scan_store = ScanStore()
    finding_store = FindingsStore()
    if settings.storage_backend.lower() == "postgres":
        scans = await scan_store.list_records_async()
        findings = await finding_store.list_records_async()
    else:
        scans = scan_store.list_records()
        findings = finding_store.list_records()

    events: list[TimelineEvent] = []
    for index, scan in enumerate(scans[-3:], start=1):
        events.append(
            TimelineEvent(
                id=index,
                event_type="scan_completed" if scan.get("status") == "completed" else "scan_started",
                message=f"Scan {scan.get('name', 'scan')} reached {scan.get('status', 'queued')} for {scan.get('target', 'example.com')}",
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )

    for index, finding in enumerate(findings[-2:], start=1):
        events.append(
            TimelineEvent(
                id=index + 10,
                event_type="finding_created",
                message=f"Finding {finding.get('title', 'item')} marked {finding.get('status', 'open')}",
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )

    return events[-8:]
