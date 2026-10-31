"""WebSocket routes for live scan events."""

import asyncio
from contextlib import suppress
import json
from jose import JWTError, jwt

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from backend.config.settings import settings

from backend.orchestrator.event_bus import event_bus

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/events")
async def websocket_events(
    websocket: WebSocket,
    scan_id: int | None = None,
    token: str | None = None,
) -> None:
    """Stream persisted Redis events without starting a second scan."""

    await websocket.accept()
    if settings.jwt.enabled:
        try:
            if not token:
                raise JWTError
            jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        except JWTError:
            await websocket.close(code=4401)
            return
    if scan_id is None:
        await websocket.send_json({"event": "connected", "scan_id": None})
        await websocket.close()
        return

    seen: set[str] = set()
    try:
        while True:
            events = await event_bus.get_scan_events(str(scan_id))
            for event in reversed(events):
                marker = json.dumps(event, sort_keys=True)
                if marker in seen:
                    continue
                seen.add(marker)
                await websocket.send_json(event)
            await asyncio.sleep(0.5)
    except (WebSocketDisconnect, asyncio.CancelledError):
        raise
    finally:
        with suppress(Exception):
            await websocket.close()
