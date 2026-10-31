"""Simplified Enumeration Agent for tests and CI.

This implementation is intentionally lightweight: it reads recon results
from backend/data/recon_{scan_id}.json (produced by ReconResultProcessor),
runs a sequence of processors that write JSON artifacts under backend/data,
publishes an 'enum.completed' event on EventBus and returns a summary dict.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any, Dict

from backend.core.eventbus import EventBus
from backend.workers.processors.live_host_processor import LiveHostProcessor
from backend.workers.processors.port_scan_coordinator import PortScanCoordinator
from backend.workers.processors.tech_fingerprinter import TechnologyFingerprinter
from backend.workers.processors.crawler_coordinator import WebCrawlerCoordinator
from backend.workers.processors.directory_coordinator import DirectoryDiscoveryCoordinator
from backend.workers.processors.enum_processor import EnumResultProcessor
from backend.workers.processors.context_builder import ScanContextBuilder
from backend.workers.celery_app import celery_app  # noqa: E402
from backend.plugins.base_plugin import PluginInput
from backend.plugins.executor import executor
from backend.core.cancellation import is_scan_cancelled


@celery_app.task(bind=True, name="enum.start", queue="enum_queue", autoretry_for=(Exception,), max_retries=3)
def start_enum(self, scan_id: str, recon_summary: dict | None = None) -> Dict[str, Any]:
    return asyncio.run(_async_start_enum(scan_id, recon_summary))


async def _async_start_enum(scan_id: str, recon_summary: dict | None = None) -> Dict[str, Any]:
    start = time.time()
    data_dir = os.path.join(os.getcwd(), "backend", "data")
    os.makedirs(data_dir, exist_ok=True)

    recon_path = os.path.join(data_dir, f"recon_{scan_id}.json")
    if not os.path.exists(recon_path):
        # nothing to do
        summary = {"scan_id": scan_id, "live_hosts": 0, "open_ports": 0, "endpoints": 0}
        EventBus().publish("enum.completed", summary)
        return summary

    with open(recon_path, "r", encoding="utf-8") as f:
        recon = json.load(f)

    # STEP 1: Live host detection
    live_proc = LiveHostProcessor()
    live_summary = await live_proc.process(recon.get("subdomains", []), scan_id)

    # STEP 2: Port scanning
    port_coord = PortScanCoordinator()
    port_summary = await port_coord.run(scan_id, live_summary.get("live_hosts_list", []))

    # STEP 3: Tech fingerprinting
    fingerprinter = TechnologyFingerprinter()
    tech_summary = await fingerprinter.run(scan_id, live_summary.get("live_hosts_list", []), [])

    # STEP 4: Crawling
    crawler = WebCrawlerCoordinator()
    crawl_summary = await crawler.run(scan_id, live_summary.get("live_hosts_list", []))

    # STEP 5: Directory discovery
    dir_coord = DirectoryDiscoveryCoordinator()
    dir_summary = await dir_coord.run(scan_id, live_summary.get("interesting_hosts", []), tech_summary)

    # STEP 6: Aggregate
    processor = EnumResultProcessor()
    await processor.update_scan_stats(scan_id, live_summary, port_summary, tech_summary, crawl_summary, dir_summary)

    # STEP 7: Build context
    builder = ScanContextBuilder()
    context = await builder.build(scan_id)

    summary = {
        "scan_id": scan_id,
        "live_hosts": live_summary.get("alive_count", 0),
        "open_ports": port_summary.get("open_ports_found", 0),
        "endpoint_count": crawl_summary.get("unique_urls", 0),
        "execution_time": time.time() - start,
    }

    EventBus().publish("enum.completed", summary)

    # persist context
    data_path = os.path.join(data_dir, f"context_{scan_id}.json")
    with open(data_path, "w", encoding="utf-8") as fh:
        json.dump(context, fh)

    return summary
"""Enumeration agent Celery tasks."""


from backend.workers.celery_app import celery_app  # noqa: E402


@celery_app.task(bind=True, name="workers.enum.run", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def run(
    self,
    scan_id: int,
    target: str,
    selected_categories: list[str] | None = None,
) -> dict[str, Any]:
    """Run the real HTTP, port, and crawl tools selected for this scan."""

    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "target": target, "status": "cancelled", "tools": []}
    return asyncio.run(
        _run_selected_tools(scan_id, target, selected_categories, self.request.id)
    )


async def _run_selected_tools(
    scan_id: int,
    target: str,
    selected_categories: list[str] | None,
    task_id: str | None = None,
) -> dict[str, Any]:
    """Execute selected enumeration tools and return only their parsed output."""

    categories = set(selected_categories or [])
    all_categories = not categories
    tools_to_run = []
    if all_categories or "enum.live_hosts" in categories or "enum.tech_fingerprint" in categories:
        tools_to_run.append("httpx")
    if all_categories or "enum.port_scan" in categories:
        tools_to_run.append("naabu")
    if all_categories or "enum.crawling" in categories or "enum.js_discovery" in categories:
        tools_to_run.append("katana")

    results = []
    for tool_name in tools_to_run:
        if is_scan_cancelled(scan_id):
            return {"scan_id": scan_id, "target": target, "status": "cancelled", "tools": results}
        tool_input = PluginInput(scan_id=str(scan_id), target=target, task_id=task_id)
        output = await asyncio.to_thread(executor.run, tool_name, tool_input)
        results.append(
            {
                "tool": output.tool_name,
                "success": output.success,
                "record_count": output.record_count,
                "results": output.parsed,
                "error": output.error_message,
                "raw_output": output.raw_output,
                "command_executed": output.command_executed,
                "execution_time": output.execution_time,
            }
        )

    successful = [result for result in results if result["success"]]
    failed = [result for result in results if not result["success"]]
    status = "completed" if successful and not failed else "partial" if successful else "failed"
    return {
        "scan_id": scan_id,
        "target": target,
        "status": status,
        "tools": results,
        "live_hosts": sum(
            result["record_count"] for result in successful if result["tool"] == "httpx_plugin"
        ),
        "open_ports": sum(
            result["record_count"] for result in successful if result["tool"] == "naabu"
        ),
        "endpoint_count": sum(
            result["record_count"] for result in successful if result["tool"] == "katana"
        ),
    }
# AgentSec AI — backend/workers/enum_agent.py