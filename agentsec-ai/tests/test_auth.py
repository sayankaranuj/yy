from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from jose import jwt

from backend.main import create_app
from backend.api.auth import require_admin
from backend.config.settings import settings


def test_auth_me_returns_current_user() -> None:
    client = TestClient(create_app())

    response = client.get("/api/auth/me")

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == "admin"
    assert payload["role"] == "admin"


def test_require_admin_accepts_configured_admin_role_case(monkeypatch) -> None:
    monkeypatch.setattr(settings.jwt, "enabled", True)
    monkeypatch.setattr(settings.jwt, "admin_password", "test-password")
    token = jwt.encode(
        {
            "sub": settings.jwt.admin_username,
            "role": "ADMIN",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )

    assert require_admin(f"Bearer {token}") == settings.jwt.admin_username
