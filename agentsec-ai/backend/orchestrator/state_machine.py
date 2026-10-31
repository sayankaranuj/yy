"""State machine for domain, subdomain, and host lifecycle transitions."""

from __future__ import annotations

from enum import Enum

from backend.models.domain import DomainState
from backend.models.subdomain import SubdomainState
from backend.models.host import HostState


class InvalidStateTransitionError(Exception):
    """Raised when an asset tries to transition to an invalid state."""


class AssetType(str, Enum):
    DOMAIN = "DOMAIN"
    SUBDOMAIN = "SUBDOMAIN"
    HOST = "HOST"
    ENDPOINT = "ENDPOINT"


class StateMachine:
    """Enforces forward-only lifecycle transitions for security assets."""

    VALID_TRANSITIONS = {
        DomainState.NEW: [DomainState.DISCOVERED],
        DomainState.DISCOVERED: [DomainState.VERIFIED],
        DomainState.VERIFIED: [DomainState.ANALYZED],
        DomainState.ANALYZED: [DomainState.SCANNED],
        DomainState.SCANNED: [DomainState.REPORTED],
        DomainState.REPORTED: [DomainState.ARCHIVED],
        SubdomainState.NEW: [SubdomainState.DISCOVERED],
        SubdomainState.DISCOVERED: [SubdomainState.VERIFIED],
        SubdomainState.VERIFIED: [SubdomainState.ANALYZED],
        SubdomainState.ANALYZED: [SubdomainState.SCANNED],
        SubdomainState.SCANNED: [SubdomainState.REPORTED],
        SubdomainState.REPORTED: [SubdomainState.ARCHIVED],
        HostState.NEW: [HostState.DISCOVERED],
        HostState.DISCOVERED: [HostState.VERIFIED],
        HostState.VERIFIED: [HostState.ACTIVE],
        HostState.ACTIVE: [HostState.INACTIVE],
        HostState.INACTIVE: [HostState.INACTIVE],
    }

    async def transition(self, asset: object, new_state: object, db_session: object) -> None:
        current_state = getattr(asset, "state", None)
        if current_state is None:
            raise InvalidStateTransitionError("Asset does not expose a state attribute")
        allowed_states = self.VALID_TRANSITIONS.get(current_state, [])
        if new_state == current_state:
            return
        if new_state == "ARCHIVED" or new_state == DomainState.ARCHIVED or new_state == SubdomainState.ARCHIVED or new_state == HostState.INACTIVE:
            setattr(asset, "state", new_state)
            return
        if new_state in allowed_states:
            setattr(asset, "state", new_state)
            return
        raise InvalidStateTransitionError(f"Invalid transition from {current_state} to {new_state}")


__all__ = ["AssetType", "InvalidStateTransitionError", "StateMachine"]
