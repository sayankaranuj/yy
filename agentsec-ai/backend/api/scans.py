"""Scan management routes for AgentSec AI."""

import ipaddress
import os
import re
import asyncio
import time
from urllib.parse import urlsplit

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field, field_validator, model_validator

from backend.orchestrator.orchestrator import run_scan_workflow
from backend.config.settings import settings
from backend.storage import ScanStore, TargetStore
from backend.workflow_store import WorkflowStore
from backend.api.schemas import ATTACK_CATALOG, valid_attack_categories
from backend.core.scan_lifecycle import validate_transition
from backend.workers.celery_app import celery_app
from backend.core.cancellation import request_scan_cancellation, clear_scan_cancellation

router = APIRouter(prefix="/scans", tags=["scans"])


class ScanCreateRequest(BaseModel):
    """Payload for creating a scan."""

    name: str = Field(min_length=1)
    target: str = Field(min_length=1)
    selected_attack_categories: list[str] | None = None
    git_options: dict[str, object] | None = None

    @field_validator("selected_attack_categories")
    @classmethod
    def validate_attack_categories(cls, value: list[str] | None) -> list[str] | None:
        """Reject selector keys that are not in the authoritative catalog."""

        if value is None:
            return None
        invalid = sorted(set(value) - valid_attack_categories())
        if invalid:
            raise ValueError(f"unknown attack categories: {', '.join(invalid)}")
        return sorted(set(value))

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        """Allow host-like targets while rejecting unsafe scan input."""

        target = value.strip()
        if settings.app_env.lower() == "development" and target.lower().startswith(("http://localhost:", "https://localhost:", "localhost:")):
            return target.lower().rstrip("/")
        if not target or any(char in target for char in "\r\n\x00"):
            raise ValueError("target must be a valid host")
        if re.search(r"[<>]|(;|&&|\|\||`)|(--|/\*)", target):
            raise ValueError("target must be a valid host")
        try:
            address = ipaddress.ip_address(target)
        except ValueError:
            return target
        if not address.is_global:
            raise ValueError("private or non-routable targets are not allowed")
        return target

    @model_validator(mode="after")
    def validate_git_repository_scan(self):
        if "secrets.git_scan" not in (self.selected_attack_categories or []):
            return self
        if self.git_options:
            allowed = {"branch", "since_commit", "until_commit", "baseline"}
            if set(self.git_options) - allowed:
                raise ValueError("unsupported Git scan option")
            for key in ("branch", "since_commit", "until_commit"):
                value = self.git_options.get(key)
                if value is not None and (not isinstance(value, str) or len(value) > 255):
                    raise ValueError(f"{key} must be a short string")
        parsed = urlsplit(self.target)
        components = [part for part in parsed.path.split("/") if part]
        if (
            parsed.scheme != "https"
            or parsed.hostname not in {"github.com", "gitlab.com", "bitbucket.org"}
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or len(components) != 2
        ):
            raise ValueError(
                "Git scans require a public HTTPS repository URL on GitHub, GitLab, or Bitbucket"
            )
        return self


class ScanRecord(BaseModel):
    """Simple in-memory scan record used by the API."""

    id: int
    name: str
    target: str
    status: str
    selected_attack_categories: list[str] | None = None
    git_options: dict[str, object] | None = None


_store = ScanStore(os.getenv("AGENTSEC_SCAN_STORE", None))
_target_store = TargetStore()
_workflow_store = WorkflowStore()
_rate_lock = asyncio.Lock()
_request_times: list[float] = []


def _is_development_local_target(target: str) -> bool:
    """Allow only loopback targets to use the development authorization path."""

    parsed = urlsplit(target if "://" in target else f"//{target}")
    return (
        settings.app_env.lower() == "development"
        and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    )


def _load_scans() -> list[ScanRecord]:
    return [
        ScanRecord(
            id=item["id"],
            name=item["name"],
            target=item["target"],
            status=item["status"],
            selected_attack_categories=item.get("selected_attack_categories"),
        )
        for item in _store.list_records()
    ]


