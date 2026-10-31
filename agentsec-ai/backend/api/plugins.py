"""Plugin registry routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.registry import registry
from backend.workers.celery_app import celery_app
import asyncio

router = APIRouter(prefix="/plugins", tags=["plugins"])


class PluginRecord(BaseModel):
    """Simple plugin registry entry."""

    name: str
    description: str
    enabled: bool = True
    category: str
    version: str


@router.get("", response_model=list[PluginRecord])
async def list_plugins() -> list[PluginRecord]:
    """Return all discovered tool adapters."""

    registry.auto_discover()
    return [
        PluginRecord(
            name=item["name"],
            description=item.get("description", ""),
            enabled=item.get("enabled", True),
            category=item.get("category", "misc"),
            version=item.get("version", "unknown"),
        )
        for item in registry.list_all()
    ]


@router.get("/preflight")
async def plugin_preflight() -> list[dict]:
    """Return Docker-runtime readiness for every registered tool."""

    result = celery_app.send_task("workers.preflight.run", queue="recon_queue")
    try:
        return await asyncio.to_thread(result.get, timeout=30, propagate=True)
    except Exception as exc:
        return {
            "status": "FAILED_PREFLIGHT",
            "detail": f"worker preflight could not complete: {exc}",
            "task_id": result.id,
        }
