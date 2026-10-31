"""Redis-backed event bus for scan lifecycle and websocket updates."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Awaitable, Callable

import redis
import redis.asyncio as redis_async

from backend.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ScanStartedEvent:
    scan_id: str
    target: str
    scan_type: str
    config: dict[str, Any]


@dataclass(slots=True)
class ReconCompleteEvent:
    scan_id: str
    results: list[dict[str, Any]]


@dataclass(slots=True)
class EnumCompleteEvent:
    scan_id: str
    results: list[dict[str, Any]]


@dataclass(slots=True)
class VulnScanCompleteEvent:
    scan_id: str
    findings: list[dict[str, Any]]


@dataclass(slots=True)
class SecretsCompleteEvent:
    scan_id: str
    secrets: list[dict[str, Any]]


@dataclass(slots=True)
class ToolFailedEvent:
    scan_id: str
    tool_name: str
    error: str


@dataclass(slots=True)
class ScanCancelledEvent:
    scan_id: str


class EventBus:
    """Simple Redis pub/sub and websocket event hub."""

    _instance: "EventBus | None" = None

    def __new__(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._redis = redis_async.from_url(settings.redis.url, decode_responses=True)
        self._sync_redis = redis.Redis.from_url(settings.redis.url, decode_responses=True)
        self._initialized = True

    async def publish(self, event: Any) -> None:
        channel = f"agentsec:{event.__class__.__name__.lower()}"
        payload = json.dumps(asdict(event))
        await self._redis.publish(channel, payload)
        logger.info("Published event %s to %s", event.__class__.__name__, channel)

    async def subscribe(self, scan_id: str, callback: Callable[[Any], Awaitable[None]]) -> None:
        channel = f"agentsec:scan:{scan_id}"
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(channel)
        async def _listener() -> None:
            async for message in pubsub.listen():
                if message.get("type") != "message":
                    continue
                payload = json.loads(message.get("data", "{}"))
                await callback(payload)
        asyncio.create_task(_listener())

    async def publish_to_websocket(self, scan_id: str, event: Any) -> None:
        key = f"agentsec:ws:{scan_id}"
        payload = asdict(event) if is_dataclass(event) else event
        await self._redis.lpush(key, json.dumps(payload))
        await self._redis.ltrim(key, 0, 499)
        await self._redis.expire(key, 86400)

    def publish_to_websocket_sync(self, scan_id: str, event: Any) -> None:
        """Persist events from synchronous tool runners without crossing event loops."""

        key = f"agentsec:ws:{scan_id}"
        payload = asdict(event) if is_dataclass(event) else event
        with self._sync_redis.pipeline() as pipeline:
            pipeline.lpush(key, json.dumps(payload))
            pipeline.ltrim(key, 0, 499)
            pipeline.expire(key, 86400)
            pipeline.execute()

    async def get_scan_events(self, scan_id: str) -> list[dict[str, Any]]:
        key = f"agentsec:ws:{scan_id}"
        raw_events = await self._redis.lrange(key, 0, 499)
        return [json.loads(item) for item in raw_events]


event_bus = EventBus()

__all__ = ["EventBus", "ScanStartedEvent", "ReconCompleteEvent", "EnumCompleteEvent", "VulnScanCompleteEvent", "SecretsCompleteEvent", "ToolFailedEvent", "ScanCancelledEvent", "event_bus"]
