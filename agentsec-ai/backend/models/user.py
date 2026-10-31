"""User and membership models for AgentSec AI."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin
from backend.models.organization import OrganizationPlan

if TYPE_CHECKING:
    from backend.models.organization import Organization
    from backend.models.scan import Scan


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


user_organization_membership = Table(
    "user_organization_membership",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
)


class User(Base, TimestampMixin, UUIDMixin):
    """Application user account."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.ANALYST, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    api_key: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    scan_quota: Mapped[int] = mapped_column(default=10, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    password_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(), nullable=False
    )

    if TYPE_CHECKING:
        organizations: Mapped[list[Organization]]
        scans: Mapped[list[Scan]]
    else:
        organizations = None
        scans = None


class RefreshSession(Base, TimestampMixin, UUIDMixin):
    """Rotating refresh-token session with revocation metadata."""

    __tablename__ = "refresh_sessions"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    replaced_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)


__all__ = ["User", "UserRole", "RefreshSession", "user_organization_membership", "OrganizationPlan"]
