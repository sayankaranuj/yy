"""Simplified Nuclei module for unit tests."""

from __future__ import annotations

import json
import os
from typing import List, Dict, Any
from backend.plugins.executor import executor
from backend.plugins.base_plugin import PluginInput


class NucleiScanModule:
    async def run(self, scan_id: str, context: Dict[str, Any], db) -> List[Dict[str, Any]]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        inp = PluginInput(
            scan_id=scan_id,
            target=context.get("target", "example.com"),
            task_id=context.get("task_id"),
        )
        out = executor.run("nuclei", inp)
        parsed = [
            {
                "title": item.get("info", {}).get("name") or item.get("template-id", "Nuclei finding"),
                "severity": str(item.get("info", {}).get("severity", "info")).upper(),
                "affected_url": item.get("matched-at") or item.get("host", context.get("target", "")),
                "evidence": item.get("curl-command") or item.get("matcher-name") or item.get("type", ""),
                "cve_id": (
                    item.get("info", {})
                    .get("classification", {})
                    .get("cve-id")
                ),
                "tool_found_by": "nuclei",
            }
            for item in out.parsed
            if out.success
        ]
        with open(os.path.join(data_dir, f"nuclei_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(parsed, f)
        return parsed
