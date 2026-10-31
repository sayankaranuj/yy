from types import SimpleNamespace

import pytest

from backend.workers.modules.js_secret_extractor import JSSecretExtractor, SecretFinding
from backend.workers.processors.secret_validator import SecretValidator
from backend.workers.modules.cloud_security_module import CloudSecurityModule, generate_bucket_names
from backend.workers.processors.immediate_notifier import ImmediateNotifier
from backend.workers.modules.git_secret_scanner import GitSecretScanner


def test_regex_extractor_finds_aws_key():
    extractor = JSSecretExtractor()
    findings = extractor._regex_extract("const key = 'AKIAIOSFODNN7EXAMPLE'", "https://example.com/app.js")
    assert any(f.title == "AWS Access Key ID Exposed" for f in findings)
    assert findings[0].raw_match.endswith("...")
    assert findings[0].severity == "CRITICAL"


def test_regex_extractor_skips_placeholder():
    extractor = JSSecretExtractor()
    findings = extractor._regex_extract("const password = 'your_password_here'", "https://example.com/app.js")
    assert findings == []


def test_secret_validator_filters_placeholder():
    SecretValidator()
    SecretFinding(
        secret_type="generic_password",
        title="Hardcoded Password Found",
        severity="HIGH",
        raw_match="changeme",
        context_snippet="value",
        source_url="https://example.com",
        line_number=1,
        tool_found_by="regex",
    )
    result = pytest.run(asyncio=False, args=[], plugins=[])
    assert result is None


def test_secret_validator_keeps_real_secret():
    validator = SecretValidator()
    finding = SecretFinding(
        secret_type="generic_secret",
        title="Hardcoded Secret Found",
        severity="HIGH",
        raw_match="AbCdEfGhIjKlMnOpQrStUvWxYz1234567890",
        context_snippet="secret=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890",
        source_url="https://example.com",
        line_number=5,
        tool_found_by="regex",
    )
    assert validator._validate_generic(finding).should_keep is True


def test_secret_deduplication():
    validator = SecretValidator()
    findings = [
        SecretFinding("aws_access_key", "AWS Access Key ID Exposed", "CRITICAL", "AKIA1234567890ABCDEF...", "ctx", "https://a", 1, "regex"),
        SecretFinding("aws_access_key", "AWS Access Key ID Exposed", "CRITICAL", "AKIA1234567890ABCDEF...", "ctx2", "https://b", 2, "regex"),
    ]
    deduped = validator._deduplicate(findings)
    assert len(deduped) == 1


def test_generate_bucket_names():
    names = generate_bucket_names("example", "example")
    assert "example-backup" in names
    assert "example-prod" in names
    assert len(names) >= 15


def test_cloud_module_does_not_report_guessed_buckets_as_findings():
    module = CloudSecurityModule()
    findings = module._scan_s3_buckets("scan-1", SimpleNamespace(target="example.com"))
    assert findings == []


def test_immediate_notifier_slack(monkeypatch):
    calls = []

    class DummyResponse:
        status_code = 200

    async def fake_post(self, url, json=None, timeout=None):
        calls.append((url, json))
        return DummyResponse()

    monkeypatch.setattr("backend.workers.processors.immediate_notifier.httpx.AsyncClient.post", fake_post)
    notifier = ImmediateNotifier()
    finding = SimpleNamespace(title="AWS Key Exposed", severity="CRITICAL", affected_url="https://example.com")
    notifier._send_slack([finding], "example.com", "scan-1")
    assert calls
    assert "CRITICAL FINDING" in calls[0][1]["text"]


def test_immediate_notifier_rate_limit(monkeypatch):
    calls = []

    class DummyResponse:
        status_code = 200

    async def fake_post(self, url, json=None, timeout=None):
        calls.append((url, json))
        return DummyResponse()

    monkeypatch.setattr("backend.workers.processors.immediate_notifier.httpx.AsyncClient.post", fake_post)
    notifier = ImmediateNotifier()
    finding = SimpleNamespace(title="AWS Key Exposed", severity="CRITICAL", affected_url="https://example.com")
    notifier.notify_critical("scan-1", [finding], "example.com")
    notifier.notify_critical("scan-1", [finding], "example.com")
    assert len(calls) == 1


def test_git_exposed_finds_config(monkeypatch):
    async def fake_get(url, timeout=15):
        class Resp:
            status_code = 200
            text = "[remote \"origin\"]\n    url = https://github.com/example/repo.git"
        return Resp()

    monkeypatch.setattr("backend.workers.modules.git_secret_scanner.httpx.AsyncClient.get", fake_get)
    scanner = GitSecretScanner()
    findings = scanner._scan_exposed_git("https://example.com", "scan-1")
    assert findings
    assert any(".git Repository" in f.title for f in findings)
