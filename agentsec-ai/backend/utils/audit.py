"""Audit logging helpers for sensitive AgentSec AI operations."""

from __future__ import annotations

import logging
from typing import Any

from backend.models.auditlog import AuditLog

logger = logging.getLogger(__name__)


class AuditLogger:
    """Persist audit events without allowing logging failures to stop a scan."""

    async def log(
        self,
        action: str,
        scan_id: str,
        db: Any,
        *,
        details: dict[str, Any] | None = None,
        actor: str = "system",
        actor_type: str = "system",
        severity: str = "info",
    ) -> AuditLog | None:
        """Write one audit record and return it when persistence succeeds."""

        record = AuditLog(
            scan_id=str(scan_id),
            action=action,
            action_type=action,
            actor=actor,
            actor_type=actor_type,
            resource_type="scan",
            resource_id=str(scan_id),
            details=details or {},
            severity=severity,
        )
        try:
            if db is None:
                logger.info("Audit event %s for scan %s: %s", action, scan_id, details or {})
                return record
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return record
        except Exception:
            logger.exception("Unable to persist audit event %s for scan %s", action, scan_id)
            try:
                await db.rollback()
            except Exception:
                logger.debug("Audit rollback failed", exc_info=True)
            return None


audit_logger = AuditLogger()

__all__ = ["AuditLogger", "audit_logger"]