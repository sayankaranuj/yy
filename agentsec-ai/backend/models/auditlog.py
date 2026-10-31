"""AuditLog model for tracking sensitive actions in AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym

from .base import Base, TimestampMixin, UUIDMixin


class AuditActionType(str, Enum):
    STRIX_AUTHORIZED = "strix_authorized"
    STRIX_DENIED = "strix_denied"
    STRIX_STARTED = "strix_started"
    STRIX_COMPLETED = "strix_completed"
    STRIX_FAILED = "strix_failed"
    """Types of actions that are audited."""

    # STRIX-related actions

    # Scan decision actions
    SCAN_DECISION_MADE = "scan_decision_made"
    TOOL_SELECTED = "tool_selected"
    TOOL_SKIPPED = "tool_skipped"

    # Authorization/Gating
    AUTHORIZATION_REQUESTED = "authorization_requested"
    AUTHORIZATION_APPROVED = "authorization_approved"
    AUTHORIZATION_DENIED = "authorization_denied"

    # Finding validation
    FINDING_VALIDATED = "finding_validated"
    FINDING_REJECTED = "finding_rejected"
    FINDING_ESCALATED = "finding_escalated"

    # Scan lifecycle
    SCAN_STARTED = "scan_started"
    SCAN_PAUSED = "scan_paused"
    SCAN_RESUMED = "scan_resumed"
    SCAN_CANCELLED = "scan_cancelled"
    SCAN_COMPLETED = "scan_completed"


class AuditLog(Base, TimestampMixin, UUIDMixin):
    """
    Audit log entry for sensitive actions and decisions.
    Used for compliance, debugging, and AI reasoning visibility.
    """

    __tablename__ = "audit_logs"

    scan_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)

    actor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    """Who/what triggered this action: user ID, agent name, system."""

    actor_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="system"
    )
    """Type of actor: user, agent, system, strix."""

    resource_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    """Type of resource affected: scan, finding, tool, strix_run."""

    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    """ID of resource affected."""

    details: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True, default=None
    )
    """Structured details about the action."""

    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    """Human-readable reason for the action."""

    decision_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    """AI-generated rationale for decisions (for visibility)."""

    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata", JSON, nullable=True, default=None
    )
    """Additional metadata."""

    severity: Mapped[str] = mapped_column(
        String(20), nullable=False, default="info"
    )
    """Severity of the action: critical, high, medium, low, info."""

    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    """IP address of actor (if applicable)."""

    def __repr__(self) -> str:
        return f"<AuditLog id={self.id} scan_id={self.scan_id} action={self.action}>"


# ``metadata`` is the public API used by audit callers, but SQLAlchemy reserves
# that attribute name while scanning declarative model definitions.
AuditLog.metadata = synonym("metadata_")


__all__ = ["AuditLog", "AuditActionType"]
