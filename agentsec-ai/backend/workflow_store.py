"""Persistent workflow storage for AgentSec AI."""

from __future__ import annotations

import json
import asyncio
import threading
from pathlib import Path
from typing import Any

from sqlalchemy import select

from backend.config.settings import settings
from backend.config.database import AsyncSessionFactory
from backend.models.active_api import ActiveWorkflow
from backend.repositories import ActiveApiRepository
from backend.workflow_results import encode_task_result, task_result_status, verified_workflow_results


_store_lock = threading.RLock()


class WorkflowStore:
    """Persist workflow tasks and results in a local JSON file."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(file_path or Path(__file__).resolve().parent / "workflow_store.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write({"workflows": []})

    def _read(self) -> dict[str, Any]:
        with _store_lock:
            try:
                return json.loads(self.file_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {"workflows": []}

    def _write(self, payload: dict[str, Any]) -> None:
        temporary_path = self.file_path.with_suffix(f"{self.file_path.suffix}.tmp")
        with _store_lock:
            temporary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            temporary_path.replace(self.file_path)

    def upsert_workflow(self, scan_id: int, workflow: dict[str, Any]) -> dict[str, Any]:
        """Persist workflow state and transform it into task/result payloads."""

        if settings.storage_backend.lower() == "postgres":
            return asyncio.run(self.upsert_workflow_async(scan_id, workflow))

        with _store_lock:
            payload = self._read()
            tasks = [
                {
                    "task_id": step.get("task_id") or f"task-{index}",
                    "task_name": step["name"],
                    "status": step["status"],
                    "retries": 0,
                }
                for index, step in enumerate(workflow.get("steps", []), start=1)
            ]
            record = {
                "scan_id": scan_id,
                "target": workflow.get("target", ""),
                "status": workflow.get("status", "queued"),
                "tasks": tasks,
                "results": [],
            }
            payload.setdefault("workflows", [])
            existing = [item for item in payload["workflows"] if item.get("scan_id") != scan_id]
            existing.append(record)
            payload["workflows"] = existing
            self._write(payload)
            return record

    async def upsert_workflow_async(self, scan_id: int, workflow: dict[str, Any]) -> dict[str, Any]:
        """Persist workflow state using the PostgreSQL repository."""

        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).upsert_workflow(scan_id, workflow)

    def get_latest_state(self) -> dict[str, Any] | None:
        """Return the latest workflow state if one exists."""

        if settings.storage_backend.lower() == "postgres":
            return asyncio.run(self.get_latest_state_async())

        payload = self._read()
        workflows = payload.get("workflows", [])
        return workflows[-1] if workflows else None

    async def get_latest_state_async(self) -> dict[str, Any] | None:
        async with AsyncSessionFactory() as session:
            row = (
                await session.execute(
                    select(ActiveWorkflow.scan_id).order_by(ActiveWorkflow.scan_id.desc()).limit(1)
                )
            ).scalar_one_or_none()
            return await ActiveApiRepository(session).get_workflow(row) if row else None

    def get_state(self, scan_id: int) -> dict[str, Any] | None:
        """Return one workflow from the JSON fallback store."""

        return next(
            (item for item in self._read().get("workflows", []) if item.get("scan_id") == scan_id),
            None,
        )

    def get_results(self, scan_id: int) -> list[dict[str, Any]]:
        """Return verified worker results belonging to one scan."""

        if settings.storage_backend.lower() == "postgres":
            return asyncio.run(self.get_results_async(scan_id))
        workflow = self.get_state(scan_id)
        if workflow is None:
            return []
        return verified_workflow_results(
            scan_id,
            workflow.get("tasks", []),
            workflow.get("results", []),
        )

    async def get_results_async(self, scan_id: int) -> list[dict[str, Any]]:
        workflow = await self.get_state_async(scan_id)
        if workflow is None:
            return []
        return verified_workflow_results(
            scan_id,
            workflow.get("tasks", []),
            workflow.get("results", []),
        )

    def update_task(
        self,
        scan_id: int,
        task_name: str,
        task_id: str,
        status: str,
        result: Any = None,
    ) -> None:
        """Update task progress in the JSON fallback store."""

        with _store_lock:
            payload = self._read()
            workflow = next(
                (item for item in payload.get("workflows", []) if item.get("scan_id") == scan_id),
                None,
            )
            if workflow is None:
                return

            task = next(
                (item for item in workflow.get("tasks", []) if item.get("task_name") == task_name),
                None,
            )
            if task is None:
                task = {
                    "task_id": task_id,
                    "task_name": task_name,
                    "status": status,
                    "retries": 0,
                }
                workflow.setdefault("tasks", []).append(task)
            else:
                task.update({"task_id": task_id, "status": status})

            if result is not None:
                existing_result = next(
                    (
                        item
                        for item in workflow.setdefault("results", [])
                        if item.get("tool_name") == task_name
                    ),
                    None,
                )
                if existing_result is None:
                    workflow["results"].append(
                        {
                            "tool_name": task_name,
                            "payload": encode_task_result(scan_id, task_id, result),
                            "status": task_result_status(status, result),
                        }
                    )
                else:
                    existing_result.update(
                        {
                            "payload": encode_task_result(scan_id, task_id, result),
                            "status": task_result_status(status, result),
                        }
                    )

            statuses = {item.get("status") for item in workflow.get("tasks", [])}
            if workflow.get("status") in {"cancel_requested", "cancelled"}:
                workflow["status"] = "cancelled"
            elif "failed" in statuses:
                workflow["status"] = "failed"
            elif statuses and statuses.issubset({"completed"}):
                workflow["status"] = "completed"
            else:
                workflow["status"] = "running"

            self._write(payload)

    async def get_state_async(self, scan_id: int) -> dict[str, Any] | None:
        """Return one workflow from PostgreSQL."""

        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).get_workflow(scan_id)

    async def set_status_async(self, scan_id: int, status: str) -> dict[str, Any] | None:
        """Update workflow status without replacing tasks or results."""

        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).set_workflow_status(scan_id, status)

    def set_status(self, scan_id: int, status: str) -> dict[str, Any] | None:
        """Update workflow status in the JSON fallback store."""

        with _store_lock:
            payload = self._read()
            workflow = next(
                (item for item in payload.get("workflows", []) if item.get("scan_id") == scan_id),
                None,
            )
            if workflow is None:
                return None
            workflow["status"] = status
            self._write(payload)
            return workflow
