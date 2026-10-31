"""Simple ScanContext builder for tests."""

import json
import os
from typing import Dict, Any


class ScanContextBuilder:
    async def build(self, scan_id: str) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        ctx = {"scan_id": scan_id, "has_wordpress": False, "has_api_endpoints": False, "has_login_page": False}
        tech_path = os.path.join(data_dir, f"tech_{scan_id}.json")
        if os.path.exists(tech_path):
            with open(tech_path, "r", encoding="utf-8") as f:
                tech = json.load(f)
            ctx["has_wordpress"] = tech.get("has_wordpress", False)
        crawl_path = os.path.join(data_dir, f"crawl_{scan_id}.json")
        if os.path.exists(crawl_path):
            with open(crawl_path, "r", encoding="utf-8") as f:
                crawl = json.load(f)
            ctx["has_api_endpoints"] = any("/api/" in u for u in crawl.get("urls", []))
        return ctx
