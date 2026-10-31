"""Simple web crawler coordinator for tests."""

import json
import os
from typing import List, Dict, Any


class WebCrawlerCoordinator:
    async def run(self, scan_id: str, hosts: List[str]) -> Dict[str, Any]:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        urls = []
        for h in hosts:
            urls.append(f"http://{h}/")
            urls.append(f"https://{h}/")
        unique = list(dict.fromkeys(urls))
        summary = {"unique_urls": len(unique), "urls": unique}
        with open(os.path.join(data_dir, f"crawl_{scan_id}.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f)
        return summary
