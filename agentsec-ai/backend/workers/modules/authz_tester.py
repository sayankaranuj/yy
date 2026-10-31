"""Simplified Authorization Tester based on authz0 logic."""

from __future__ import annotations

import json
import os
from typing import List, Dict, Any


class AuthorizationTester:
    async def run(self, scan_id: str, context: Dict[str, Any], db) -> List[Dict[str, Any]]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        findings = []
        with open(os.path.join(data_dir, f"authz_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(findings, f)
        return findings
