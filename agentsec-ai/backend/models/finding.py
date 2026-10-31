"""Finding model for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.endpoint import Endpoint
    from backend.models.host import Host
    from backend.models.scan import Scan
    from backend.models.subdomain import Subdomain


class FindingStatus(str, Enum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    FIXED = "FIXED"
    ACCEPTED_RISK = "ACCEPTED_RISK"


class Finding(Base, TimestampMixin, UUIDMixin):
    """Security finding emitted by a scan or agent."""

    __tablename__ = "findings"

    title: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="INFO", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[FindingStatus] = mapped_column(SAEnum(FindingStatus, native_enum=False), default=FindingStatus.NEW, nullable=False)
    vector: Mapped[str | None] = mapped_column(String(255), nullable=True)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)
    subdomain_id: Mapped[UUID | None] = mapped_column(ForeignKey("subdomains.id"), nullable=True)
    host_id: Mapped[UUID | None] = mapped_column(ForeignKey("hosts.id"), nullable=True)
    endpoint_id: Mapped[UUID | None] = mapped_column(ForeignKey("endpoints.id"), nullable=True)

    def __init__(self, **kwargs: object) -> None:
        """Apply the review defaults immediately as well as on database insert."""
        kwargs.setdefault("severity", "INFO")
        super().__init__(**kwargs)

    if TYPE_CHECKING:
        scan: Mapped[Scan]
        subdomain: Mapped[Subdomain | None]
        host: Mapped[Host | None]
        endpoint: Mapped[Endpoint | None]
    else:
        scan = None
        subdomain = None
        host = None
        endpoint = None


__all__ = ["Finding", "FindingStatus"]
