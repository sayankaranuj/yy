"""Per-scan workflow and live event routes."""

from fastapi import APIRouter, HTTPException

from backend.config.settings import settings
from backend.workflow_store import WorkflowStore

router = APIRouter(prefix="/scans", tags=["workflow"])
store = WorkflowStore()


@router.get("/{scan_id}/workflow")
async def get_scan_workflow(scan_id: int) -> dict[str, object]:
    """Return task-level progress for one scan."""

    workflow = (
        await store.get_state_async(scan_id)
        if settings.storage_backend.lower() == "postgres"
        else store.get_state(scan_id)
    )
    if workflow is None:
        raise HTTPException(status_code=404, detail="workflow not found")
    return workflow


@router.get("/{scan_id}/results")
async def get_scan_results(scan_id: int) -> list[dict[str, object]]:
    """Return only worker results verified against this scan and its Celery task IDs."""

    if settings.storage_backend.lower() == "postgres":
        return await store.get_results_async(scan_id)
    return store.get_results(scan_id)
