"""Per-scan report routes backed by verified worker results."""

from typing import Any
import re
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.config.settings import settings
from backend.reports.report_builder import build_pdf_artifact, build_report_artifacts
from backend.storage import FindingsStore, ScanStore
from backend.workflow_store import WorkflowStore

router = APIRouter(prefix="/reports", tags=["reports"])
_findings_store = FindingsStore()
_scan_store = ScanStore()
_workflow_store = WorkflowStore()


class ReportSummary(BaseModel):
    status: str
    steps: int
    target: str
    findings_count: int
    artifacts: list[dict[str, str]]


class ReportRecord(BaseModel):
    scan_id: int
    target: str
    summary: ReportSummary


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return ""


def _commands(value: Any) -> list[str]:
    commands: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"command", "command_executed"} and isinstance(item, str) and item not in commands:
                commands.append(item)
            else:
                commands.extend(_commands(item))
    elif isinstance(value, list):
        for item in value:
            commands.extend(_commands(item))
    return list(dict.fromkeys(commands))


def _sanitize_command(command: str) -> str:
    """Keep reproducible command context without exposing credentials."""

    sanitized = re.sub(
        r"(?i)(--?(?:token|password|passwd|secret|api[-_]?key)(?:=|\s+))\S+",
        r"\1[REDACTED]",
        command,
    )
    return sanitized.replace("Authorization:", "Authorization: [REDACTED]")


