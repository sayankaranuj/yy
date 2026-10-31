"""Health checking utilities for plugins.

This module provides simple checks used by the tool-management dashboard
and startup health validations.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class HealthResult:
    plugin_name: str
    ok: bool
    detail: Optional[str]
    checked_at: datetime


class HealthChecker:
    @staticmethod
    def check_binary_exists(binary_name: str) -> bool:
        return shutil.which(binary_name) is not None

    @staticmethod
    def check_binary_version(binary_name: str, version_flag: str = "--version") -> Optional[str]:
        try:
            out = subprocess.run([binary_name, version_flag], capture_output=True, text=True, timeout=5)
            if out.returncode == 0:
                return out.stdout.strip() or out.stderr.strip()
        except Exception:
            return None
        return None

    @staticmethod
    async def check_one(
        plugin_name: str,
        binary_name: Optional[str] = None,
        required_paths: Optional[list[str]] = None,
    ) -> HealthResult:
        ok = True
        detail = None
        if binary_name:
            exists = HealthChecker.check_binary_exists(binary_name)
            ok = exists
            detail = None if exists else f"missing executable: {binary_name}"
        missing_paths = [
            path for path in (required_paths or []) if not Path(path).exists()
        ]
        if missing_paths:
            ok = False
            detail = "missing required files: " + ", ".join(missing_paths)
        if ok:
            detail = "ready"

        return HealthResult(plugin_name=plugin_name, ok=ok, detail=detail, checked_at=datetime.utcnow())

    @staticmethod
    async def check_all(registry) -> list[HealthResult]:
        runtime_binaries = {
            "cloud_enum": "/opt/agentsec-tools/venv/bin/cloud_enum",
            "corsy": "/opt/agentsec-tools/venv/bin/python",
            "linkfinder": "/opt/agentsec-tools/venv/bin/python",
            "secretfinder": "/opt/agentsec-tools/venv/bin/python",
            "tplmap": "/opt/agentsec-tools/venv/bin/python",
        }
        required_paths = {
            "corsy": ["/opt/agentsec-tools/Corsy/corsy.py"],
            "cloud_enum": ["/opt/agentsec-tools/cloud_enum"],
            "linkfinder": ["/opt/agentsec-tools/LinkFinder/linkfinder.py"],
            "secretfinder": ["/opt/agentsec-tools/SecretFinder/SecretFinder.py"],
            "tplmap": ["/opt/agentsec-tools/tplmap/tplmap.py"],
        }
        results = []
        for meta in registry.list_all():
            name = meta.get("name")
            binary = runtime_binaries.get(name, meta.get("binary_name") or name)
            results.append(
                await HealthChecker.check_one(
                    name,
                    binary,
                    required_paths.get(name),
                )
            )
        return results


health_checker = HealthChecker()
