"""Base plugin abstractions and data contracts for AgentSec AI plugins.

This module defines small dataclasses and an abstract base plugin class
used by the registry and executor. Implementations in the `plugins` package
should subclass `AbstractPlugin` and register themselves with the
`registry.register` decorator (see `registry.py`).
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import json
import shlex
import shutil
import subprocess
import time
import logging
import re
import os
import threading
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit
from xml.etree import ElementTree

from backend.core.eventbus import EventBus
from backend.core.cancellation import is_scan_cancelled
from backend.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class PluginInput:
    scan_id: str
    target: str
    extra_params: Dict[str, Any] = field(default_factory=dict)
    rate_limit: int = 150
    timeout: Optional[int] = None
    task_id: Optional[str] = None


@dataclass
class PluginOutput:
    scan_id: str
    tool_name: str = ""
    raw: str = ""
    parsed: List[Dict[str, Any]] = field(default_factory=list)
    quality_score: float = 0.0
    executed_at: datetime = field(default_factory=datetime.utcnow)
    success: bool = True
    raw_output: str = ""
    parsed_data: List[Dict[str, Any]] = field(default_factory=list)
    record_count: int = 0
    execution_time: float = 0.0
    error_message: Optional[str] = None
    command_executed: Optional[str] = None
    output_file_path: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    status: str = "success"
    exit_code: Optional[int] = None
    timed_out: bool = False
    unavailable: bool = False


@dataclass
class PluginMetadata:
    name: str
    description: str = ""
    version: str = "1.0.0"
    category: str = "misc"
    enabled: bool = True
    binary_name: Optional[str] = None
    fallback_plugin: Optional[str] = None
    default_timeout: int = 60
    supports_json_output: bool = False


class PluginNotInstalledError(Exception):
    pass


class PluginParseError(Exception):
    pass


class AbstractPlugin(ABC):
    """Base class for all plugins.

    Subclasses should implement `execute` (sync or async) and
    `health_check`.
    """

    metadata: PluginMetadata

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        self.settings = settings or {}

    def build_command(self, inp: PluginInput) -> List[str]:
        """Build a safe, tool-specific argv without invoking a shell."""
        binary = self.metadata.binary_name or self.metadata.name
        python_tool = "/opt/agentsec-tools/venv/bin/python"
        target = inp.target.strip()
        parsed_target = urlparse(target if "://" in target else f"//{target}")
        host = parsed_target.hostname or target.split("/", maxsplit=1)[0]
        target_url = target if "://" in target else f"https://{target}"
        params = inp.extra_params
        timeout_seconds = inp.timeout or self.metadata.default_timeout

        commands = {
            "subfinder": [binary, "-d", host, "-silent"],
            "amass": [
                binary,
                "enum",
                "-passive",
                "-d",
                host,
                "-timeout",
                str(max(1, (timeout_seconds + 59) // 60)),
            ],
            "assetfinder": [binary, "--subs-only", host],
            "findomain": [binary, "-t", host, "--quiet"],
            "dnsx": [binary, "-d", host, "-w", settings.tools.dns_wordlist, "-silent"],
            "httpx_plugin": [binary, "-u", target, "-json", "-silent"],
            "naabu": [binary, "-host", host, "-json", "-silent"],
            "rustscan": [binary, "-a", host, "-g"],
            "nmap_plugin": [binary, "-sV", "-oX", "-", host],
            "nuclei_plugin": [
                binary,
                "-u",
                target,
                "-t",
                ",".join(
                    [
                        os.path.join(settings.tools.nuclei_templates_path, "http", "misconfiguration"),
                        os.path.join(settings.tools.nuclei_templates_path, "http", "exposures"),
                    ]
                ),
                "-jsonl",
                "-silent",
                "-duc",
                "-ni",
                "-c",
                "10",
                "-rl",
                "50",
                "-bs",
                "10",
            ],
            "katana": [binary, "-u", target, "-jsonl", "-silent"],
            "dalfox": [binary, "url", target, "--silence", "--format", "json"],
            "sqlmap_plugin": [
                binary, "-u", target, "--batch", "--risk=1", "--level=1",
                "--disable-coloring",
            ],
            "gau": [binary, "--json", host],
            "whatweb": [binary, "--log-json=-", target],
            "trufflehog": [
                binary, "git", target, "--json",
                *(
                    ["--branch", str(params["branch"])]
                    if params.get("branch") else []
                ),
                *(["--since-commit", str(params["since_commit"])] if params.get("since_commit") else []),
                *(["--until-commit", str(params["until_commit"])] if params.get("until_commit") else []),
            ],
            "wpscan_plugin": [binary, "--url", target, "--no-update", "--format", "json"],
            "ffuf_plugin": [
                binary,
                "-u",
                target_url.rstrip("/") + "/FUZZ",
                "-w",
                str(params.get("wordlist", settings.tools.directory_wordlist)),
                "-json",
                "-s",
            ],
            "linkfinder": [
                binary,
                "/opt/agentsec-tools/LinkFinder/linkfinder.py",
                "-i",
                target_url,
                "-o",
                "cli",
            ],
            "secretfinder": [
                binary,
                "/opt/agentsec-tools/SecretFinder/SecretFinder.py",
                "-i",
                target_url,
                "-o",
                "cli",
            ],
            "corsy": [
                binary,
                "/opt/agentsec-tools/Corsy/corsy.py",
                "-u",
                target_url,
            ],
            "cloud_enum": [
                "/opt/agentsec-tools/venv/bin/cloud_enum",
                "-k",
                host.split(".", maxsplit=1)[0],
            ],
            "tplmap": [
                binary,
                "/opt/agentsec-tools/tplmap/tplmap.py",
                "-u",
                target_url,
                "--batch",
            ],
        }
        python_commands = {
            "linkfinder": [
                python_tool,
                "/opt/agentsec-tools/LinkFinder/linkfinder.py",
                "-i",
                target_url,
                "-o",
                "cli",
            ],
            "secretfinder": [
                python_tool,
                "/opt/agentsec-tools/SecretFinder/SecretFinder.py",
                "-i",
                target_url,
                "-o",
                "cli",
            ],
            "corsy": [
                python_tool,
                "/opt/agentsec-tools/Corsy/corsy.py",
                "-u",
                target_url,
            ],
            "tplmap": [
                python_tool,
                "/opt/agentsec-tools/tplmap/tplmap.py",
                "-u",
                target,
                "--batch",
            ],
        }
        commands.update(python_commands)
        command = commands.get(self.metadata.name)
        if command is None:
            raise NotImplementedError(
                f"No safe command adapter is configured for {self.metadata.name}"
            )

        return command

    def parse_output(self, raw: str) -> List[Dict[str, Any]]:
        """Parse newline-delimited JSON or preserve useful text as records."""
        if self.metadata.name == "nmap_plugin":
            try:
                root = ElementTree.fromstring(raw)
            except ElementTree.ParseError:
                return []
            records: List[Dict[str, Any]] = []
            for host in root.findall("host"):
                address = host.find("address")
                for port in host.findall("./ports/port"):
                    state = port.find("state")
                    if state is None or state.get("state") != "open":
                        continue
                    service = port.find("service")
                    records.append(
                        {
                            "host": address.get("addr") if address is not None else "",
                            "port": port.get("portid"),
                            "protocol": port.get("protocol"),
                            "service": service.get("name") if service is not None else "",
                        }
                    )
            return records

        records: List[Dict[str, Any]] = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                value = {"value": line}
            if isinstance(value, dict):
                records.append(value)
            else:
                records.append({"value": value})
        return records

    def execute(self, inp: PluginInput) -> PluginOutput:
        """Execute a local security tool without raising tool-level failures."""
        started = time.monotonic()
        command: List[str] = []
        try:
            command = self.build_command(inp)
            self._publish_command_event(
                inp,
                {
                    "event": "tool.command_started",
                    "scan_id": inp.scan_id,
                    "task_id": inp.task_id,
                    "tool_name": self.metadata.name,
                    "command": self._format_command(command),
                    "status": "running",
                },
            )
            process_kwargs: Dict[str, Any] = {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "text": True,
                "start_new_session": True,
            }
            completed = subprocess.Popen(
                command,
                **process_kwargs,
            )
            stdout_chunks: List[str] = []
            stderr_chunks: List[str] = []

            def drain(stream: Any, chunks: List[str]) -> None:
                for chunk in iter(stream.readline, ""):
                    chunks.append(chunk)
                stream.close()

            stdout_thread = threading.Thread(
                target=drain,
                args=(completed.stdout, stdout_chunks),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=drain,
                args=(completed.stderr, stderr_chunks),
                daemon=True,
            )
            stdout_thread.start()
            stderr_thread.start()
            deadline = time.monotonic() + (inp.timeout or self.metadata.default_timeout)
            while completed.poll() is None:
                if is_scan_cancelled(inp.scan_id):
                    self._terminate_process(completed)
                    completed.wait()
                    stdout_thread.join(timeout=2)
                    stderr_thread.join(timeout=2)
                    stdout = "".join(stdout_chunks)
                    return PluginOutput(
                        scan_id=inp.scan_id,
                        tool_name=self.metadata.name,
                        raw=stdout or "",
                        raw_output=stdout or "",
                        success=False,
                        execution_time=time.monotonic() - started,
                        command_executed=shlex.join(command),
                        error_message="scan cancellation requested",
                        status="cancelled",
                        exit_code=completed.returncode,
                        extra={"tool_version": self.metadata.version},
                    )
                if time.monotonic() >= deadline:
                    self._terminate_process(completed)
                    completed.wait()
                    stdout_thread.join(timeout=2)
                    stderr_thread.join(timeout=2)
                    raise subprocess.TimeoutExpired(
                        command,
                        inp.timeout,
                        "".join(stdout_chunks),
                        "".join(stderr_chunks),
                    )
                time.sleep(0.1)
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            stdout = "".join(stdout_chunks)
            stderr = "".join(stderr_chunks)
            raw = stdout
            self._publish_tool_events(inp, raw, stderr)
            self._publish_command_event(
                inp,
                {
                    "event": "tool.command_finished",
                    "scan_id": inp.scan_id,
                    "task_id": inp.task_id,
                    "tool_name": self.metadata.name,
                    "exit_code": completed.returncode,
                    "status": "completed" if completed.returncode == 0 else "failed",
                },
            )
            parsed = self.parse_output(raw) if completed.returncode == 0 else []
            return PluginOutput(
                scan_id=inp.scan_id,
                tool_name=self.metadata.name,
                raw=raw,
                raw_output=raw,
                parsed=parsed,
                parsed_data=parsed,
                record_count=len(parsed),
                quality_score=min(1.0, len(parsed) / 10),
                success=completed.returncode == 0,
                execution_time=time.monotonic() - started,
                command_executed=shlex.join(command),
                error_message=None if completed.returncode == 0 else stderr.strip() or raw,
                status="success" if completed.returncode == 0 and parsed else (
                    "success_no_results" if completed.returncode == 0 else "failed"
                ),
                exit_code=completed.returncode,
                extra={"tool_version": self.metadata.version},
            )
        except (
            FileNotFoundError,
            subprocess.TimeoutExpired,
            OSError,
            NotImplementedError,
        ) as exc:
            if command:
                self._publish_command_event(
                    inp,
                    {
                        "event": "tool.command_finished",
                        "scan_id": inp.scan_id,
                        "task_id": inp.task_id,
                        "tool_name": self.metadata.name,
                        "status": "failed",
                        "error": str(exc),
                    },
                )
            logger.warning(
                "Plugin %s could not execute for scan %s: %s",
                self.metadata.name,
                inp.scan_id,
                exc,
            )
            return PluginOutput(
                scan_id=inp.scan_id,
                tool_name=self.metadata.name,
                raw=str(getattr(exc, "output", "") or ""),
                raw_output=str(getattr(exc, "output", "") or ""),
                success=False,
                execution_time=time.monotonic() - started,
                command_executed=shlex.join(command),
                error_message=str(getattr(exc, "stderr", "") or str(exc)),
                status=(
                    "unavailable"
                    if isinstance(exc, FileNotFoundError)
                    else "timed_out"
                    if isinstance(exc, subprocess.TimeoutExpired)
                    else "failed"
                ),
                timed_out=isinstance(exc, subprocess.TimeoutExpired),
                unavailable=isinstance(exc, FileNotFoundError),
                extra={"tool_version": self.metadata.version},
            )

    @staticmethod
    def _terminate_process(process: subprocess.Popen[str]) -> None:
        """Stop the complete process group, including tool child processes."""
        if process.poll() is not None:
            return
        if os.name == "nt":
            process.kill()
        else:
            os.killpg(process.pid, 9)

    @staticmethod
    def _format_command(command: List[str]) -> str:
        """Shell-escape argv for display while redacting credentials in URLs/options."""

        redacted: List[str] = []
        redact_next = False
        for argument in command:
            if redact_next:
                redacted.append("[REDACTED]")
                redact_next = False
                continue
            if re.match(r"^--?(?:api[-_]?key|token|password|secret|auth)(?:=|$)", argument, re.I):
                if "=" in argument:
                    redacted.append(argument.split("=", 1)[0] + "=[REDACTED]")
                else:
                    redacted.append(argument)
                    redact_next = True
                continue
            try:
                parsed = urlsplit(argument)
                if parsed.scheme in {"http", "https"} and parsed.hostname:
                    host = parsed.hostname
                    if ":" in host and not host.startswith("["):
                        host = f"[{host}]"
                    if parsed.port:
                        host = f"{host}:{parsed.port}"
                    netloc = f"[REDACTED]@{host}" if parsed.username or parsed.password else host
                    query = urlencode(
                        [
                            (key, "[REDACTED]" if re.search(
                                r"(token|key|secret|password|auth|signature|credential|session)",
                                key,
                                re.I,
                            ) else value)
                            for key, value in parse_qsl(parsed.query, keep_blank_values=True)
                        ]
                    )
                    argument = urlunsplit(
                        (parsed.scheme, netloc, parsed.path, query, parsed.fragment)
                    )
            except ValueError:
                pass
            redacted.append(argument)
        return shlex.join(redacted)

    def _publish_tool_events(self, inp: PluginInput, stdout: str, stderr: str) -> None:
        """Publish bounded terminal and attempt events for tool output."""

        bus = EventBus()
        from backend.orchestrator.event_bus import event_bus as redis_event_bus

        lines = [
            ("stdout", line) for line in stdout.splitlines()[-200:]
        ] + [("stderr", line) for line in stderr.splitlines()[-200:]]
        for attempt_number, (stream, line) in enumerate(lines, start=1):
            payload = {
                "scan_id": inp.scan_id,
                "task_id": inp.task_id,
                "tool_name": self.metadata.name,
                "line": line[:4000],
                "stream": stream,
            }
            bus.publish("tool.terminal_line", payload)
            self._publish_redis_event(
                redis_event_bus,
                inp.scan_id,
                {"event": "tool.terminal_line", **payload},
            )
            if stream == "stdout" and re.search(
                r"(testing|payload|template|request|fuzz|matched)", line, re.I
            ):
                attempt = {
                    **payload,
                    "attempt_number": attempt_number,
                    "payload_sample": line[:240],
                }
                bus.publish("tool.attempt", attempt)
                self._publish_redis_event(
                    redis_event_bus,
                    inp.scan_id,
                    {"event": "tool.attempt", **attempt},
                )

    @staticmethod
    def _publish_command_event(inp: PluginInput, event: Dict[str, Any]) -> None:
        bus = EventBus()
        from backend.orchestrator.event_bus import event_bus as redis_event_bus

        bus.publish(event["event"], event)
        AbstractPlugin._publish_redis_event(redis_event_bus, inp.scan_id, event)

    @staticmethod
    def _publish_redis_event(redis_event_bus: Any, scan_id: str, event: dict[str, Any]) -> None:
        """Persist a tool event for authenticated WebSocket clients."""

        try:
            redis_event_bus.publish_to_websocket_sync(str(scan_id), event)
        except Exception:
            logger.debug("Unable to publish tool event for scan %s", scan_id, exc_info=True)

    def health_check(self) -> bool:
        """Return whether the configured binary is available."""
        return bool(shutil.which(self.metadata.binary_name or self.metadata.name))
