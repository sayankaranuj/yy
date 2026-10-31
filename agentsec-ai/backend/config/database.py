"""Async database configuration for AgentSec AI."""

from __future__ import annotations

from collections.abc import AsyncGenerator
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config.settings import settings

engine = create_async_engine(
    settings.database.url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=settings.app_debug,
)

logger = logging.getLogger(__name__)

AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for dependency injection."""

    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Create all tables for the configured metadata."""

    from backend.models.base import Base
    from backend.models import active_api, user, organization, auditlog  # noqa: F401

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            for statement in (
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS scan_id INTEGER",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS task_id VARCHAR(255)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS affected_url TEXT",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS description TEXT",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS evidence JSON",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS source_tool VARCHAR(100)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS category VARCHAR(100)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS confidence DOUBLE PRECISION",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS asset TEXT",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS parameter VARCHAR(255)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS remediation TEXT",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS cwe VARCHAR(50)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS owasp_category VARCHAR(100)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS verification_state VARCHAR(30) NOT NULL DEFAULT 'unverified'",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS analyst_notes TEXT",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS assignee VARCHAR(255)",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS due_date TIMESTAMPTZ",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS risk_acceptance BOOLEAN NOT NULL DEFAULT FALSE",
                "ALTER TABLE active_findings ADD COLUMN IF NOT EXISTS dedup_key VARCHAR(64)",
                "UPDATE active_findings SET dedup_key = md5(lower(trim(title)) || chr(31) || lower(trim(coalesce(affected_url, ''))) || ':' || id::text) WHERE dedup_key IS NULL",
                "ALTER TABLE active_findings ALTER COLUMN dedup_key SET NOT NULL",
                "CREATE INDEX IF NOT EXISTS ix_active_findings_dedup_key ON active_findings (dedup_key)",
                "ALTER TABLE approved_targets ADD COLUMN IF NOT EXISTS ownership_verified BOOLEAN NOT NULL DEFAULT TRUE",
                "ALTER TABLE active_scans ALTER COLUMN target TYPE VARCHAR(500)",
                "ALTER TABLE active_scans ADD COLUMN IF NOT EXISTS git_options JSON",
                "ALTER TABLE approved_targets ALTER COLUMN target TYPE VARCHAR(500)",
                "ALTER TABLE active_workflows ALTER COLUMN target TYPE VARCHAR(500)",
                "CREATE INDEX IF NOT EXISTS ix_active_findings_scan_id ON active_findings (scan_id)",
                "ALTER TABLE active_workflow_tasks ADD COLUMN IF NOT EXISTS started_at TIMESTAMPTZ",
                "ALTER TABLE active_workflow_tasks ADD COLUMN IF NOT EXISTS completed_at TIMESTAMPTZ",
                "ALTER TABLE active_workflow_tasks ADD COLUMN IF NOT EXISTS duration_ms INTEGER",
                "ALTER TABLE active_workflow_tasks ADD COLUMN IF NOT EXISTS exit_code INTEGER",
                "ALTER TABLE active_workflow_tasks ADD COLUMN IF NOT EXISTS worker_hostname VARCHAR(255)",
                "ALTER TABLE active_workflow_results ADD COLUMN IF NOT EXISTS task_id VARCHAR(255)",
                "ALTER TABLE active_workflow_results ADD COLUMN IF NOT EXISTS command_metadata JSON",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER NOT NULL DEFAULT 0",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS locked_until TIMESTAMPTZ",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()",
                "ALTER TABLE refresh_sessions ALTER COLUMN replaced_by TYPE VARCHAR(128)",
            ):
                await conn.execute(text(statement))
    except Exception:
        if settings.app_env.lower() == "development":
            if settings.storage_backend.lower() == "postgres":
                settings.storage_backend = "json"
                logger.warning(
                    "Database unavailable; falling back to the JSON-backed development API"
                )
            else:
                logger.warning("Database unavailable; continuing with store-backed development API")
            return
        raise


__all__ = ["AsyncSessionFactory", "engine", "get_db", "init_db"]
