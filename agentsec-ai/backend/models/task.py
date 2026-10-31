"""Task model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.result import Result
    from backend.models.scan import Scan


class Task(Base, TimestampMixin, UUIDMixin):
    """Represents a Celery task execution for a scan."""

    __tablename__ = "tasks"

    task_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
    retries: Mapped[int] = mapped_column(default=0, nullable=False)
    execution_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        scan: Mapped[Scan]
        results: Mapped[list[Result]]
    else:
        scan = None
        results = None


__all__ = ["Task"]
