"""Runtime preflight checks for registered security tools."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from backend.config.settings import settings
from backend.plugins.registry import registry


@dataclass
class PreflightResult:
    name: str
    category: str
    binary: str
    status: str
    version: str | None = None
    detail: str = ""
    resources: list[str] | None = None


def _version(binary: str, name: str) -> str:
    """Use known version flags; some security tools intentionally have none."""

    commands = {
        "assetfinder": [[binary, "-h"]],
        "cloud_enum": [[binary, "-h"]],
        "dalfox": [[binary, "version"], [binary, "--version"]],
        "ffuf_plugin": [[binary, "-V"], [binary, "--version"]],
        "waybackurls": [[binary, "-h"]],
    }.get(name, [[binary, "--version"]])
    for command in commands:
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=5, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        output = (result.stdout or result.stderr).strip()
        if output:
            return output[:500]
    return "version unavailable"


def run_preflight() -> list[dict[str, Any]]:
    """Check executable and tool-specific resources without running scans."""

    registry.auto_discover()
    results: list[dict[str, Any]] = []
    python_tools = {"cloud_enum", "corsy", "secretfinder", "linkfinder", "tplmap"}
    required_resources = {
        "dnsx": [settings.tools.dns_wordlist],
        "ffuf_plugin": [settings.tools.directory_wordlist],
        "nuclei_plugin": [
            os.path.join(settings.tools.nuclei_templates_path, "http", "misconfiguration"),
            os.path.join(settings.tools.nuclei_templates_path, "http", "exposures"),
        ],
        "corsy": ["/opt/agentsec-tools/Corsy/corsy.py"],
        "secretfinder": ["/opt/agentsec-tools/SecretFinder/SecretFinder.py"],
        "linkfinder": ["/opt/agentsec-tools/LinkFinder/linkfinder.py"],
        "tplmap": ["/opt/agentsec-tools/tplmap/tplmap.py"],
        "cloud_enum": ["/opt/agentsec-tools/cloud_enum"],
    }
    for metadata in registry.list_all():
        name = metadata["name"]
        binary = (
            "/opt/agentsec-tools/venv/bin/cloud_enum"
            if name == "cloud_enum"
            else "/opt/agentsec-tools/venv/bin/python"
            if name in python_tools
            else metadata.get("binary_name") or name
        )
        resources = required_resources.get(name, [])
        if not shutil.which(binary) and not Path(binary).exists():
            result = PreflightResult(
                name, metadata.get("category", "misc"), binary, "MISSING_BINARY",
                detail=f"executable not found: {binary}", resources=resources,
            )
        elif any(not os.access(path, os.R_OK) for path in resources):
            result = PreflightResult(
                name, metadata.get("category", "misc"), binary, "MISSING_WORDLIST" if name in {"dnsx", "ffuf_plugin"} else "MISSING_TEMPLATE" if name == "nuclei_plugin" else "MISSING_SCRIPT",
                detail="required resource is missing or unreadable", resources=resources,
            )
        else:
            version = _version(binary, name)
            result = PreflightResult(
                name, metadata.get("category", "misc"), binary,
                "READY",
                version=version, detail="ready" if version != "version unavailable" else "ready; version flag unavailable",
                resources=resources,
            )
        results.append(asdict(result))
    return results
