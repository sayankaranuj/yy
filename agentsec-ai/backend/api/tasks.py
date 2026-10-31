"""Task routes for AgentSec AI."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.workflow_store import WorkflowStore
from backend.config.settings import settings

router = APIRouter(prefix="/tasks", tags=["tasks"])
_store = WorkflowStore()


class TaskRecord(BaseModel):
    """Task payload returned by the API."""

    task_id: str
    task_name: str
    status: str
    retries: int = 0


@router.get("", response_model=list[TaskRecord])
async def list_tasks() -> list[TaskRecord]:
    """Return task inventory derived from the latest persisted workflow."""

    latest_state = (
        await _store.get_latest_state_async()
        if settings.storage_backend.lower() == "postgres"
        else _store.get_latest_state()
    )
    if latest_state is None:
        return []

    return [
        TaskRecord(
            task_id=task["task_id"],
            task_name=task["task_name"],
            status=task["status"],
            retries=task.get("retries", 0),
        )
        for task in latest_state.get("tasks", [])
    ]
