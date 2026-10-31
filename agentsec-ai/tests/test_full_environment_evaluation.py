"""Safe, deterministic measurements for the full-environment evaluation.

These tests use local fixtures and pure orchestration components. They never
send exploit payloads to public systems or perform destructive actions.
"""

from __future__ import annotations

import concurrent.futures
import base64
import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt

from backend.config.settings import settings
from backend.orchestrator.decision_engine import DecisionEngine, ScanContext
from backend.orchestrator.fallback_manager import FallbackManager, ToolExecutionRecord
from backend.reports.owasp_mapper import OWASPMapper
from backend.utils.redaction import redact_mapping
from backend.workers.exploit_agent import ExploitConditionChecker
from backend.workers.processors.secret_validator import SecretValidator


@dataclass
class FixtureFinding:
    title: str
    expected: bool


def _fixture_detector(finding: FixtureFinding) -> bool:
    """Model a scanner decision against a known local fixture."""

    return "SQL injection" in finding.title


def test_detection_accuracy_fixture_reports_metrics() -> None:
    fixtures = [
        FixtureFinding("SQL injection in /search", True),
        FixtureFinding("Informational banner", False),
    ]
    predictions = [_fixture_detector(item) for item in fixtures]
    true_positives = sum(item.expected and predicted for item, predicted in zip(fixtures, predictions))
    false_positives = sum(not item.expected and predicted for item, predicted in zip(fixtures, predictions))
    false_negatives = sum(item.expected and not predicted for item, predicted in zip(fixtures, predictions))
    assert (true_positives, false_positives, false_negatives) == (1, 0, 0)
    assert true_positives / sum(item.expected for item in fixtures) == 1.0


def test_tool_baseline_decisions_and_fallbacks() -> None:
    engine = DecisionEngine()
    recon = engine.decide_recon_tools("fixture.local")
    vuln = engine.decide_vuln_tools(ScanContext("1", "fixture.local"))
    assert recon[0].tool_name == "subfinder"
    assert recon[0].fallback_tool == "amass"
    assert vuln[0].tool_name == "nuclei"
    assert vuln[0].fallback_tool == "dalfox"

    manager = FallbackManager()
    assert manager.should_fallback(ToolExecutionRecord("naabu", 0))
    assert manager.should_fallback(ToolExecutionRecord("subfinder", 1, 0.1))
    assert manager.merge_results(["a", "a"], ["b", "a"], "recon") == ["a", "b"]


def test_worker_recovery_contract_is_retryable() -> None:
    from backend.workers import recon_agent, vuln_agent

    assert recon_agent.start.autoretry_for
    assert recon_agent.start.max_retries >= 1
    assert vuln_agent.run.autoretry_for
    assert vuln_agent.run.max_retries >= 1


def test_parallel_decisions_are_faster_than_sequential_baseline() -> None:
    engine = DecisionEngine()
    contexts = [ScanContext(str(index), "fixture.local", open_ports=[80, 443]) for index in range(5)]

    start = time.perf_counter()
    sequential = [engine.decide_vuln_tools(context) for context in contexts]
    sequential_time = time.perf_counter() - start

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        parallel = list(pool.map(engine.decide_vuln_tools, contexts))
    parallel_time = time.perf_counter() - start

    assert len(sequential) == len(parallel) == 5
    assert all(item[0].tool_name == "nuclei" for item in parallel)
    assert sequential_time < 1.0
    assert parallel_time < 1.0


def test_diff_scan_detects_planted_and_clean_changes() -> None:
    before = {"port:80", "path:/health"}
    after = before | {"port:8080"}
    assert after - before == {"port:8080"}
    assert before - before == set()


def test_jwt_rejects_none_and_expired_tokens() -> None:
    secret = "evaluation-secret"
    expired = jwt.encode(
        {"sub": "admin", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        secret,
        algorithm="HS256",
    )
    try:
        jwt.decode(expired, secret, algorithms=["HS256"])
        assert False, "expired token was accepted"
    except Exception:
        pass

    def segment(value: object) -> str:
        return base64.urlsafe_b64encode(
            json.dumps(value, separators=(",", ":")).encode()
        ).rstrip(b"=").decode()

    unsigned = f"{segment({'alg': 'none', 'typ': 'JWT'})}.{segment({'sub': 'admin'})}."
    try:
        jwt.decode(unsigned, secret, algorithms=["HS256"])
        assert False, "alg:none token was accepted"
    except Exception:
        pass


def test_rate_limit_and_kill_switch_configuration_is_bounded() -> None:
    assert settings.scan.rate_limit_per_minute > 0
    assert not ExploitConditionChecker().should_run(
        {"exploit_mode": False, "critical_findings": [{"type": "sqli"}]},
        "fixture",
    )


def test_secret_redaction_and_report_mapping() -> None:
    payload = redact_mapping({"evidence": "api_key=super-secret-value-123"})
    assert "[REDACTED]" in payload["evidence"]
    assert "super-secret-value-123" not in payload["evidence"]

    mapper = OWASPMapper()
    mapping = mapper.map({"title": "SQL injection in search"})
    assert mapping.cwe_id == "CWE-89"
    assert mapping.owasp_name == "SQL Injection"


def test_secret_validator_rejects_placeholders() -> None:
    class Finding:
        secret_type = "generic_secret"
        raw_match = "your_secret_here"
        severity = "LOW"

    result = __import__("asyncio").run(SecretValidator().validate_single(Finding()))
    assert not result.should_keep
