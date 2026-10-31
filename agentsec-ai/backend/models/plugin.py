"""Plugin registry model for AgentSec AI."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin


class Plugin(Base, TimestampMixin, UUIDMixin):
    """Global plugin registry entry."""

    __tablename__ = "plugins"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)


__all__ = ["Plugin"]
