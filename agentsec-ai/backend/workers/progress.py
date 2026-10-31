"""Persist Celery task lifecycle state for live scan progress."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from backend.repositories import ActiveApiRepository
from backend.config.settings import settings
from backend.workflow_store import WorkflowStore

logger = logging.getLogger(__name__)


async def update_task_async(
    scan_id: int,
    task_name: str,
    task_id: str,
    status: str,
    result: Any = None,
) -> None:
    """Update one workflow task and its aggregate workflow status."""

    engine = create_async_engine(settings.database.url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        await ActiveApiRepository(session).update_workflow_task(
            scan_id, task_name, task_id, status, result
        )
    await engine.dispose()


def update_task(
    scan_id: int,
    task_name: str,
    task_id: str,
    status: str,
    result: Any = None,
) -> None:
    """Best-effort synchronous bridge used by Celery signal handlers."""

    try:
        if settings.storage_backend.lower() != "postgres":
            WorkflowStore().update_task(scan_id, task_name, task_id, status, result)
            return
        asyncio.run(update_task_async(scan_id, task_name, task_id, status, result))
    except Exception:
        logger.warning("Unable to persist task progress for scan %s", scan_id, exc_info=True)