async def _dispatch_scan_work(
    scan_id: int,
    target: str,
    selected_attack_categories: list[str] | None = None,
    git_options: dict[str, str | bool] | None = None,
) -> None:
    """Advance a scan through the orchestrator workflow in the background."""

    stages = ["workers.recon.run", "workers.enum.run", "workers.vuln.run", "workers.report.run"]
    if selected_attack_categories and "secrets.git_scan" in selected_attack_categories:
        stages.insert(-1, "workers.git.run")
    if selected_attack_categories is not None:
        selected = set(selected_attack_categories)
        stages = [
            stage
            for stage in stages
            if stage == "workers.report.run"
            or any(
                category.startswith(
                    {
                        "workers.recon.run": "recon",
                        "workers.enum.run": "enum",
                        "workers.vuln.run": "vuln",
                        "workers.git.run": "secrets",
                    }[stage]
                    + "."
                )
                for category in selected
            )
        ]
    if selected_attack_categories and "secrets.git_scan" in selected_attack_categories:
        stages = [stage for stage in stages if stage in {"workers.git.run", "workers.report.run"}]
    workflow = {
        "target": target,
        "status": "queued",
        "steps": [
            {"name": stage, "status": "queued", "details": ""}
            for stage in stages
        ],
    }
    if settings.storage_backend.lower() == "postgres":
        await _workflow_store.upsert_workflow_async(scan_id, workflow)
    else:
        _workflow_store.upsert_workflow(scan_id, workflow)

    try:
        await asyncio.to_thread(
            run_scan_workflow,
            scan_id=scan_id,
            target=target,
            persist=False,
            selected_attack_categories=selected_attack_categories,
            git_options=git_options,
        )
    except Exception as exc:
        failed_workflow = {
            **workflow,
            "status": "failed",
            "steps": [
                {**step, "status": "failed", "details": str(exc)}
                for step in workflow["steps"]
            ],
        }
        if settings.storage_backend.lower() == "postgres":
            await _workflow_store.upsert_workflow_async(scan_id, failed_workflow)
            await _store.update_status_async(scan_id, "failed")
        else:
            _workflow_store.upsert_workflow(scan_id, failed_workflow)
            _store.update_status(scan_id, "failed")


@router.get("", response_model=list[ScanRecord])
async def list_scans() -> list[ScanRecord]:
    """Return the current scan inventory."""

    if settings.storage_backend.lower() == "postgres":
        return [ScanRecord(**item) for item in await _store.list_records_async()]
    return _load_scans()


@router.post("", response_model=ScanRecord, status_code=status.HTTP_201_CREATED)
async def create_scan(
    payload: ScanCreateRequest,
    background_tasks: BackgroundTasks,
) -> ScanRecord:
    """Create a new scan and return the persisted record."""

    is_git_scan = "secrets.git_scan" in (payload.selected_attack_categories or [])
    if is_git_scan:
        from backend.api.targets import normalize_target

        normalized_target = payload.target.strip().lower().rstrip("/")
        approval_target = normalize_target(normalized_target)
    else:
        from backend.api.targets import normalize_target

        normalized_target = payload.target.strip().lower().rstrip(".")
        approval_target = normalize_target(normalized_target)
    approved = (
        await _target_store.is_approved_async(approval_target)
        if settings.storage_backend.lower() == "postgres"
        else _target_store.is_approved(approval_target)
    )
    if not approved and not _is_development_local_target(normalized_target):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"target '{normalized_target}' is not approved by an administrator; "
                f"approval is checked as '{approval_target}'"
            ),
        )

    now = time.monotonic()
    async with _rate_lock:
        _request_times[:] = [stamp for stamp in _request_times if now - stamp < 60]
        if len(_request_times) >= settings.scan.rate_limit_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="scan rate limit exceeded",
            )
        _request_times.append(now)

    if settings.storage_backend.lower() == "postgres":
        stored_record = await _store.create_record_async(
            payload.name,
            normalized_target,
            "queued",
            payload.selected_attack_categories,
            payload.git_options,
        )
    else:
        stored_record = _store.create_record(
            name=payload.name,
            target=normalized_target,
            status="queued",
            selected_attack_categories=payload.selected_attack_categories,
            git_options=payload.git_options,
        )
    record = ScanRecord(
        id=stored_record["id"],
        name=stored_record["name"],
        target=stored_record["target"],
        status=stored_record["status"],
        selected_attack_categories=stored_record.get("selected_attack_categories"),
        git_options=stored_record.get("git_options"),
    )
    background_tasks.add_task(
        _dispatch_scan_work,
        record.id,
        normalized_target,
        payload.selected_attack_categories,
    )
    return record


