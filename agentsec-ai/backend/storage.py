"""Simple JSON-backed scan storage for AgentSec AI."""

from __future__ import annotations

import json
from datetime import datetime, timezone
import threading
from pathlib import Path
from typing import Any

from backend.config.database import AsyncSessionFactory
from backend.repositories import ActiveApiRepository


_STORE_WRITE_LOCK = threading.Lock()


class ScanStore:
    """Persist scan records to a local JSON file."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(file_path or Path(__file__).resolve().parent / "scan_store.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return []
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict[str, Any]]) -> None:
        payload = json.dumps(records, indent=2)
        temp_path = self.file_path.with_suffix(".tmp")
        with _STORE_WRITE_LOCK:
            temp_path.write_text(payload, encoding="utf-8")
            try:
                temp_path.replace(self.file_path)
            except PermissionError:
                self.file_path.write_text(payload, encoding="utf-8")
                temp_path.unlink(missing_ok=True)

    def list_records(self) -> list[dict[str, Any]]:
        return self._read()

    def create_record(
        self,
        name: str,
        target: str,
        status: str = "queued",
        selected_attack_categories: list[str] | None = None,
        git_options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        records = self._read()
        record = {
            "id": len(records) + 1,
            "name": name,
            "target": target,
            "status": status,
            "selected_attack_categories": selected_attack_categories,
            "git_options": git_options,
        }
        records.append(record)
        self._write(records)
        return record

    def update_status(self, scan_id: int, status: str) -> dict[str, Any] | None:
        records = self._read()
        for record in records:
            if record["id"] == scan_id:
                record["status"] = status
                self._write(records)
                return record
        return None

    async def list_records_async(self) -> list[dict[str, Any]]:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).list_scans()

    async def create_record_async(
        self,
        name: str,
        target: str,
        status: str = "queued",
        selected_attack_categories: list[str] | None = None,
        git_options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).create_scan(
                name,
                target,
                status,
                selected_attack_categories,
                git_options,
            )

    async def update_status_async(self, scan_id: int, status: str) -> dict[str, Any] | None:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).update_scan_status(scan_id, status)


class TargetStore:
    """Persist administrator-approved targets."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(file_path or Path(__file__).resolve().parent / "approved_targets.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict[str, Any]]) -> None:
        with _STORE_WRITE_LOCK:
            temporary_path = self.file_path.with_suffix(".tmp")
            temporary_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
            temporary_path.replace(self.file_path)

    def list_records(self) -> list[dict[str, Any]]:
        return [record for record in self._read() if record.get("enabled", True)]

    def approve(self, target: str, approved_by: str, reason: str) -> dict[str, Any]:
        records = self._read()
        record = next((item for item in records if item["target"] == target), None)
        if record is None or not record.get("ownership_verified", False):
            raise ValueError("target ownership has not been verified")
        record.update(
            {
                "approved_by": approved_by,
                "reason": reason,
                "enabled": True,
                "ownership_verified": True,
            }
        )
        self._write(records)
        return record

    def approve_manual(self, target: str, approved_by: str, reason: str) -> dict[str, Any]:
        """Add a target explicitly approved by an administrator without claiming proof."""
        records = self._read()
        record = next((item for item in records if item["target"] == target), None)
        if record is None:
            record = {"id": len(records) + 1, "target": target}
            records.append(record)
        record.update(
            {
                "approved_by": approved_by,
                "reason": reason,
                "enabled": True,
                "ownership_verified": False,
            }
        )
        self._write(records)
        return record

    def create_verification(self, target: str, method: str, token: str) -> dict[str, Any]:
        records = self._read()
        record = next((item for item in records if item["target"] == target), None)
        if record is None:
            record = {"id": len(records) + 1, "target": target, "enabled": False}
            records.append(record)
        record.update(
            {
                "verification_method": method,
                "verification_token": token,
                "ownership_verified": False,
                "verified_at": None,
            }
        )
        self._write(records)
        return record

    def mark_verified(self, target: str, method: str, token: str) -> bool:
        records = self._read()
        record = next((item for item in records if item["target"] == target), None)
        if record is None or record.get("verification_method") != method or record.get("verification_token") != token:
            return False
        record["ownership_verified"] = True
        record["verified_at"] = datetime.now(timezone.utc).isoformat()
        self._write(records)
        return True

    def is_verified(self, target: str) -> bool:
        return any(
            item["target"] == target and item.get("ownership_verified", False)
            for item in self._read()
        )

    def revoke(self, target: str) -> bool:
        records = self._read()
        record = next((item for item in records if item["target"] == target), None)
        if record is None:
            return False
        record["enabled"] = False
        self._write(records)
        return True

    def is_approved(self, target: str) -> bool:
        return any(item["target"] == target for item in self.list_records())

    async def list_records_async(self) -> list[dict[str, Any]]:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).list_approved_targets()

    async def approve_async(self, target: str, approved_by: str, reason: str) -> dict[str, Any]:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).approve_target(target, approved_by, reason)

    async def revoke_async(self, target: str) -> bool:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).revoke_target(target)

    async def is_approved_async(self, target: str) -> bool:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).is_target_approved(target)


