"""Rule-based tool selection for AgentSec AI scans."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ScanContext:
    scan_id: str
    target: str
    has_wordpress: bool = False
    open_ports: list[int] | None = None
    technologies: list[str] | None = None
    scan_type: str = "FULL"


@dataclass(slots=True)
class ToolDecision:
    tool_name: str
    priority: int
    fallback_tool: str | None = None


class DecisionEngine:
    """Pure logic engine for selecting tools for a scan."""

    def decide_recon_tools(self, target: str) -> list[ToolDecision]:
        return [
            ToolDecision("subfinder", 1, "amass"),
            ToolDecision("amass", 2, "assetfinder"),
            ToolDecision("assetfinder", 3, "findomain"),
            ToolDecision("findomain", 4, None),
        ]

    def decide_enum_tools(self, recon_results: dict[str, Any]) -> list[ToolDecision]:
        return [
            ToolDecision("httpx", 1, "naabu"),
            ToolDecision("naabu", 2, "nmap"),
            ToolDecision("nmap", 3, "whatweb"),
            ToolDecision("whatweb", 4, "katana"),
            ToolDecision("katana", 5, None),
        ]

    def decide_vuln_tools(self, context: ScanContext) -> list[ToolDecision]:
        decisions: list[ToolDecision] = [
            ToolDecision("nuclei", 1, "dalfox"),
            ToolDecision("sqlmap", 2, None),
            ToolDecision("dalfox", 3, None),
        ]
        if context.has_wordpress:
            decisions.append(ToolDecision("wpscan", 4, None))
        if context.open_ports and 445 in context.open_ports:
            decisions.append(ToolDecision("nmap_smb_scripts", 5, None))
        decisions.extend([
            ToolDecision("corsy", 6, None),
            ToolDecision("tplmap", 7, None),
            ToolDecision("wapiti", 8, None),
        ])
        return decisions

    def decide_secrets_tools(self, context: ScanContext) -> list[ToolDecision]:
        return [
            ToolDecision("trufflehog", 1, "secretfinder"),
            ToolDecision("secretfinder", 2, "linkfinder"),
            ToolDecision("linkfinder", 3, None),
            ToolDecision("cloud_enum", 4, None),
        ]

    def get_fallback_tool(self, tool_name: str) -> str | None:
        fallback_map = {
            "subfinder": "amass",
            "amass": "assetfinder",
            "assetfinder": "findomain",
            "httpx": "naabu",
            "naabu": "nmap",
            "nmap": "whatweb",
            "whatweb": "katana",
            "nuclei": "dalfox",
            "trufflehog": "secretfinder",
            "secretfinder": "linkfinder",
        }
        return fallback_map.get(tool_name)


__all__ = ["DecisionEngine", "ScanContext", "ToolDecision"]
