"""Result model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.scan import Scan
    from backend.models.task import Task


class Result(Base, TimestampMixin, UUIDMixin):
    """Tool result captured from an executed task."""

    __tablename__ = "results"

    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="SUCCESS", nullable=False)
    execution_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        task: Mapped[Task]
        scan: Mapped[Scan]
    else:
        task = None
        scan = None


__all__ = ["Result"]
