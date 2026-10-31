"""Read-only status for the configured PostgreSQL connection."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.config.database import engine
from backend.config.settings import settings

router = APIRouter(prefix="/database", tags=["database"])


@router.get("/status")
async def database_status() -> dict[str, str]:
    """Return connection metadata without exposing credentials or arbitrary queries."""
    if settings.storage_backend.lower() != "postgres":
        return {
            "status": "unavailable",
            "storage_backend": settings.storage_backend,
            "database": "",
            "user": "",
            "version": "",
        }
    try:
        async with engine.connect() as connection:
            row = (
                await connection.execute(
                    text("SELECT current_database(), current_user, version()")
                )
            ).one()
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="configured PostgreSQL database is unavailable",
        ) from exc
    return {
        "status": "connected",
        "storage_backend": "postgres",
        "database": row[0],
        "user": row[1],
        "version": row[2].split(",", maxsplit=1)[0],
    }
