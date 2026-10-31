"""Plugin package exports for AgentSec AI."""

from .registry import registry  # exposes the singleton registry

__all__ = ["registry"]