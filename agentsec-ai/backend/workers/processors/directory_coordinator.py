"""Simple directory discovery coordinator for tests."""

import json
import os
from typing import Dict, Any, List


class DirectoryDiscoveryCoordinator:
    async def run(self, scan_id: str, hosts: List[str], tech_summary: Dict[str, Any]) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        results = {h: ["/admin", "/login"] for h in hosts}
        summary = {"dirs_found": results, "total": sum(len(v) for v in results.values())}
        with open(os.path.join(data_dir, f"dirs_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f)
        return summary
