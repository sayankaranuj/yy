"""Authoritative scan lifecycle transitions."""

from __future__ import annotations

from fastapi import HTTPException, status

SCAN_STATES = {
    "created",
    "authorized",
    "queued",
    "running",
    "partial",
    "completed",
    "failed",
    "cancel_requested",
    "cancelled",
}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "created": {"authorized", "queued", "cancelled"},
    "authorized": {"queued", "cancelled"},
    "queued": {"running", "cancel_requested", "cancelled", "failed"},
    "running": {"partial", "completed", "failed", "cancel_requested"},
    "partial": {"completed", "failed", "queued", "cancel_requested"},
    "failed": {"queued", "cancelled"},
    "cancel_requested": {"cancelled", "failed", "completed"},
    "completed": set(),
    "cancelled": {"queued"},
}


def validate_transition(current: str, requested: str) -> None:
    """Reject lifecycle changes that would make scan state inconsistent."""

    if current not in SCAN_STATES or requested not in SCAN_STATES:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unknown scan lifecycle state",
        )
    if requested not in ALLOWED_TRANSITIONS[current]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"invalid scan transition: {current} -> {requested}",
        )
