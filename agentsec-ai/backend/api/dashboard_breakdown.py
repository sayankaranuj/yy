"""Severity breakdown dashboard routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config.settings import settings
from backend.storage import FindingsStore

router = APIRouter(prefix="/dashboard/breakdown", tags=["dashboard"])


class BreakdownPayload(BaseModel):
    """Severity breakdown payload for dashboard charts."""

    total_findings: int
    severity_breakdown: dict[str, int]


@router.get("", response_model=BreakdownPayload)
async def get_dashboard_breakdown() -> BreakdownPayload:
    """Return a severity breakdown suitable for charts and progress cards."""

    finding_store = FindingsStore()
    findings = (
        await finding_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else finding_store.list_records()
    )

    severity_breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for finding in findings:
        severity = finding.get("severity", "medium").lower()
        if severity in severity_breakdown:
            severity_breakdown[severity] += 1
        else:
            severity_breakdown["medium"] += 1

    return BreakdownPayload(
        total_findings=len(findings),
        severity_breakdown=severity_breakdown,
    )
