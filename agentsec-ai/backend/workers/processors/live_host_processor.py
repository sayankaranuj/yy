"""Simple live host processor for tests."""

import json
import os
from typing import List, Dict, Any


class LiveHostProcessor:
    async def process(self, subdomains: List[str], scan_id: str) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        # naive: treat all subdomains as alive
        live = [s for s in subdomains if s]
        out = {
            "alive_count": len(live),
            "live_hosts_list": live,
            "interesting_hosts": live,
        }
        with open(os.path.join(data_dir, f"live_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f)
        return out
