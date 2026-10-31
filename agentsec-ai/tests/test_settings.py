from backend.config.settings import Settings


def test_settings_load_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test AgentSec")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@db:5432/testdb")
    monkeypatch.setenv("POSTGRES_HOST", "db-host")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setenv("POSTGRES_USER", "test-user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test-pass")
    monkeypatch.setenv("POSTGRES_DB", "test-db")
    monkeypatch.setenv("REDIS_HOST", "redis-host")
    monkeypatch.setenv("REDIS_PORT", "6380")
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://redis-host:6380/2")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://redis-host:6380/3")
    monkeypatch.setenv("JWT_SECRET_KEY", "secret-from-env")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test AgentSec"
    assert settings.database.url == "postgresql+asyncpg://test:test@db:5432/testdb"
    assert settings.database.host == "db-host"
    assert settings.database.port == 5433
    assert settings.database.user == "test-user"
    assert settings.database.password == "test-pass"
    assert settings.database.name == "test-db"
    assert settings.redis.host == "redis-host"
    assert settings.redis.port == 6380
    assert settings.celery.broker_url == "redis://redis-host:6380/2"
    assert settings.celery.result_backend == "redis://redis-host:6380/3"
    assert settings.jwt.secret_key == "secret-from-env"
