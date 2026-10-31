"""Processor to aggregate enum results and update simple JSON scan record."""

import json
import os


class EnumResultProcessor:
    async def update_scan_stats(self, scan_id: str, live, ports, tech, crawl, dirs) -> None:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        out = {
            "scan_id": scan_id,
            "live": live,
            "ports": ports,
            "tech": tech,
            "crawl": crawl,
            "dirs": dirs,
        }
        with open(os.path.join(data_dir, f"enum_summary_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f)
