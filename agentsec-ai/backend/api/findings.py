"""Finding routes for AgentSec AI."""

import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.storage import FindingsStore
from backend.config.settings import settings
from backend.config.database import AsyncSessionFactory
from backend.repositories import ActiveApiRepository

router = APIRouter(prefix="/findings", tags=["findings"])


class FindingRecord(BaseModel):
    """Simple in-memory finding record used by the API."""

    id: int
    title: str
    severity: str = Field(default="medium")
    status: str = Field(default="open")
    scan_id: int | None = None
    task_id: str | None = None
    affected_url: str | None = None
    description: str | None = None
    evidence: dict | list | str | None = None
    source_tool: str | None = None
    category: str | None = None
    confidence: float | None = None
    asset: str | None = None
    parameter: str | None = None
    remediation: str | None = None
    cwe: str | None = None
    owasp_category: str | None = None
    verification_state: str = "unverified"
    analyst_notes: str | None = None
    assignee: str | None = None
    due_date: datetime | None = None
    risk_acceptance: bool = False
    dedup_key: str | None = None


class FindingUpdate(BaseModel):
    title: str | None = None
    severity: str | None = None
    status: str | None = None
    description: str | None = None
    evidence: dict | list | str | None = None
    source_tool: str | None = None
    category: str | None = None
    confidence: float | None = None
    asset: str | None = None
    parameter: str | None = None
    remediation: str | None = None
    cwe: str | None = None
    owasp_category: str | None = None
    verification_state: str | None = None
    analyst_notes: str | None = None
    assignee: str | None = None
    due_date: datetime | None = None
    risk_acceptance: bool | None = None


_store = FindingsStore(os.getenv("AGENTSEC_FINDINGS_STORE", None))


def _load_findings() -> list[FindingRecord]:
    return [
        FindingRecord(
            id=item["id"],
            title=item["title"],
            severity=item["severity"],
            status=item["status"],
            scan_id=item.get("scan_id"),
            task_id=item.get("task_id"),
            affected_url=item.get("affected_url"),
            description=item.get("description"),
            evidence=item.get("evidence"),
        )
        for item in _store.list_records()
    ]


@router.get("", response_model=list[FindingRecord])
async def list_findings() -> list[FindingRecord]:
    """Return the current finding inventory."""

    if settings.storage_backend.lower() == "postgres":
        return [FindingRecord(**item) for item in await _store.list_records_async()]
    return _load_findings()


@router.get("/{finding_id}", response_model=FindingRecord)
async def get_finding(finding_id: int) -> FindingRecord:
    """Return a specific finding by identifier."""

    records = (
        [FindingRecord(**item) for item in await _store.list_records_async()]
        if settings.storage_backend.lower() == "postgres"
        else _load_findings()
    )
    for finding in records:
        if finding.id == finding_id:
            return finding

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="finding not found")


@router.patch("/{finding_id}", response_model=FindingRecord)
async def update_finding(finding_id: int, update: FindingUpdate) -> FindingRecord:
    """Update analyst workflow fields for a persisted PostgreSQL finding."""
    if settings.storage_backend.lower() != "postgres":
        raise HTTPException(status_code=501, detail="finding updates require PostgreSQL storage")
    async with AsyncSessionFactory() as session:
        record = await ActiveApiRepository(session).update_finding(
            finding_id, **update.model_dump(exclude_unset=True)
        )
    if record is None:
        raise HTTPException(status_code=404, detail="finding not found")
    return FindingRecord(**record)
