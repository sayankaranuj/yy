"""Simple in-process EventBus used by agents and tests.

Provides subscribe/publish with minimal scheduling: synchronous
callables are invoked directly; async handlers are scheduled on the
running event loop if present, otherwise run with asyncio.run().
"""

from __future__ import annotations

import asyncio
from typing import Any, Callable

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subs = {}
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        return cls._instance

    def subscribe(self, event: str, handler: Callable[[str, Any], Any]) -> None:
        """
        Normalize and store handlers so `publish` can always invoke them
        with `(event, payload)`. Handlers that accept a single `payload`
        argument will still work via a wrapper.
        """
        # Wrap async handlers
        if asyncio.iscoroutinefunction(handler):
            async def _wrapped(e, p):
                try:
                    await handler(e, p)
                except TypeError:
                    await handler(p)

            self._subs.setdefault(event, []).append(_wrapped)
        else:
            def _wrapped(e, p):
                try:
                    return handler(e, p)
                except TypeError:
                    return handler(p)

            self._subs.setdefault(event, []).append(_wrapped)

    def publish(self, event: str, payload: Any) -> None:
        handlers = list(self._subs.get(event, []))
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        for h in handlers:
            try:
                if asyncio.iscoroutinefunction(h):
                    # For async handlers, always call the (event, payload) signature.
                    # Older sync handlers are supported below.
                    if loop:
                        loop.create_task(h(event, payload))
                    else:
                        asyncio.run(h(event, payload))
                else:
                    try:
                        h(event, payload)
                    except TypeError:
                        h(payload)
            except Exception:
                # swallow handler exceptions to avoid breaking publisher
                pass


__all__ = ["EventBus"]
