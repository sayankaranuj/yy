"""Simplified Vulnerability Agent orchestration for tests."""

from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any, Dict, List

from backend.core.eventbus import EventBus
from backend.workers.celery_app import celery_app  # noqa: E402
from backend.workers.modules.nuclei_module import NucleiScanModule
from backend.workers.modules.webapp_test_module import WebAppTestModule
from backend.workers.modules.api_security_module import APISecurityModule
from backend.workers.modules.authz_tester import AuthorizationTester
from backend.workers.processors.vuln_validator import VulnValidator
from backend.workers.processors.finding_processor import FindingProcessor
from backend.core.cancellation import is_scan_cancelled


@celery_app.task(bind=True, name="vuln.start", queue="vuln_queue", autoretry_for=(Exception,), max_retries=1)
def start_vuln(self, scan_id: str, context: dict) -> Dict[str, Any]:
    return asyncio.run(_async_start_vuln(scan_id, context))


async def _async_start_vuln(scan_id: str, context: dict) -> Dict[str, Any]:
    start = time.time()
    data_dir = os.path.join(os.getcwd(), "backend", "data")
    os.makedirs(data_dir, exist_ok=True)

    findings: List[dict] = []

    # Nuclei
    nuclei = NucleiScanModule()
    nuclei_findings = await nuclei.run(scan_id, context, None)
    findings.extend(nuclei_findings)

    # Web app tests
    webmod = WebAppTestModule()
    web_findings = await webmod.run(scan_id, context, None)
    findings.extend(web_findings)

    # API tests
    apimod = APISecurityModule()
    api_findings = await apimod.run(scan_id, context, None)
    findings.extend(api_findings)

    # Authz tests
    authz = AuthorizationTester()
    authz_findings = await authz.run(scan_id, context, None)
    findings.extend(authz_findings)

    # Validate
    validator = VulnValidator()
    validated = await validator.validate_all(findings)

    # Process
    processor = FindingProcessor()
    count = await processor.process_all(scan_id, validated, None)

    summary = {
        "scan_id": scan_id,
        "total_findings": count,
        "findings": validated,
        "execution_time": time.time() - start,
    }
    EventBus().publish("vuln.completed", summary)

    # persist raw
    with open(os.path.join(data_dir, f"vuln_raw_{scan_id}.json"), "w", encoding="utf-8") as f:
        json.dump(findings, f)

    return summary
"""Vulnerability check agent Celery tasks."""

from typing import Any

@celery_app.task(bind=True, name="workers.vuln.run", autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def run(self, scan_id: int, target: str) -> dict[str, Any]:
    """Run the real vulnerability pipeline for the active scan."""

    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "target": target, "status": "cancelled", "findings": []}
    result = asyncio.run(
        _async_start_vuln(
            str(scan_id),
            {
                "scan_id": scan_id,
                "target": target,
                "task_id": self.request.id,
            },
        )
    )
    return {
        "scan_id": scan_id,
        "target": target,
        "findings": result.get("findings", []),
        "total_findings": result.get("total_findings", 0),
    }