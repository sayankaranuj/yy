"""Basic technology fingerprinter for tests."""

import json
import os
from typing import List, Dict, Any


class TechnologyFingerprinter:
    async def run(self, scan_id: str, hosts: List[str], ports: List[int]) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        tech = {h: ["http"] for h in hosts}
        summary = {"tech_map": tech, "has_wordpress": any("wordpress" in h for h in hosts)}
        with open(os.path.join(data_dir, f"tech_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f)
        return summary
