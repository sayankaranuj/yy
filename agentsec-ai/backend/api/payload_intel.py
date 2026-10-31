"""Public payload-intelligence metadata and sample routes."""

from fastapi import APIRouter, HTTPException, Query

from backend.services.payload_intel import payload_intel

router = APIRouter(prefix="/intel", tags=["intel"])


@router.get("/sources")
async def list_sources() -> list[dict[str, object]]:
    """List public sources and their license attribution."""

    return payload_intel.sources()


@router.get("/sample/{category}")
async def get_sample(
    category: str,
    count: int = Query(default=20, ge=1, le=100),
) -> dict[str, object]:
    """Return a bounded sample for a supported category."""

    try:
        source, samples = await payload_intel.sample(category, count)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="unknown payload category") from exc
    return {
        "category": category,
        "source": source,
        "samples": samples,
    }
