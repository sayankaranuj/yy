"""Simplified API security module for unit tests."""

from __future__ import annotations

import json
import os
from typing import List, Dict, Any
from backend.plugins.executor import executor
from backend.plugins.base_plugin import PluginInput


class APISecurityModule:
    async def run(self, scan_id: str, context: Dict[str, Any], db) -> List[Dict[str, Any]]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        findings = []
        if context.get("has_api_endpoints"):
            inp = PluginInput(
                scan_id=scan_id,
                target=context.get("target", "example.com"),
                task_id=context.get("task_id"),
            )
            out = executor.run("secretfinder", inp)
            parsed = getattr(out, "parsed", []) if out else []
            findings.extend(parsed)

        with open(os.path.join(data_dir, f"api_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(findings, f)
        return findings
