"""Port model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.host import Host
    from backend.models.scan import Scan
    from backend.models.service import Service


class Port(Base, TimestampMixin, UUIDMixin):
    """Open or closed network port."""

    __tablename__ = "ports"

    number: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    protocol: Mapped[str] = mapped_column(String(10), default="tcp", nullable=False)
    state: Mapped[str] = mapped_column(String(20), default="open", nullable=False)
    service_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    https_accessible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    host_id: Mapped[UUID] = mapped_column(ForeignKey("hosts.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        host: Mapped[Host]
        scan: Mapped[Scan]
        services: Mapped[list[Service]]
    else:
        host = None
        scan = None
        services = None


__all__ = ["Port"]
