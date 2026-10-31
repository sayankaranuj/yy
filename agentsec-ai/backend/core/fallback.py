"""Fallback and retry manager for tasks and small operations."""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


class FallbackManager:
    def __init__(self, retries: int = 3, backoff: float = 1.0) -> None:
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        self.retries = retries
        self.backoff = backoff

    async def run_with_retry(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        last_exc = None
        for attempt in range(1, self.retries + 1):
            try:
                return await fn(*args, **kwargs)
            except Exception as exc:  # pragma: no cover - behavior exercised in tests
                last_exc = exc
                await asyncio.sleep(self.backoff * attempt)
        raise last_exc

    def run_with_retry_sync(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Run a synchronous callable with retries and incremental backoff."""
        import time

        last_exc = None
        for attempt in range(1, self.retries + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                last_exc = exc
                time.sleep(self.backoff * attempt)
        raise last_exc


__all__ = ["FallbackManager"]
