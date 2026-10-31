"""Domain model for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.organization import Organization
    from backend.models.scan import Scan
    from backend.models.subdomain import Subdomain


class DomainState(str, Enum):
    NEW = "NEW"
    DISCOVERED = "DISCOVERED"
    VERIFIED = "VERIFIED"
    ANALYZED = "ANALYZED"
    SCANNED = "SCANNED"
    REPORTED = "REPORTED"
    ARCHIVED = "ARCHIVED"


class Domain(Base, TimestampMixin, UUIDMixin):
    """Discovered target domain."""

    __tablename__ = "domains"

    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    state: Mapped[DomainState] = mapped_column(SAEnum(DomainState, native_enum=False), default=DomainState.NEW, nullable=False)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        organization: Mapped[Organization]
        scan: Mapped[Scan]
        subdomains: Mapped[list[Subdomain]]
    else:
        organization = None
        scan = None
        subdomains = None


__all__ = ["Domain", "DomainState"]
