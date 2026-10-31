"""Service model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.port import Port
    from backend.models.scan import Scan


class Service(Base, TimestampMixin, UUIDMixin):
    """Service discovered on a port."""

    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    banner: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    vuln_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    port_id: Mapped[UUID] = mapped_column(ForeignKey("ports.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        port: Mapped[Port]
        scan: Mapped[Scan]
    else:
        port = None
        scan = None


__all__ = ["Service"]
