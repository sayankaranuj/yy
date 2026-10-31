"""Integer-keyed persistence models for the active API surface.

These records intentionally do not reuse the UUID-based domain models.  The
active API has historically exposed integer identifiers and must keep doing so.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin


class ActiveScan(Base, TimestampMixin):
    __tablename__ = "active_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued")
    selected_attack_categories: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    git_options: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class ApprovedTarget(Base, TimestampMixin):
    """Administrator-managed target allowlist entry."""

    __tablename__ = "approved_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    approved_by: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ownership_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ActiveFinding(Base, TimestampMixin):
    __tablename__ = "active_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    scan_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    affected_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence: Mapped[dict[str, Any] | list[Any] | str | None] = mapped_column(JSON, nullable=True)
    source_tool: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence: Mapped[float | None] = mapped_column(nullable=True)
    asset: Mapped[str | None] = mapped_column(Text, nullable=True)
    parameter: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remediation: Mapped[str | None] = mapped_column(Text, nullable=True)
    cwe: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owasp_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    verification_state: Mapped[str] = mapped_column(String(30), nullable=False, default="unverified")
    analyst_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignee: Mapped[str | None] = mapped_column(String(255), nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    risk_acceptance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dedup_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)


class AuthorizationRequestRecord(Base, TimestampMixin):
    __tablename__ = "authorization_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False, default="operator")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ActiveWorkflow(Base, TimestampMixin):
    __tablename__ = "active_workflows"

    scan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("active_scans.id", ondelete="CASCADE"), primary_key=True
    )
    target: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued")


class ActiveWorkflowTask(Base):
    __tablename__ = "active_workflow_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_scan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("active_workflows.scan_id", ondelete="CASCADE"), nullable=False
    )
    task_id: Mapped[str] = mapped_column(String(255), nullable=False)
    task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    retries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    exit_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    worker_hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    __table_args__ = (UniqueConstraint("workflow_scan_id", "task_id", name="uq_workflow_task_scan_task"),)


class ActiveWorkflowTaskAttempt(Base):
    """Durable lifecycle record for each execution of a workflow task."""

    __tablename__ = "active_workflow_task_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("active_workflow_tasks.id", ondelete="CASCADE"), nullable=False
    )
    workflow_scan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("active_workflows.scan_id", ondelete="CASCADE"), nullable=False, index=True
    )
    task_id: Mapped[str] = mapped_column(String(255), nullable=False)
    task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running")
    queue: Mapped[str | None] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    recovered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dead_lettered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dead_letter_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempt_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "workflow_task_id", "attempt_number", name="uq_workflow_task_attempt_number"
        ),
    )


class ActiveWorkflowResult(Base):
    __tablename__ = "active_workflow_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_scan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("active_workflows.scan_id", ondelete="CASCADE"), nullable=False
    )
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    command_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    __table_args__ = (UniqueConstraint("workflow_scan_id", "tool_name", name="uq_workflow_result_scan_tool"),)


__all__ = [
    "ActiveFinding",
    "ActiveScan",
    "ApprovedTarget",
    "ActiveWorkflow",
    "ActiveWorkflowResult",
    "ActiveWorkflowTask",
    "ActiveWorkflowTaskAttempt",
    "AuthorizationRequestRecord",
]
