"""Result routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from backend.workflow_store import WorkflowStore
from backend.config.settings import settings
from backend.workflow_results import verified_workflow_results

router = APIRouter(prefix="/results", tags=["results"])
_store = WorkflowStore()


class ResultRecord(BaseModel):
    """Structured result payload returned by the API."""

    scan_id: int
    task_id: str
    tool_name: str
    payload: Any
    status: str = "SUCCESS"


@router.get("", response_model=list[ResultRecord])
async def list_results() -> list[ResultRecord]:
    """Return the current result inventory derived from the latest persisted workflow."""

    latest_state = (
        await _store.get_latest_state_async()
        if settings.storage_backend.lower() == "postgres"
        else _store.get_latest_state()
    )
    if latest_state is None:
        return []

    return [
        ResultRecord(**result)
        for result in verified_workflow_results(
            latest_state["scan_id"],
            latest_state.get("tasks", []),
            latest_state.get("results", []),
        )
    ]
