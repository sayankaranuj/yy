"""Simple port scan coordinator for tests."""

import json
import os
from typing import List, Dict, Any


class PortScanCoordinator:
    async def run(self, scan_id: str, hosts: List[str]) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        open_ports = {h: [80, 443] for h in hosts}
        summary = {"open_ports_found": sum(len(v) for v in open_ports.values()), "open_ports": open_ports}
        with open(os.path.join(data_dir, f"ports_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f)
        return summary
