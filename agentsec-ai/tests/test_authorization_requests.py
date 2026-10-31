from fastapi.testclient import TestClient

from backend.api import targets
from backend.config.settings import settings
from backend.main import create_app
from backend.storage import AuthorizationRequestStore, TargetStore
from backend.api.scans import ScanCreateRequest
from backend.api.targets import normalize_target


def test_admin_can_manually_review_authorization_request(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "storage_backend", "json")
    monkeypatch.setattr(settings.jwt, "enabled", True)
    monkeypatch.setattr(settings.jwt, "admin_username", "test-admin")
    monkeypatch.setattr(settings.jwt, "admin_password", "test-password")
    monkeypatch.setattr(targets, "_store", TargetStore(tmp_path / "targets.json"))
    monkeypatch.setattr(
        targets,
        "_request_store",
        AuthorizationRequestStore(tmp_path / "requests.json"),
    )

    with TestClient(create_app()) as client:
        login = client.post(
            "/api/auth/login",
            json={"username": "test-admin", "password": "test-password"},
        )
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['token']}"}

        request = client.post(
            "/api/targets/requests",
            headers=headers,
            json={
                "target": "https://pentest-ground.com:9000/",
                "reason": "Authorized test environment",
            },
        )
        assert request.status_code == 201
        assert request.json()["target"] == "pentest-ground.com:9000"

        decision = client.post(
            f"/api/targets/requests/{request.json()['id']}/decision",
            headers=headers,
            json={"decision": "approve", "note": "Approved for scoped testing"},
        )
        assert decision.status_code == 200
        assert decision.json()["status"] == "approved"

        targets_response = client.get("/api/targets", headers=headers)
        assert targets_response.status_code == 200
        approved = targets_response.json()[0]
        assert approved["target"] == "pentest-ground.com:9000"
        assert approved["ownership_verified"] is False

        duplicate_decision = client.post(
            f"/api/targets/requests/{request.json()['id']}/decision",
            headers=headers,
            json={"decision": "reject"},
        )
        assert duplicate_decision.status_code == 409


def test_admin_request_queue_rejects_unauthenticated_access(monkeypatch) -> None:
    monkeypatch.setattr(settings, "storage_backend", "json")
    monkeypatch.setattr(settings.jwt, "enabled", True)
    with TestClient(create_app()) as client:
        response = client.get("/api/targets/requests")
    assert response.status_code == 401


def test_git_scan_requires_exact_public_repository_url() -> None:
    scan = ScanCreateRequest(
        name="Public repository",
        target="https://github.com/owner/repository.git",
        selected_attack_categories=["secrets.git_scan"],
    )
    assert scan.target == "https://github.com/owner/repository.git"

    try:
        ScanCreateRequest(
            name="Invalid repository",
            target="https://github.com/owner",
            selected_attack_categories=["secrets.git_scan"],
        )
    except ValueError as error:
        assert "public HTTPS repository URL" in str(error)
    else:
        raise AssertionError("a non-repository URL should be rejected")


def test_scan_approval_matches_root_url_to_manually_approved_host() -> None:
    assert normalize_target("https://pentest-ground.com:4280/") == "pentest-ground.com:4280"
    assert normalize_target("pentest-ground.com:4280") == "pentest-ground.com:4280"
    assert (
        normalize_target("https://pentest-ground.com:4280/vulnerabilities/sqli/")
        == "pentest-ground.com:4280"
    )
    assert normalize_target("https://pentest-ground.com/vulnerabilities/sqli/") == "pentest-ground.com"
