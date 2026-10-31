import json
import os
import asyncio

from backend.workers.vuln_agent import _async_start_vuln
from backend.core.eventbus import EventBus


def setup_context(scan_id: str):
    data_dir = os.path.join(os.getcwd(), "backend", "data")
    os.makedirs(data_dir, exist_ok=True)
    # create a minimal context with api and login
    ctx = {"scan_id": scan_id, "has_api_endpoints": True, "has_login_page": True}
    with open(os.path.join(data_dir, f"context_{scan_id}.json"), "w", encoding="utf-8") as f:
        json.dump(ctx, f)
    return ctx


def test_vuln_flow():
    scan_id = "test-002"
    ctx = setup_context(scan_id)
    events = []

    def on_complete(payload):
        events.append(payload)

    EventBus().subscribe("vuln.completed", on_complete)

    res = asyncio.run(_async_start_vuln(scan_id, ctx))
    assert res["scan_id"] == scan_id
    assert res["total_findings"] >= 0
    assert events, "vuln.completed event not published"
