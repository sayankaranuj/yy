import asyncio
import json
import os

from backend.plugins.base_plugin import PluginInput, PluginOutput
from backend.plugins.executor import executor
from backend.plugins.subfinder import Plugin as SubfinderPlugin
from backend.plugins.nmap_plugin import Plugin as NmapPlugin
from backend.plugins.health_checker import HealthChecker
from backend.config.settings import settings
from backend.storage import FindingsStore
from backend.workers.enum_agent import _run_selected_tools
from backend.workers.modules.cloud_security_module import CloudSecurityModule
from backend.workers.modules.nuclei_module import NucleiScanModule
from backend.workers.processors.finding_processor import FindingProcessor


def test_subfinder_command_uses_domain_argument() -> None:
    plugin = SubfinderPlugin()

    assert plugin.build_command(
        PluginInput(scan_id="1", target="https://example.com/path")
    ) == ["subfinder", "-d", "example.com", "-silent"]


def test_amass_command_has_a_bounded_enumeration_timeout() -> None:
    from backend.plugins.amass import Plugin as AmassPlugin

    command = AmassPlugin().build_command(
        PluginInput(scan_id="2", target="https://example.com", timeout=125)
    )

    assert command[:5] == ["amass", "enum", "-passive", "-d", "example.com"]
    assert command[-2:] == ["-timeout", "3"]


def test_amass_execution_caps_scan_wide_timeout(monkeypatch) -> None:
    from backend.plugins.amass import Plugin as AmassPlugin
    from backend.plugins.base_plugin import AbstractPlugin

    received = []

    def fake_execute(_plugin, plugin_input):
        received.append(plugin_input.timeout)
        return PluginOutput(scan_id=plugin_input.scan_id, tool_name="amass")

    monkeypatch.setattr(AbstractPlugin, "execute", fake_execute)
    AmassPlugin().execute(
        PluginInput(scan_id="3", target="example.com", timeout=300)
    )

    assert received == [120]


def test_dnsx_command_includes_required_wordlist() -> None:
    from backend.plugins.dnsx import Plugin as DnsxPlugin

    command = DnsxPlugin().build_command(
        PluginInput(scan_id="2", target="https://example.com:8443/")
    )

    assert command[:4] == ["dnsx", "-d", "example.com", "-w"]
    assert command[-1] == "-silent"


def test_url_scanners_normalize_bare_domains_to_http_urls() -> None:
    from backend.plugins.corsy import Plugin as CorsyPlugin
    from backend.plugins.ffuf_plugin import Plugin as FfufPlugin

    corsy = CorsyPlugin().build_command(
        PluginInput(scan_id="5", target="example.com")
    )
    ffuf = FfufPlugin().build_command(
        PluginInput(scan_id="5", target="example.com")
    )

    assert corsy[-1] == "https://example.com"
    assert ffuf[2] == "https://example.com/FUZZ"


def test_nuclei_command_uses_configured_templates() -> None:
    from backend.plugins.nuclei_plugin import Plugin as NucleiPlugin

    command = NucleiPlugin().build_command(
        PluginInput(scan_id="6", target="https://example.com")
    )

    assert command == [
        "nuclei",
        "-u",
        "https://example.com",
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
    ]


def test_terminal_command_format_redacts_url_and_option_credentials() -> None:
    from backend.plugins.base_plugin import AbstractPlugin

    command = AbstractPlugin._format_command(
        [
            "nuclei",
            "-u",
            "https://operator:secret@example.org/check?api_key=private&view=full",
            "--token",
            "hidden-token",
        ]
    )

    assert "secret" not in command
    assert "private" not in command
    assert "hidden-token" not in command
    assert "[REDACTED]@example.org" in command
    assert "view=full" in command


def test_plugin_health_does_not_report_missing_script_adapters_as_ready(
    monkeypatch,
) -> None:
    class StubRegistry:
        @staticmethod
        def list_all():
            return [{"name": "linkfinder", "binary_name": "python"}]

    monkeypatch.setattr(
        HealthChecker,
        "check_binary_exists",
        staticmethod(lambda binary: binary == "python"),
    )
    result = asyncio.run(HealthChecker.check_all(StubRegistry()))[0]

    assert result.ok is False
    assert "linkfinder.py" in result.detail


