"""Cheap performance guardrails for pure pipeline utilities."""

import time

import pytest

from backend.orchestrator.decision_engine import DecisionEngine, ScanContext


@pytest.mark.slow
def test_decision_engine_handles_large_port_context() -> None:
    """Rule evaluation stays comfortably below the interactive threshold."""

    start = time.perf_counter()
    for _ in range(5000):
        DecisionEngine().decide_vuln_tools(
            ScanContext("scan", "example.com", open_ports=list(range(1, 1000)))
        )
    assert time.perf_counter() - start < 1.0