@router.get("/attack-catalog")
async def get_attack_catalog() -> dict[str, object]:
    """Return the authoritative attack selector catalog."""

    return ATTACK_CATALOG


@router.get("/{scan_id}", response_model=ScanRecord)
async def get_scan(scan_id: int) -> ScanRecord:
    """Return a specific scan record by identifier."""

    records = (
        [ScanRecord(**item) for item in await _store.list_records_async()]
        if settings.storage_backend.lower() == "postgres"
        else _load_scans()
    )
    for record in records:
        if record.id == scan_id:
            return record

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")


@router.post("/{scan_id}/cancel", response_model=ScanRecord)
async def cancel_scan(scan_id: int) -> ScanRecord:
    """Request cancellation and revoke every currently known Celery task."""

    records = await _store.list_records_async() if settings.storage_backend.lower() == "postgres" else _load_scans()
    scan = next((item for item in records if int(item["id"]) == scan_id), None)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    validate_transition(scan["status"], "cancel_requested")
    request_scan_cancellation(scan_id)
    workflow = (
        await _workflow_store.get_state_async(scan_id)
        if settings.storage_backend.lower() == "postgres"
        else _workflow_store.get_state(scan_id)
    )
    for task in (workflow or {}).get("tasks", []):
        task_id = task.get("task_id")
        if task_id and not str(task_id).startswith("task-"):
            celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")
    if settings.storage_backend.lower() == "postgres":
        await _store.update_status_async(scan_id, "cancel_requested")
        await _workflow_store.set_status_async(scan_id, "cancel_requested")
        await _store.update_status_async(scan_id, "cancelled")
        await _workflow_store.set_status_async(scan_id, "cancelled")
    else:
        _store.update_status(scan_id, "cancelled")
        _workflow_store.set_status(scan_id, "cancelled")
    updated = next(item for item in (await _store.list_records_async() if settings.storage_backend.lower() == "postgres" else _load_scans()) if int(item["id"]) == scan_id)
    return ScanRecord(**updated)


@router.post("/{scan_id}/resume", response_model=ScanRecord)
async def resume_scan(scan_id: int, background_tasks: BackgroundTasks) -> ScanRecord:
    """Resume a failed, partial, or cancelled scan by dispatching a fresh workflow."""

    records = await _store.list_records_async() if settings.storage_backend.lower() == "postgres" else _load_scans()
    scan = next((item for item in records if int(item["id"]) == scan_id), None)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    validate_transition(scan["status"], "queued")
    clear_scan_cancellation(scan_id)
    selected = scan.get("selected_attack_categories")
    if settings.storage_backend.lower() == "postgres":
        await _store.update_status_async(scan_id, "queued")
    else:
        _store.update_status(scan_id, "queued")
    background_tasks.add_task(_dispatch_scan_work, scan_id, scan["target"], selected)
    updated = next(item for item in (await _store.list_records_async() if settings.storage_backend.lower() == "postgres" else _load_scans()) if int(item["id"]) == scan_id)
    return ScanRecord(**updated)
