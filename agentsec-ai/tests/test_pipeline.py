"""Phase 14 pipeline decision and normalization tests."""

import pytest

from backend.orchestrator.decision_engine import DecisionEngine, ScanContext


@pytest.mark.agent
def test_decision_engine_selects_wordpress_and_smb_checks() -> None:
    """Context-sensitive vulnerability tools are selected deterministically."""

    decisions = DecisionEngine().decide_vuln_tools(
        ScanContext("scan-1", "example.com", has_wordpress=True, open_ports=[445])
    )
    names = {decision.tool_name for decision in decisions}
    assert {"wpscan", "nmap_smb_scripts", "nuclei"} <= names


@pytest.mark.agent
def test_secrets_pipeline_does_not_select_removed_gitleaks() -> None:
    decisions = DecisionEngine().decide_secrets_tools(
        ScanContext("scan-2", "example.com")
    )
    assert all(decision.tool_name != "gitleaks" for decision in decisions)
    assert DecisionEngine().get_fallback_tool("trufflehog") == "secretfinder"
