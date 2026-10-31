"""One-time import of the legacy JSON stores into PostgreSQL.

Run from the repository root after applying migrations:
    python scripts/import_json_store.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from sqlalchemy import text

from backend.config.database import AsyncSessionFactory, init_db
from backend.repositories import ActiveApiRepository


async def import_stores(scan_path: Path, findings_path: Path, workflow_path: Path) -> None:
    await init_db()
    scans = json.loads(scan_path.read_text(encoding="utf-8")) if scan_path.exists() else []
    findings = json.loads(findings_path.read_text(encoding="utf-8")) if findings_path.exists() else []
    workflows = json.loads(workflow_path.read_text(encoding="utf-8")).get("workflows", [])
    async with AsyncSessionFactory() as session:
        repo = ActiveApiRepository(session)
        from backend.models.active_api import ActiveFinding, ActiveScan
        for scan in scans:
            if await session.get(ActiveScan, scan["id"]) is None:
                session.add(ActiveScan(
                    id=scan["id"], name=scan["name"], target=scan["target"],
                    status=scan.get("status", "queued"),
                ))
        for finding in findings:
            if await session.get(ActiveFinding, finding["id"]) is None:
                session.add(ActiveFinding(
                    id=finding["id"], title=finding["title"],
                    severity=finding.get("severity", "medium"), status=finding.get("status", "open"),
                ))
        await session.commit()
        for table in ("active_scans", "active_findings"):
            await session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table}), 1), true)"
            ))
        await session.commit()
        for workflow in workflows:
            if await session.get(ActiveScan, workflow["scan_id"]) is None:
                continue
            await repo.upsert_workflow(workflow["scan_id"], {
                "target": workflow.get("target", ""),
                "status": workflow.get("status", "queued"),
                "steps": [
                    {"name": item["task_name"], "status": item["status"], "details": ""}
                    for item in workflow.get("tasks", [])
                ],
            })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan-store", type=Path, default=Path("backend/scan_store.json"))
    parser.add_argument("--findings-store", type=Path, default=Path("backend/findings_store.json"))
    parser.add_argument("--workflow-store", type=Path, default=Path("backend/workflow_store.json"))
    args = parser.parse_args()
    asyncio.run(import_stores(args.scan_store, args.findings_store, args.workflow_store))


if __name__ == "__main__":
    main()
