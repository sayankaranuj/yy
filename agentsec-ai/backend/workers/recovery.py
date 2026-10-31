"""Bounded recovery for workflow tasks whose workers stopped reporting."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from backend.repositories import ActiveApiRepository


class StaleTaskRecoveryService:
    """Detect stale attempts and retry them once before dead-lettering."""

    def __init__(
        self,
        repository: ActiveApiRepository,
        *,
        max_attempts: int = 3,
        dead_letter_queue: str = "workflow_dead_letter_queue",
        enqueue: Callable[..., Any] | None = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self.repository = repository
        self.max_attempts = max_attempts
        self.dead_letter_queue = dead_letter_queue
        self.enqueue = enqueue

    async def recover(
        self,
        *,
        stale_after: timedelta,
        now: datetime | None = None,
        scan_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """Recover all stale attempts, bounded by ``max_attempts``."""

        current = now or datetime.now(timezone.utc)
        stale = await self.repository.list_stale_task_attempts(
            current - stale_after, scan_id=scan_id
        )
        recovered: list[dict[str, Any]] = []
        for attempt in stale:
            terminal = attempt["attempt_number"] >= self.max_attempts
            queue = self.dead_letter_queue if terminal else attempt["queue"]
            reason = (
                f"stale after {stale_after.total_seconds():g}s; "
                f"attempt {attempt['attempt_number']} of {self.max_attempts}"
            )
            metadata = {
                "recovery_reason": reason,
                "recovered_at": current.isoformat(),
                "dead_letter": terminal,
            }
            row = await self.repository.recover_task_attempt(
                attempt["id"],
                dead_letter=terminal,
                reason=reason,
                queue=queue,
                metadata=metadata,
            )
            if row is None:
                continue
            if not terminal and self.enqueue is not None:
                self.enqueue(
                    attempt["task_name"],
                    args=(attempt["workflow_scan_id"],),
                    queue=queue,
                    headers={"recovered_from_attempt": attempt["id"]},
                )
            recovered.append(row)
        return recovered

