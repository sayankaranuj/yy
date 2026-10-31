"""Subdomain model for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.domain import Domain
    from backend.models.host import Host
    from backend.models.finding import Finding
    from backend.models.scan import Scan


class SubdomainState(str, Enum):
    NEW = "NEW"
    DISCOVERED = "DISCOVERED"
    VERIFIED = "VERIFIED"
    ANALYZED = "ANALYZED"
    SCANNED = "SCANNED"
    REPORTED = "REPORTED"
    ARCHIVED = "ARCHIVED"


class Subdomain(Base, TimestampMixin, UUIDMixin):
    """Subdomain discovered under a domain."""

    __tablename__ = "subdomains"

    name: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    state: Mapped[SubdomainState] = mapped_column(SAEnum(SubdomainState, native_enum=False), default=SubdomainState.NEW, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    domain_id: Mapped[UUID] = mapped_column(ForeignKey("domains.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        domain: Mapped[Domain]
        scan: Mapped[Scan]
        hosts: Mapped[list[Host]]
        findings: Mapped[list[Finding]]
    else:
        domain = None
        scan = None
        hosts = None
        findings = None


__all__ = ["Subdomain", "SubdomainState"]