class FindingsStore:
    """Persist finding records to a local JSON file."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(file_path or Path(__file__).resolve().parent / "findings_store.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return []
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict[str, Any]]) -> None:
        payload = json.dumps(records, indent=2)
        temp_path = self.file_path.with_suffix(".tmp")
        with _STORE_WRITE_LOCK:
            temp_path.write_text(payload, encoding="utf-8")
            try:
                temp_path.replace(self.file_path)
            except PermissionError:
                self.file_path.write_text(payload, encoding="utf-8")
                temp_path.unlink(missing_ok=True)

    def list_records(self) -> list[dict[str, Any]]:
        return self._read()

    def create_record(
        self,
        title: str,
        severity: str,
        status: str = "open",
        scan_id: int | None = None,
        task_id: str | None = None,
        affected_url: str | None = None,
        description: str | None = None,
        evidence: Any = None,
    ) -> dict[str, Any]:
        records = self._read()
        record = {
            "id": len(records) + 1,
            "title": title,
            "severity": severity,
            "status": status,
            "scan_id": scan_id,
            "task_id": task_id,
            "affected_url": affected_url,
            "description": description,
            "evidence": evidence,
        }
        records.append(record)
        self._write(records)
        return record

    async def create_record_async(
        self,
        title: str,
        severity: str,
        status: str = "open",
        scan_id: int | None = None,
        task_id: str | None = None,
        affected_url: str | None = None,
        description: str | None = None,
        evidence: Any = None,
    ) -> dict[str, Any]:
        """Persist a finding in the configured PostgreSQL store."""

        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).create_finding(
                title, severity, status, scan_id, task_id, affected_url, description, evidence
            )

    async def list_records_async(self) -> list[dict[str, Any]]:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).list_findings()

    async def get_record_async(self, finding_id: int) -> dict[str, Any] | None:
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).get_finding(finding_id)


class AuthorizationRequestStore:
    """Persist administrator-reviewed target authorization requests."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = Path(
            file_path or Path(__file__).resolve().parent / "authorization_requests.json"
        )
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict[str, Any]]) -> None:
        temporary_path = self.file_path.with_suffix(".tmp")
        with _STORE_WRITE_LOCK:
            temporary_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
            temporary_path.replace(self.file_path)

    def list_records(self) -> list[dict[str, Any]]:
        return sorted(self._read(), key=lambda item: item["id"], reverse=True)

    def create(self, target: str, reason: str, requested_by: str) -> dict[str, Any]:
        records = self._read()
        record = {
            "id": max((item["id"] for item in records), default=0) + 1,
            "target": target,
            "reason": reason,
            "requested_by": requested_by,
            "status": "pending",
            "reviewed_by": None,
            "review_note": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "reviewed_at": None,
        }
        records.append(record)
        self._write(records)
        return record

    def review(
        self, request_id: int, decision: str, reviewed_by: str, review_note: str
    ) -> dict[str, Any] | None:
        records = self._read()
        record = next(
            (item for item in records if item["id"] == request_id and item["status"] == "pending"),
            None,
        )
        if record is None:
            return None
        record.update(
            {
                "status": "approved" if decision == "approve" else "rejected",
                "reviewed_by": reviewed_by,
                "review_note": review_note,
                "reviewed_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._write(records)
        return record
