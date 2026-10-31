"""Endpoint model for AgentSec AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.scan import Scan
    from backend.models.subdomain import Subdomain


class Endpoint(Base, TimestampMixin, UUIDMixin):
    """HTTP endpoint discovered during enumeration."""

    __tablename__ = "endpoints"

    url: Mapped[str] = mapped_column(String(2000), index=True, nullable=False)
    method: Mapped[str] = mapped_column(String(20), default="GET", nullable=False)
    status_code: Mapped[int | None] = mapped_column(nullable=True)
    response_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    subdomain_id: Mapped[UUID] = mapped_column(ForeignKey("subdomains.id"), nullable=False)
    scan_id: Mapped[UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)

    if TYPE_CHECKING:
        subdomain: Mapped[Subdomain]
        scan: Mapped[Scan]
    else:
        subdomain = None
        scan = None


__all__ = ["Endpoint"]
