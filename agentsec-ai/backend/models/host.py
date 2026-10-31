"""Host model for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.finding import Finding
    from backend.models.port import Port
    from backend.models.scan import Scan
    from backend.models.subdomain import Subdomain
    from backend.models.technology import Technology


class HostState(str, Enum):
    NEW = "NEW"
    DISCOVERED = "DISCOVERED"
    VERIFIED = "VERIFIED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Host(Base, TimestampMixin, UUIDMixin):
    """Discovered network host."""

    __tablename__ = "hosts"

    ip_address: Mapped[str] = mapped_column(String(45), index=True, nullable=False)
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[HostState] = mapped_column(SAEnum(HostState, native_enum=False), default=HostState.NEW, nullable=False)
    subdomain_id: Mapped[UUID | None] = mapped_column(ForeignKey("subdomains.id"), nullable=True)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        subdomain: Mapped[Subdomain | None]
        scan: Mapped[Scan]
        ports: Mapped[list[Port]]
        technologies: Mapped[list[Technology]]
        findings: Mapped[list[Finding]]
    else:
        subdomain = None
        scan = None
        ports = None
        technologies = None
        findings = None


__all__ = ["Host", "HostState"]
