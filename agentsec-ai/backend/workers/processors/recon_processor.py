"""Recon result processor helpers.

Provides small async helpers to persist recon subdomains and auxiliary
data. For Phase 4 we persist to a JSON file under `backend/data/` to
avoid DB coupling in unit tests. The interface mirrors what agents expect.
"""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ReconSummary:
    scan_id: str
    inserted: int
    created_at: datetime


class ReconResultProcessor:
    def __init__(self, storage_dir: str | None = None) -> None:
        self.storage_dir = storage_dir or os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(self.storage_dir, exist_ok=True)

    async def store_subdomains(self, scan_id: str, subdomains: List[str]) -> int:
        """Persist a simple JSON file with discovered subdomains. Returns inserted count."""
        # Simulate async DB work
        await asyncio.sleep(0)
        path = os.path.join(self.storage_dir, f"recon_{scan_id}.json")
        payload = {"scan_id": scan_id, "subdomains": subdomains, "created_at": datetime.utcnow().isoformat()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return len(subdomains)

    async def store_all(self, scan_id: str, subdomains: List[str], **kwargs) -> ReconSummary:
        count = await self.store_subdomains(scan_id, subdomains)
        return ReconSummary(scan_id=scan_id, inserted=count, created_at=datetime.utcnow())
