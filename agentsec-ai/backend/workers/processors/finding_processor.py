"""Processor to insert validated findings into JSON storage for tests."""

import json
import os
from typing import List, Dict, Any

from backend.config.settings import settings
from backend.storage import FindingsStore
from backend.utils.redaction import redact_mapping


class FindingProcessor:
    async def process_all(self, scan_id: str, validated_results: List[Dict[str, Any]], db) -> int:
        data_dir = os.path.join(os.getcwd(), "backend", "data")
        os.makedirs(data_dir, exist_ok=True)
        out_file = os.path.join(data_dir, f"findings_{scan_id}.json")
        existing = []
        if os.path.exists(out_file):
            with open(out_file, "r", encoding="utf-8") as f:
                existing = json.load(f)

        count = 0
        findings_store = FindingsStore()
        for r in validated_results:
            key = (r.get("title"), r.get("affected_url"))
            if any((e.get("title"), e.get("affected_url")) == key for e in existing):
                continue
            finding = redact_mapping(r)
            existing.append(finding)
            if settings.storage_backend.lower() == "postgres":
                await findings_store.create_record_async(
                    title=finding.get("title", "Scanner finding"),
                    severity=str(finding.get("severity", "info")).lower(),
                    status="open",
                    scan_id=int(scan_id) if str(scan_id).isdigit() else None,
                    task_id=finding.get("task_id"),
                    affected_url=finding.get("affected_url") or finding.get("url"),
                    description=finding.get("description") or finding.get("detail"),
                    evidence=finding.get("evidence") or finding.get("proof"),
                )
            else:
                findings_store.create_record(
                    title=finding.get("title", "Scanner finding"),
                    severity=str(finding.get("severity", "info")).lower(),
                    status="open",
                    scan_id=int(scan_id) if str(scan_id).isdigit() else None,
                    task_id=finding.get("task_id"),
                    affected_url=finding.get("affected_url") or finding.get("url"),
                    description=finding.get("description") or finding.get("detail"),
                    evidence=finding.get("evidence") or finding.get("proof"),
                )
            count += 1

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(existing, f)
        return count
