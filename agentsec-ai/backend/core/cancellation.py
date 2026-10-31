"""Cross-process cancellation signals for scan workers."""

from __future__ import annotations

import redis

from backend.config.settings import settings


_PREFIX = "agentsec:scan:cancel:"


def _client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis.url, decode_responses=True)


def request_scan_cancellation(scan_id: int, *, ttl: int = 86400) -> None:
    """Publish a durable, expiring cancellation signal visible to every worker."""

    client = _client()
    try:
        client.setex(f"{_PREFIX}{scan_id}", ttl, "1")
    finally:
        client.close()


def clear_scan_cancellation(scan_id: int) -> None:
    client = _client()
    try:
        client.delete(f"{_PREFIX}{scan_id}")
    finally:
        client.close()


def is_scan_cancelled(scan_id: int | str) -> bool:
    client = _client()
    try:
        return bool(client.exists(f"{_PREFIX}{scan_id}"))
    finally:
        client.close()
