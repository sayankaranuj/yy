"""Async repositories for the integer-keyed active API records."""

from __future__ import annotations

from typing import Any
from datetime import datetime, timezone
import hashlib

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.active_api import (
    ActiveFinding,
    ActiveScan,
    ActiveWorkflow,
    ActiveWorkflowResult,
    ActiveWorkflowTask,
    ActiveWorkflowTaskAttempt,
    AuthorizationRequestRecord,
    ApprovedTarget,
)
from backend.workflow_results import encode_task_result, task_result_status


class ActiveApiRepository:
    """Persist active API and workflow records in PostgreSQL."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_scans(self) -> list[dict[str, Any]]:
        rows = (await self.session.scalars(select(ActiveScan).order_by(ActiveScan.id))).all()
        return [self._scan(row) for row in rows]

    async def get_scan(self, scan_id: int) -> dict[str, Any] | None:
        row = await self.session.get(ActiveScan, scan_id)
        return self._scan(row) if row else None

    async def list_approved_targets(self) -> list[dict[str, Any]]:
        rows = (
            await self.session.scalars(
                select(ApprovedTarget).where(ApprovedTarget.enabled.is_(True)).order_by(ApprovedTarget.target)
            )
        ).all()
        return [self._approved_target(row) for row in rows]

    async def approve_target(
        self, target: str, approved_by: str, reason: str, ownership_verified: bool = True
    ) -> dict[str, Any]:
        row = await self.session.scalar(select(ApprovedTarget).where(ApprovedTarget.target == target))
        if row is None:
            row = ApprovedTarget(
                target=target,
                approved_by=approved_by,
                reason=reason,
                enabled=True,
                ownership_verified=ownership_verified,
            )
            self.session.add(row)
        else:
            row.approved_by = approved_by
            row.reason = reason
            row.enabled = True
            row.ownership_verified = ownership_verified
        await self.session.commit()
        await self.session.refresh(row)
        return self._approved_target(row)

    async def revoke_target(self, target: str) -> bool:
        row = await self.session.scalar(select(ApprovedTarget).where(ApprovedTarget.target == target))
        if row is None:
            return False
        row.enabled = False
        await self.session.commit()
        return True

    async def is_target_approved(self, target: str) -> bool:
        return bool(
            await self.session.scalar(
                select(ApprovedTarget.id).where(
                    ApprovedTarget.target == target,
                    ApprovedTarget.enabled.is_(True),
                )
            )
        )

    async def create_scan(
        self,
        name: str,
        target: str,
        status: str = "queued",
        selected_attack_categories: list[str] | None = None,
        git_options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        row = ActiveScan(
            name=name,
            target=target,
            status=status,
            selected_attack_categories=selected_attack_categories,
            git_options=git_options,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return self._scan(row)

    async def update_scan_status(self, scan_id: int, status: str) -> dict[str, Any] | None:
        row = await self.session.get(ActiveScan, scan_id)
        if row is None:
            return None
        row.status = status
        await self.session.commit()
        return self._scan(row)

    async def set_workflow_status(self, scan_id: int, status: str) -> dict[str, Any] | None:
        """Update the authoritative workflow and scan aggregate status."""

        workflow = await self.session.get(ActiveWorkflow, scan_id)
        if workflow is None:
            return None
        workflow.status = status
        scan = await self.session.get(ActiveScan, scan_id)
        if scan is not None:
            scan.status = status
        await self.session.commit()
        return await self.get_workflow(scan_id)

    async def list_findings(self) -> list[dict[str, Any]]:
        rows = (await self.session.scalars(select(ActiveFinding).order_by(ActiveFinding.id))).all()
        return [self._finding(row) for row in rows]

    async def create_finding(
        self,
        title: str,
        severity: str,
        status: str = "open",
        scan_id: int | None = None,
        task_id: str | None = None,
        affected_url: str | None = None,
        description: str | None = None,
        evidence: Any = None,
        source_tool: str | None = None,
        category: str | None = None,
        confidence: float | None = None,
        asset: str | None = None,
        parameter: str | None = None,
        remediation: str | None = None,
        cwe: str | None = None,
        owasp_category: str | None = None,
        verification_state: str = "unverified",
        analyst_notes: str | None = None,
        assignee: str | None = None,
        due_date: datetime | None = None,
        risk_acceptance: bool = False,
    ) -> dict[str, Any]:
        """Persist a finding from a completed scanner result."""

        dedup_key = self.finding_dedup_key(
            title=title, source_tool=source_tool, category=category,
            asset=asset or affected_url, parameter=parameter,
        )
        row = await self.session.scalar(select(ActiveFinding).where(ActiveFinding.dedup_key == dedup_key))
        if row is not None:
            return self._finding(row)
        row = ActiveFinding(
            title=title,
            severity=severity,
            status=status,
            scan_id=scan_id,
            task_id=task_id,
            affected_url=affected_url,
            description=description,
            evidence=evidence,
            source_tool=source_tool, category=category, confidence=confidence,
            asset=asset or affected_url, parameter=parameter, remediation=remediation,
            cwe=cwe, owasp_category=owasp_category, verification_state=verification_state,
            analyst_notes=analyst_notes, assignee=assignee, due_date=due_date,
            risk_acceptance=risk_acceptance, dedup_key=dedup_key,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return self._finding(row)

    @staticmethod
    def finding_dedup_key(
        *, title: str, source_tool: str | None, category: str | None,
        asset: str | None, parameter: str | None,
    ) -> str:
        """Return a stable key for scanner repeats regardless of casing/spacing."""
        values = [title, source_tool, category, asset, parameter]
        canonical = "\x1f".join(" ".join((value or "").strip().lower().split()) for value in values)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    async def update_finding(self, finding_id: int, **changes: Any) -> dict[str, Any] | None:
        row = await self.session.get(ActiveFinding, finding_id)
        if row is None:
            return None
        allowed = {
            "title", "severity", "status", "description", "evidence", "source_tool",
            "category", "confidence", "asset", "parameter", "remediation", "cwe",
            "owasp_category", "verification_state", "analyst_notes", "assignee",
            "due_date", "risk_acceptance",
        }
        for key, value in changes.items():
            if key in allowed:
                setattr(row, key, value)
        await self.session.commit()
        await self.session.refresh(row)
        return self._finding(row)

    async def get_finding(self, finding_id: int) -> dict[str, Any] | None:
        row = await self.session.get(ActiveFinding, finding_id)
        return self._finding(row) if row else None

    async def list_authorization_requests(self) -> list[dict[str, Any]]:
        rows = (
            await self.session.scalars(
                select(AuthorizationRequestRecord).order_by(AuthorizationRequestRecord.id.desc())
            )
        ).all()
        return [self._authorization_request(row) for row in rows]

    async def create_authorization_request(
        self, target: str, reason: str, requested_by: str
    ) -> dict[str, Any]:
        row = AuthorizationRequestRecord(
            target=target,
            reason=reason,
            requested_by=requested_by,
            status="pending",
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return self._authorization_request(row)

    async def review_authorization_request(
        self, request_id: int, decision: str, reviewed_by: str, review_note: str
    ) -> dict[str, Any] | None:
        row = await self.session.get(AuthorizationRequestRecord, request_id)
        if row is None or row.status != "pending":
            return None
        if decision == "approve":
            target = await self.session.scalar(
                select(ApprovedTarget).where(ApprovedTarget.target == row.target)
            )
            if target is None:
                self.session.add(
                    ApprovedTarget(
                        target=row.target,
                        approved_by=reviewed_by,
                        reason=review_note or row.reason,
                        enabled=True,
                        ownership_verified=False,
                    )
                )
            else:
                target.approved_by = reviewed_by
                target.reason = review_note or row.reason
                target.enabled = True
                target.ownership_verified = False
        row.status = "approved" if decision == "approve" else "rejected"
        row.reviewed_by = reviewed_by
        row.review_note = review_note
        from datetime import datetime, timezone

        row.reviewed_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(row)
        return self._authorization_request(row)

    async def upsert_workflow(self, scan_id: int, workflow: dict[str, Any]) -> dict[str, Any]:
        row = await self.session.get(ActiveWorkflow, scan_id)
        if row is None:
            row = ActiveWorkflow(scan_id=scan_id)
            self.session.add(row)
        row.target = workflow.get("target", "")
        row.status = workflow.get("status", "queued")
        await self.session.flush()
        await self.session.execute(
            delete(ActiveWorkflowTask).where(ActiveWorkflowTask.workflow_scan_id == scan_id)
        )
        await self.session.execute(
            delete(ActiveWorkflowResult).where(ActiveWorkflowResult.workflow_scan_id == scan_id)
        )
        steps = workflow.get("steps", [])
        self.session.add_all(
            [
                ActiveWorkflowTask(
                    workflow_scan_id=scan_id,
                    task_id=step.get("task_id") or f"task-{index}",
                    task_name=step["name"],
                    status=step["status"],
                    retries=0,
                )
                for index, step in enumerate(steps, start=1)
            ]
        )
        await self.session.commit()
        return await self.get_workflow(scan_id) or {}

    async def get_workflow(self, scan_id: int) -> dict[str, Any] | None:
        workflow = await self.session.get(ActiveWorkflow, scan_id)
        if workflow is None:
            return None
        tasks = (
            await self.session.scalars(
                select(ActiveWorkflowTask)
                .where(ActiveWorkflowTask.workflow_scan_id == scan_id)
                .order_by(ActiveWorkflowTask.id)
            )
        ).all()
        results = (
            await self.session.scalars(
                select(ActiveWorkflowResult)
                .where(ActiveWorkflowResult.workflow_scan_id == scan_id)
                .order_by(ActiveWorkflowResult.id)
            )
        ).all()
        task_ids = {task.task_name: task.task_id for task in tasks}
        return {
            "scan_id": workflow.scan_id,
            "target": workflow.target,
            "status": workflow.status,
            "tasks": [
                {
                    "task_id": x.task_id,
                    "task_name": x.task_name,
                    "status": x.status,
                    "retries": x.retries,
                    "started_at": x.started_at.isoformat() if x.started_at else None,
                    "completed_at": x.completed_at.isoformat() if x.completed_at else None,
                    "duration_ms": x.duration_ms,
                    "exit_code": x.exit_code,
                    "worker_hostname": x.worker_hostname,
                }
                for x in tasks
            ],
            "results": [
                {
                    "tool_name": x.tool_name,
                    "task_id": task_ids.get(x.tool_name),
                    "payload": x.payload,
                    "status": x.status,
                }
                for x in results
            ],
        }

    async def update_workflow_task(
        self,
        scan_id: int,
        task_name: str,
        task_id: str,
        status: str,
        result: Any = None,
    ) -> None:
        """Update a task row and derive aggregate workflow status."""

        workflow = await self.session.get(ActiveWorkflow, scan_id)
        if workflow is None:
            return
        task = (
            await self.session.scalars(
                select(ActiveWorkflowTask)
                .where(
                    ActiveWorkflowTask.workflow_scan_id == scan_id,
                    ActiveWorkflowTask.task_name == task_name,
                )
                .order_by(ActiveWorkflowTask.id)
            )
        ).first()
        if task is None:
            task = ActiveWorkflowTask(
                workflow_scan_id=scan_id,
                task_id=task_id,
                task_name=task_name,
                status=status,
                retries=0,
            )
            self.session.add(task)
            await self.session.flush()
        else:
            task.task_id = task_id
            task.status = status
        now = datetime.now(timezone.utc)
        attempt = (
            await self.session.scalars(
                select(ActiveWorkflowTaskAttempt)
                .where(
                    ActiveWorkflowTaskAttempt.workflow_scan_id == scan_id,
                    ActiveWorkflowTaskAttempt.task_id == task_id,
                    ActiveWorkflowTaskAttempt.status.in_(("running", "retrying")),
                )
                .order_by(ActiveWorkflowTaskAttempt.attempt_number.desc())
            )
        ).first()
        if status == "running" and attempt is None:
            previous = await self.session.scalar(
                select(ActiveWorkflowTaskAttempt.attempt_number)
                .where(ActiveWorkflowTaskAttempt.workflow_task_id == task.id)
                .order_by(ActiveWorkflowTaskAttempt.attempt_number.desc())
                .limit(1)
            )
            attempt = ActiveWorkflowTaskAttempt(
                workflow_task_id=task.id,
                workflow_scan_id=scan_id,
                task_id=task_id,
                task_name=task_name,
                attempt_number=(previous or 0) + 1,
                status="running",
                started_at=now,
                heartbeat_at=now,
            )
            self.session.add(attempt)
        elif attempt is not None:
            attempt.heartbeat_at = now
            if status in {"completed", "failed", "cancelled"}:
                attempt.status = status
                attempt.completed_at = now
        if status == "running" and task.started_at is None:
            task.started_at = now
        if status in {"completed", "failed", "cancelled"}:
            task.completed_at = now
            if task.started_at is not None:
                task.duration_ms = max(0, int((now - task.started_at).total_seconds() * 1000))
        if result is not None:
            existing_result = (
                await self.session.scalars(
                    select(ActiveWorkflowResult)
                    .where(
                        ActiveWorkflowResult.workflow_scan_id == scan_id,
                        ActiveWorkflowResult.tool_name == task_name,
                    )
                    .order_by(ActiveWorkflowResult.id)
                )
            ).first()
            result_status = task_result_status(status, result)
            if existing_result is None:
                self.session.add(
                    ActiveWorkflowResult(
                        workflow_scan_id=scan_id,
                        tool_name=task_name,
                        payload=encode_task_result(scan_id, task_id, result),
                        status=result_status,
                        task_id=task_id,
                    )
                )
            else:
                existing_result.payload = encode_task_result(scan_id, task_id, result)
                existing_result.status = result_status
                existing_result.task_id = task_id
        tasks = (
            await self.session.scalars(
                select(ActiveWorkflowTask).where(
                    ActiveWorkflowTask.workflow_scan_id == scan_id
                )
            )
        ).all()
        statuses = {item.status for item in tasks}
        if workflow.status in {"cancel_requested", "cancelled"}:
            workflow.status = "cancelled"
        elif "failed" in statuses:
            workflow.status = "failed"
        elif tasks and all(item.status == "completed" for item in tasks):
            workflow.status = "completed"
        else:
            workflow.status = "running"
        scan = await self.session.get(ActiveScan, scan_id)
        if scan is not None:
            scan.status = workflow.status
        await self.session.commit()

    async def list_stale_task_attempts(
        self, cutoff: datetime, scan_id: int | None = None
    ) -> list[dict[str, Any]]:
        """Return running attempts whose heartbeat is older than ``cutoff``."""

        query = select(ActiveWorkflowTaskAttempt).where(
            ActiveWorkflowTaskAttempt.status.in_(("running", "retrying")),
            ActiveWorkflowTaskAttempt.heartbeat_at < cutoff,
        )
        if scan_id is not None:
            query = query.where(ActiveWorkflowTaskAttempt.workflow_scan_id == scan_id)
        rows = (await self.session.scalars(query.order_by(ActiveWorkflowTaskAttempt.id))).all()
        return [self._task_attempt(row) for row in rows]

    async def recover_task_attempt(
        self,
        attempt_id: int,
        *,
        dead_letter: bool,
        reason: str,
        queue: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Mark a stale attempt as retrying or dead-lettered atomically."""

        row = await self.session.get(ActiveWorkflowTaskAttempt, attempt_id)
        if row is None or row.status not in {"running", "retrying"}:
            return None
        now = datetime.now(timezone.utc)
        row.status = "dead_lettered" if dead_letter else "retrying"
        row.dead_lettered = dead_letter
        row.dead_letter_reason = reason if dead_letter else None
        row.recovered_at = now
        row.completed_at = now if dead_letter else None
        row.heartbeat_at = now
        if queue is not None:
            row.queue = queue
        if metadata is not None:
            row.attempt_metadata = metadata
        await self.session.commit()
        return self._task_attempt(row)

    async def record_task_attempt(
        self,
        scan_id: int,
        task_name: str,
        task_id: str,
        *,
        status: str = "running",
        queue: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Create an attempt explicitly for workers that do not use lifecycle signals."""

        task = (
            await self.session.scalars(
                select(ActiveWorkflowTask)
                .where(
                    ActiveWorkflowTask.workflow_scan_id == scan_id,
                    ActiveWorkflowTask.task_id == task_id,
                )
            )
        ).first()
        if task is None:
            return None
        previous = await self.session.scalar(
            select(ActiveWorkflowTaskAttempt.attempt_number)
            .where(ActiveWorkflowTaskAttempt.workflow_task_id == task.id)
            .order_by(ActiveWorkflowTaskAttempt.attempt_number.desc())
            .limit(1)
        )
        now = datetime.now(timezone.utc)
        row = ActiveWorkflowTaskAttempt(
            workflow_task_id=task.id,
            workflow_scan_id=scan_id,
            task_id=task_id,
            task_name=task_name,
            attempt_number=(previous or 0) + 1,
            status=status,
            queue=queue,
            started_at=now,
            heartbeat_at=now,
            attempt_metadata=metadata,
        )
        self.session.add(row)
        await self.session.commit()
        return self._task_attempt(row)

    @staticmethod
    def _task_attempt(row: ActiveWorkflowTaskAttempt) -> dict[str, Any]:
        return {
            "id": row.id,
            "workflow_task_id": row.workflow_task_id,
            "workflow_scan_id": row.workflow_scan_id,
            "task_id": row.task_id,
            "task_name": row.task_name,
            "attempt_number": row.attempt_number,
            "status": row.status,
            "queue": row.queue,
            "started_at": row.started_at.isoformat(),
            "heartbeat_at": row.heartbeat_at.isoformat(),
            "completed_at": row.completed_at.isoformat() if row.completed_at else None,
            "recovered_at": row.recovered_at.isoformat() if row.recovered_at else None,
            "dead_lettered": row.dead_lettered,
            "dead_letter_reason": row.dead_letter_reason,
            "metadata": row.attempt_metadata,
        }

    @staticmethod
    def _scan(row: ActiveScan) -> dict[str, Any]:
        return {
            "id": row.id,
            "name": row.name,
            "target": row.target,
            "status": row.status,
            "selected_attack_categories": row.selected_attack_categories,
            "git_options": row.git_options,
        }

    @staticmethod
    def _approved_target(row: ApprovedTarget) -> dict[str, Any]:
        return {
            "id": row.id,
            "target": row.target,
            "approved_by": row.approved_by,
            "reason": row.reason,
            "enabled": row.enabled,
            "ownership_verified": row.ownership_verified,
        }

    @staticmethod
    def _finding(row: ActiveFinding) -> dict[str, Any]:
        return {
            "id": row.id,
            "title": row.title,
            "severity": row.severity,
            "status": row.status,
            "scan_id": row.scan_id,
            "task_id": row.task_id,
            "affected_url": row.affected_url,
            "description": row.description,
            "evidence": row.evidence,
            "source_tool": row.source_tool,
            "category": row.category,
            "confidence": row.confidence,
            "asset": row.asset,
            "parameter": row.parameter,
            "remediation": row.remediation,
            "cwe": row.cwe,
            "owasp_category": row.owasp_category,
            "verification_state": row.verification_state,
            "analyst_notes": row.analyst_notes,
            "assignee": row.assignee,
            "due_date": row.due_date.isoformat() if row.due_date else None,
            "risk_acceptance": row.risk_acceptance,
            "dedup_key": row.dedup_key,
        }

    @staticmethod
    def _authorization_request(row: AuthorizationRequestRecord) -> dict[str, Any]:
        return {
            "id": row.id,
            "target": row.target,
            "reason": row.reason,
            "requested_by": row.requested_by,
            "status": row.status,
            "reviewed_by": row.reviewed_by,
            "review_note": row.review_note,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "reviewed_at": row.reviewed_at.isoformat() if row.reviewed_at else None,
        }