def test_nmap_parser_returns_only_open_ports() -> None:
    plugin = NmapPlugin()
    output = """<?xml version="1.0"?>
    <nmaprun>
      <host><address addr="192.0.2.10" addrtype="ipv4"/><ports>
        <port protocol="tcp" portid="443"><state state="open"/>
          <service name="https"/>
        </port>
        <port protocol="tcp" portid="22"><state state="closed"/></port>
      </ports></host>
    </nmaprun>"""

    assert plugin.parse_output(output) == [
        {
            "host": "192.0.2.10",
            "port": "443",
            "protocol": "tcp",
            "service": "https",
        }
    ]


def test_enumeration_worker_returns_real_tool_results(monkeypatch) -> None:
    def fake_run(name, tool_input):
        output_by_name = {
            "httpx": ("httpx_plugin", [{"url": "https://example.com", "status_code": 200}]),
            "naabu": ("naabu", [{"host": "example.com", "port": 443}]),
            "katana": ("katana", [{"url": "https://example.com/login"}]),
        }
        actual_name, parsed = output_by_name[name]
        assert tool_input.target == "example.com"
        assert tool_input.task_id == "celery-task-15"
        return PluginOutput(
            scan_id=tool_input.scan_id,
            tool_name=actual_name,
            success=True,
            parsed=parsed,
            record_count=len(parsed),
            command_executed=f"{name} --target example.com",
        )

    monkeypatch.setattr(executor, "run", fake_run)
    result = asyncio.run(_run_selected_tools(15, "example.com", None, "celery-task-15"))

    assert result["status"] == "completed"
    assert result["live_hosts"] == 1
    assert result["open_ports"] == 1
    assert result["endpoint_count"] == 1
    assert {item["tool"] for item in result["tools"]} == {
        "httpx_plugin",
        "naabu",
        "katana",
    }
    assert all(item["success"] for item in result["tools"])
    assert result["tools"][0]["command_executed"] == "httpx --target example.com"


def test_nuclei_unavailable_does_not_create_a_synthetic_finding(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        executor,
        "run",
        lambda *_: PluginOutput(
            scan_id="16",
            tool_name="nuclei_plugin",
            success=False,
            error_message="nuclei binary unavailable",
        ),
    )

    findings = asyncio.run(
        NucleiScanModule().run("16", {"target": "example.com"}, None)
    )

    assert findings == []
    assert json.loads((tmp_path / "backend" / "data" / "nuclei_16.json").read_text()) == []


def test_nuclei_results_are_normalized_and_persisted_for_the_findings_api(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(settings, "storage_backend", "json")
    monkeypatch.setattr(
        executor,
        "run",
        lambda *_: PluginOutput(
            scan_id="18",
            tool_name="nuclei_plugin",
            success=True,
            record_count=1,
            parsed=[
                {
                    "template-id": "sample-template",
                    "matched-at": "https://example.com/path",
                    "info": {"name": "Sample finding", "severity": "medium"},
                    "matcher-name": "header-check",
                }
            ],
        ),
    )
    findings = asyncio.run(
        NucleiScanModule().run("18", {"target": "example.com"}, None)
    )

    assert findings == [
        {
            "title": "Sample finding",
            "severity": "MEDIUM",
            "affected_url": "https://example.com/path",
            "evidence": "header-check",
            "cve_id": None,
            "tool_found_by": "nuclei",
        }
    ]
    assert asyncio.run(FindingProcessor().process_all("18", findings, None)) == 1
    assert any(
        record["title"] == "Sample finding"
        for record in FindingsStore().list_records()
    )


def test_cloud_module_does_not_report_guessed_bucket_names_as_findings() -> None:
    findings = CloudSecurityModule()._scan_s3_buckets(
        "17", type("Context", (), {"target": "example.com"})()
    )

    assert findings == []
