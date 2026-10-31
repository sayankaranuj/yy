"""Helpers for persisting and validating real Celery task results."""

from __future__ import annotations

import json
from typing import Any


_RESULT_PROVENANCE = "celery-task-result-v1"


def encode_task_result(scan_id: int, task_id: str, result: Any) -> str:
    """Encode a task return value with the identifiers needed to verify it later."""

    return json.dumps(
        {
            "provenance": _RESULT_PROVENANCE,
            "scan_id": scan_id,
            "task_id": task_id,
            "result": result,
        },
        separators=(",", ":"),
    )


def verified_workflow_results(
    scan_id: int,
    tasks: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return only result records whose persisted provenance matches this workflow."""

    task_ids = {
        task["task_name"]: task["task_id"]
        for task in tasks
        if task.get("task_name") and task.get("task_id")
    }
    verified: list[dict[str, Any]] = []
    for result in results:
        task_id = task_ids.get(result.get("tool_name"))
        if not task_id:
            continue
        try:
            stored = json.loads(result.get("payload") or "")
        except (TypeError, json.JSONDecodeError):
            continue
        if (
            not isinstance(stored, dict)
            or stored.get("provenance") != _RESULT_PROVENANCE
            or stored.get("scan_id") != scan_id
            or stored.get("task_id") != task_id
        ):
            continue
        verified.append(
            {
                "scan_id": scan_id,
                "task_id": task_id,
                "tool_name": result["tool_name"],
                "status": result.get("status", "SUCCESS"),
                "payload": stored.get("result"),
            }
        )
    return verified


def task_result_status(task_status: str, result: Any) -> str:
    """Describe both Celery task completion and tool-level partial failures."""

    if task_status != "completed":
        return task_status.upper()
    if isinstance(result, dict):
        explicit = str(result.get("status", "")).lower()
        if explicit in {"unavailable", "timed_out", "skipped", "failed", "partial"}:
            return explicit.upper()
        if result.get("unavailable"):
            return "UNAVAILABLE"
        if result.get("timed_out"):
            return "TIMED_OUT"
        result_status = str(result.get("status", "")).upper()
        if result_status in {"FAILED", "PARTIAL"}:
            return result_status
        tools = result.get("tools")
        if isinstance(tools, list):
            failures = [item for item in tools if isinstance(item, dict) and not item.get("success", True)]
            if failures:
                return "PARTIAL" if len(failures) < len(tools) else "FAILED"
        if result.get("tool_errors"):
            return "PARTIAL"
        if result.get("finding_count", result.get("total_findings")) == 0:
            return "SUCCESS_NO_RESULTS"
        if result.get("findings") or result.get("total_findings", 0) > 0:
            return "SUCCESS_WITH_FINDINGS"
    return "SUCCESS"
