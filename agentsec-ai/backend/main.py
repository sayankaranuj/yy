"""Entry point for the AgentSec AI FastAPI backend."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import asyncpg
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.api.router import include_api_routes
from backend.config.database import engine, init_db
from backend.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize backend services when the app starts and clean up on shutdown."""

    await init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    app = FastAPI(title="AgentSec AI", lifespan=lifespan)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[host.strip() for host in settings.allowed_hosts.split(",") if host.strip()],
    )

    @app.middleware("http")
    async def require_api_auth(request: Request, call_next) -> Response:
        """Protect API routes while leaving health and login available."""

        if (
            not settings.jwt.enabled
            or not request.url.path.startswith(("/api/", "/api/v1/"))
            or request.url.path.endswith("/auth/login")
            or request.url.path.endswith("/auth/register")
            or request.url.path.endswith("/auth/refresh")
            or request.url.path.endswith("/auth/logout")
            or request.url.path.endswith("/health")
        ):
            return await call_next(request)
        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "authentication required"})
        try:
            jwt.decode(
                authorization[7:],
                settings.jwt.secret_key,
                algorithms=[settings.jwt.algorithm],
            )
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "invalid or expired token"})
        return await call_next(request)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Return the backend health status for smoke tests and monitoring."""

        return {"status": "ok"}

    @app.get("/health/ready")
    async def readiness_check() -> JSONResponse:
        """Report whether the backend can reach its configured PostgreSQL database."""

        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except (SQLAlchemyError, asyncpg.PostgresError, OSError):
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "database": "unavailable"},
            )

        return JSONResponse(status_code=200, content={"status": "ready", "database": "ok"})

    include_api_routes(app)
    return app


app = create_app()