def _iso(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return value if isinstance(value, str) else None


def _tool_metadata(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return []
    return [
        {
            "tool": tool.get("tool") or tool.get("plugin") or "unknown",
            "version": tool.get("version") or tool.get("tool_version"),
            "status": "success" if tool.get("success", True) else "failed",
            "exit_code": tool.get("exit_code"),
            "duration_ms": tool.get("duration_ms"),
        }
        for tool in tools
        if isinstance(tool, dict)
    ]


async def _workflows_for_all_scans() -> list[ReportRecord]:
    scans = (
        await _scan_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else _scan_store.list_records()
    )
    findings = (
        await _findings_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else _findings_store.list_records()
    )
    records: list[ReportRecord] = []
    for scan in scans:
        scan_id = int(scan["id"])
        workflow = (
            await _workflow_store.get_state_async(scan_id)
            if settings.storage_backend.lower() == "postgres"
            else _workflow_store.get_state(scan_id)
        )
        if workflow is None:
            continue
        scan_findings = [finding for finding in findings if finding.get("scan_id") == scan_id]
        artifacts = build_report_artifacts(
            target=scan["target"],
            findings=scan_findings,
            scan_id=scan_id,
        )
        records.append(
            ReportRecord(
                scan_id=scan_id,
                target=scan["target"],
                summary=ReportSummary(
                    status=workflow.get("status", scan.get("status", "unknown")),
                    steps=len(workflow.get("tasks", workflow.get("steps", []))),
                    target=scan["target"],
                    findings_count=len(scan_findings),
                    artifacts=[
                        {"format": item["format"], "name": item["name"]}
                        for item in artifacts
                    ],
                ),
            )
        )
    return records


@router.get("", response_model=list[ReportRecord])
async def list_reports() -> list[ReportRecord]:
    """Return one report entry for every scan with persisted workflow data."""
    return await _workflows_for_all_scans()


@router.get("/{scan_id}")
async def get_report(scan_id: int) -> dict[str, Any]:
    """Return the selected scan's real tasks, commands, results, and findings."""
    scans = (
        await _scan_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else _scan_store.list_records()
    )
    scan = next((item for item in scans if item["id"] == scan_id), None)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="scan not found")
    workflow = (
        await _workflow_store.get_state_async(scan_id)
        if settings.storage_backend.lower() == "postgres"
        else _workflow_store.get_state(scan_id)
    )
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no persisted workflow exists for this scan",
        )
    results = (
        await _workflow_store.get_results_async(scan_id)
        if settings.storage_backend.lower() == "postgres"
        else _workflow_store.get_results(scan_id)
    )
    result_by_task = {item["tool_name"]: item for item in results}
    tasks = workflow.get("tasks", [])
    if not tasks:
        tasks = [
            {"task_name": step.get("name", ""), "status": step.get("status", "unknown"), "task_id": ""}
            for step in workflow.get("steps", [])
        ]
    steps = []
    for task in tasks:
        stored = result_by_task.get(task.get("task_name"), {})
        payload = stored.get("payload")
        raw_commands = _commands(payload)
        task_start = task.get("started_at")
        task_end = task.get("completed_at")
        steps.append(
            {
                "task_id": task.get("task_id", ""),
                "task_name": task.get("task_name", ""),
                "status": task.get("status", stored.get("status", "unknown")),
                "result_status": stored.get("status", ""),
                "commands": [_sanitize_command(command) for command in raw_commands],
                "raw_evidence": payload,
                "started_at": _iso(task_start),
                "completed_at": _iso(task_end),
                "duration_ms": task.get("duration_ms"),
                "retries": task.get("retries", 0),
                "worker_hostname": task.get("worker_hostname"),
                "exit_code": task.get("exit_code"),
                "tools": _tool_metadata(payload),
                "result": payload,
                "error": (
                    _as_text(payload.get("error")) if isinstance(payload, dict) else ""
                ),
            }
        )
    all_findings = (
        await _findings_store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else _findings_store.list_records()
    )
    scan_findings = [finding for finding in all_findings if finding.get("scan_id") == scan_id]
    starts = [step["started_at"] for step in steps if step.get("started_at")]
    ends = [step["completed_at"] for step in steps if step.get("completed_at")]
    failed_steps = [step for step in steps if step["status"] in {"failed", "error"}]
    skipped_steps = [step for step in steps if step["status"] in {"skipped", "unavailable"}]
    tool_versions = [
        tool
        for step in steps
        for tool in step.get("tools", [])
        if tool.get("version")
    ]
    configuration = {
        "selected_attack_categories": scan.get("selected_attack_categories") or [],
        "scan_name": scan.get("name", ""),
        "target": scan["target"],
    }
    return {
        "scan_id": scan_id,
        "target": scan["target"],
        "status": workflow.get("status", scan.get("status", "unknown")),
        "steps": steps,
        "findings": scan_findings,
        "executive_summary": {
            "headline": (
                f"{len(scan_findings)} finding(s) identified"
                if scan_findings
                else "No findings were recorded by the completed checks"
            ),
            "risk": sorted(
                {str(finding.get("severity", "info")).upper() for finding in scan_findings}
            ),
            "coverage": f"{len(steps) - len(failed_steps) - len(skipped_steps)} of {len(steps)} stages returned usable data",
        },
        "scope": {
            "target": scan["target"],
            "authorization_record": "Scan was accepted by the target authorization gate.",
        },
        "timeline": {
            "started_at": min(starts) if starts else None,
            "ended_at": max(ends) if ends else None,
            "stages": [
                {
                    "name": step["task_name"],
                    "status": step["status"],
                    "started_at": step.get("started_at"),
                    "completed_at": step.get("completed_at"),
                    "duration_ms": step.get("duration_ms"),
                }
                for step in steps
            ],
        },
        "tool_versions": tool_versions,
        "failed_checks": failed_steps,
        "skipped_checks": skipped_steps,
        "coverage_limitations": [
            "Only stages dispatched for this scan are represented.",
            "A missing worker result is not interpreted as a clean result.",
        ],
        "scan_configuration": configuration,
        "analyst_notes": "",
        "summary": {
            "step_count": len(steps),
            "finding_count": len(scan_findings),
            "message": (
                "No findings were recorded for this scan."
                if not scan_findings
                else f"{len(scan_findings)} finding(s) came from this scan."
            ),
        },
    }


@router.get("/{scan_id}/pdf")
async def download_report_pdf(scan_id: int) -> FileResponse:
    """Generate and download the redacted report for one scan as PDF."""

    detail = await get_report(scan_id)
    path = build_pdf_artifact(detail["target"], detail["findings"], scan_id, detail=detail)
    return FileResponse(path, media_type="application/pdf", filename=path.name)
