"""API router registration for AgentSec AI."""

from fastapi import APIRouter, FastAPI

from backend.api.assets import router as assets_router
from backend.api.ai_status import router as ai_status_router
from backend.api.auth import router as auth_router
from backend.api.dashboard import router as dashboard_router
from backend.api.dashboard_breakdown import router as dashboard_breakdown_router
from backend.api.dashboard_details import router as dashboard_details_router
from backend.api.dashboard_timeline import router as dashboard_timeline_router
from backend.api.database_status import router as database_status_router
from backend.api.findings import router as findings_router
from backend.api.plugins import router as plugins_router
from backend.api.payload_intel import router as payload_intel_router
from backend.api.reports import router as reports_router
from backend.api.results import router as results_router
from backend.api.scans import router as scans_router
from backend.api.tasks import router as tasks_router
from backend.api.targets import router as targets_router
from backend.api.websocket import router as websocket_router
from backend.api.workflow import router as workflow_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(ai_status_router)
api_router.include_router(scans_router)
api_router.include_router(findings_router)
api_router.include_router(reports_router)
api_router.include_router(assets_router)
api_router.include_router(dashboard_router)
api_router.include_router(dashboard_details_router)
api_router.include_router(dashboard_breakdown_router)
api_router.include_router(dashboard_timeline_router)
api_router.include_router(database_status_router)
api_router.include_router(plugins_router)
api_router.include_router(tasks_router)
api_router.include_router(targets_router)
api_router.include_router(results_router)
api_router.include_router(websocket_router)
api_router.include_router(payload_intel_router)
api_router.include_router(workflow_router)

api_v1_router = APIRouter(prefix="/api/v1")
for router in [
    auth_router,
    ai_status_router,
    scans_router,
    findings_router,
    reports_router,
    assets_router,
    dashboard_router,
    dashboard_details_router,
    dashboard_breakdown_router,
    dashboard_timeline_router,
    database_status_router,
    plugins_router,
    tasks_router,
    targets_router,
    results_router,
    websocket_router,
    payload_intel_router,
    workflow_router,
]:
    api_v1_router.include_router(router)


def include_api_routes(app: FastAPI) -> None:
    """Register the API router with the FastAPI app."""

    app.include_router(api_router)
    app.include_router(api_v1_router)
