import json
import os
import asyncio

from backend.workers.enum_agent import _async_start_enum
from backend.core.eventbus import EventBus


def setup_recon(scan_id: str):
    data_dir = os.path.join(os.getcwd(), "backend", "data")
    os.makedirs(data_dir, exist_ok=True)
    recon = {"subdomains": ["example.com", "wordpress.example.com"]}
    with open(os.path.join(data_dir, f"recon_{scan_id}.json"), "w", encoding="utf-8") as f:
        json.dump(recon, f)


def test_enum_flow(tmp_path, monkeypatch):
    scan_id = "test-001"
    setup_recon(scan_id)
    events = []

    def on_complete(payload):
        events.append(payload)

    EventBus().subscribe("enum.completed", on_complete)

    # run
    res = asyncio.run(_async_start_enum(scan_id))
    assert res["scan_id"] == scan_id
    assert res["live_hosts"] == 2
    assert events, "enum.completed event was not published"
