"""Scan model and supporting enums for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.domain import Domain
    from backend.models.finding import Finding
    from backend.models.organization import Organization
    from backend.models.result import Result
    from backend.models.subdomain import Subdomain
    from backend.models.task import Task
    from backend.models.user import User


class ScanType(str, Enum):
    FULL = "FULL"
    RECON_ONLY = "RECON_ONLY"
    VULN_ONLY = "VULN_ONLY"
    QUICK = "QUICK"
    DEEP_AI = "DEEP_AI"


class ScanMode(str, Enum):
    CLASSIC = "CLASSIC"
    HYBRID = "HYBRID"
    AUTONOMOUS = "AUTONOMOUS"


class ScanStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Scan(Base, TimestampMixin, UUIDMixin):
    """Represents an overall security scan workflow."""

    __tablename__ = "scans"

    target: Mapped[str] = mapped_column(String(255), nullable=False)
    scan_type: Mapped[ScanType] = mapped_column(SAEnum(ScanType, native_enum=False), nullable=False)
    status: Mapped[ScanStatus] = mapped_column(SAEnum(ScanStatus, native_enum=False), default=ScanStatus.PENDING, nullable=False)
    scan_mode: Mapped[ScanMode] = mapped_column(SAEnum(ScanMode, native_enum=False), default=ScanMode.CLASSIC, nullable=False)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_phase: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    strix_cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    strix_run_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    strix_status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    created_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    if TYPE_CHECKING:
        organization: Mapped[Organization]
        created_by: Mapped[User]
        domains: Mapped[list[Domain]]
        subdomains: Mapped[list[Subdomain]]
        findings: Mapped[list[Finding]]
        tasks: Mapped[list[Task]]
        results: Mapped[list[Result]]
    else:
        organization = None
        created_by = None
        domains = None
        subdomains = None
        findings = None
        tasks = None
        results = None


__all__ = ["Scan", "ScanMode", "ScanStatus", "ScanType"]
