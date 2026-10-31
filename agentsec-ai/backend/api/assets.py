"""Asset inventory routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/assets", tags=["assets"])


class HostAsset(BaseModel):
    """Represents a discovered host."""

    host: str
    port: int = 80
    status: str = "open"
    service: str = "http"
    risk: str = "medium"


class EndpointAsset(BaseModel):
    """Represents a discovered endpoint."""

    path: str
    method: str = "GET"


class AssetInventory(BaseModel):
    """Collection of discovered hosts and endpoints."""

    hosts: list[HostAsset]
    endpoints: list[EndpointAsset]


@router.get("", response_model=AssetInventory)
async def list_assets() -> AssetInventory:
    """Return a simple asset inventory for the current workflow."""

    return AssetInventory(
        hosts=[HostAsset(host="example.com", port=80, status="open")],
        endpoints=[EndpointAsset(path="/", method="GET")],
    )
