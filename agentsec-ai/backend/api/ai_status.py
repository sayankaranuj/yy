"""Expose safe status information for the configured AI providers."""

from fastapi import APIRouter

from backend.config.settings import settings

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status")
async def ai_status() -> dict:
    return {
        "available": False,
        "message": "No LLM analysis provider is currently wired into the scan workflow.",
        "providers": [
            {"name": "OpenAI", "configured": bool(settings.ai.openai_api_key)},
            {"name": "Anthropic", "configured": bool(settings.ai.anthropic_api_key)},
        ],
    }
