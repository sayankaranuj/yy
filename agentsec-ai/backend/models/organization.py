"""Organization model definitions for AgentSec AI."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from backend.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from backend.models.domain import Domain
    from backend.models.scan import Scan
    from backend.models.user import User

class OrganizationPlan(str, Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"


class Organization(Base, TimestampMixin, UUIDMixin):
    """Customer or workspace organization."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    plan: Mapped[OrganizationPlan] = mapped_column(default=OrganizationPlan.FREE, nullable=False)
    max_scans: Mapped[int] = mapped_column(default=5, nullable=False)
    max_targets: Mapped[int] = mapped_column(default=10, nullable=False)
    authorized_scope_confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    scope_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scope_confirmed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scope_confirmation_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)

    if TYPE_CHECKING:
        members: Mapped[list[User]]
        domains: Mapped[list[Domain]]
        scans: Mapped[list[Scan]]
    else:
        members = None
        domains = None
        scans = None


__all__ = ["Organization", "OrganizationPlan"]
