"""Technology model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.host import Host
    from backend.models.scan import Scan
    from backend.models.subdomain import Subdomain


class Technology(Base, TimestampMixin, UUIDMixin):
    """Technology fingerprint discovered on a host or subdomain."""

    __tablename__ = "technologies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cve_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    host_id: Mapped[UUID] = mapped_column(ForeignKey("hosts.id"), nullable=False)
    subdomain_id: Mapped[UUID | None] = mapped_column(ForeignKey("subdomains.id"), nullable=True)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        host: Mapped[Host]
        subdomain: Mapped[Subdomain | None]
        scan: Mapped[Scan]
    else:
        host = None
        subdomain = None
        scan = None


__all__ = ["Technology"]
