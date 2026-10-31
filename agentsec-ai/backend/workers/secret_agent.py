from __future__ import annotations

import asyncio
import time
from typing import Any

from backend.config.settings import settings
from backend.plugins.base_plugin import PluginInput
from backend.plugins.executor import executor
from backend.workers.celery_app import celery_app
from backend.utils.redaction import redact_mapping
from backend.core.cancellation import is_scan_cancelled


@celery_app.task(bind=True, name="secrets.start", queue="secrets_queue", max_retries=1)
def start_secrets(self, scan_id: str, context_dict: dict) -> dict[str, Any]:
    """Start the secret and cloud analysis task."""
    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "status": "cancelled", "findings": []}
    return asyncio.run(_async_start_secrets(self, scan_id, context_dict))


async def _async_start_secrets(self, scan_id: str, context_dict: dict) -> dict[str, Any]:
    start = time.time()
    js_files = context_dict.get("js_files", [])
    repo_urls = context_dict.get("repo_urls", [])

    from backend.workers.modules.js_secret_extractor import JSSecretExtractor
    from backend.workers.modules.git_secret_scanner import GitSecretScanner
    from backend.workers.modules.cloud_security_module import CloudSecurityModule
    from backend.workers.processors.secret_validator import SecretValidator

    findings = []
    extractor = JSSecretExtractor()
    findings.extend(await extractor.run(scan_id, js_files, context_dict))

    git = GitSecretScanner()
    findings.extend(await git.run(scan_id, repo_urls, context_dict.get("target", "example.com"), None))

    cloud = CloudSecurityModule()
    findings.extend(await cloud.run(scan_id, context_dict.get("context") or type("Ctx", (), {"target": context_dict.get("target", "example.com")})(), None))

    validated = await SecretValidator().validate_all(findings, scan_id)
    summary = {
        "scan_id": scan_id,
        "secret_count": len(validated),
        "cloud_count": len([f for f in validated if getattr(f, "secret_type", "").startswith("cloud") or 1]),
        "critical_confirmed": sum(1 for f in validated if getattr(f, "severity", "").upper() == "CRITICAL"),
        "tools_run": ["js_secret_extractor", "git_secret_scanner", "cloud_security_module"],
        "execution_time": time.time() - start,
    }
    return summary


@celery_app.task(
    bind=True,
    name="workers.git.run",
    queue="secrets_queue",
    autoretry_for=(Exception,),
    max_retries=1,
)
def run_git_scan(
    self,
    scan_id: int,
    repository_url: str,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Scan an explicitly approved public Git repository with TruffleHog."""
    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "task_id": self.request.id, "status": "cancelled", "findings": []}
    from backend.plugins.registry import registry
    from backend.storage import FindingsStore

    registry.auto_discover()
    options = options or {}
    plugin_input = PluginInput(
        scan_id=str(scan_id),
        target=repository_url,
        task_id=self.request.id,
        timeout=settings.scan.tool_timeout_seconds,
        extra_params={
            key: value for key, value in options.items()
            if key in {"branch", "since_commit", "until_commit", "baseline"}
        },
    )
    output = executor.run("trufflehog", plugin_input)
    safe_findings = []
    for item in output.parsed:
        finding = dict(item)
        signature = "|".join(
            str(finding.get(key, "")).strip().lower()
            for key in ("DetectorName", "SourceMetadata", "Verified")
        )
        if signature in {str(item).strip().lower() for item in options.get("baseline", [])}:
            continue
        for key in ("Raw", "RawV2", "Secret", "secret", "token", "password"):
            if key in finding:
                finding[key] = "[REDACTED]"
        safe_findings.append(redact_mapping(finding))
    store = FindingsStore()
    for finding in safe_findings:
        detector = finding.get("DetectorName") or finding.get("detector") or "secret"
        source = finding.get("SourceMetadata") or {}
        data = source.get("Data", {}) if isinstance(source, dict) else {}
        github = data.get("Git") or data.get("Github") or {}
        location = (
            github.get("link")
            or github.get("repository")
            or repository_url
            if isinstance(github, dict)
            else repository_url
        )
        title = f"Git secret detected: {detector}"
        description = "TruffleHog reported a credential-like value in this repository. Secret values are redacted."
        if settings.storage_backend.lower() == "postgres":
            import asyncio

            asyncio.run(
                store.create_record_async(
                    title=title,
                    severity="high" if finding.get("Verified") else "medium",
                    scan_id=scan_id,
                    task_id=self.request.id,
                    affected_url=str(location),
                    description=description,
                    evidence=finding,
                )
            )
        else:
            store.create_record(
                title=title,
                severity="high" if finding.get("Verified") else "medium",
                scan_id=scan_id,
                task_id=self.request.id,
                affected_url=str(location),
                description=description,
                evidence=finding,
            )
    if is_scan_cancelled(scan_id):
        return {"scan_id": scan_id, "task_id": self.request.id, "status": "cancelled", "findings": []}
    return redact_mapping({
        "scan_id": scan_id,
        "task_id": self.request.id,
        "tool_name": "trufflehog",
        "status": output.status,
        "success": output.success,
        "exit_code": output.exit_code,
        "timed_out": output.timed_out,
        "unavailable": output.unavailable,
        "command_executed": output.command_executed,
        "execution_time": output.execution_time,
        "finding_count": len(safe_findings),
        "findings": safe_findings,
        "suppressed_count": len(output.parsed) - len(safe_findings),
        "error": output.error_message,
    })


__all__ = ["start_secrets", "_async_start_secrets", "run_git_scan"]
