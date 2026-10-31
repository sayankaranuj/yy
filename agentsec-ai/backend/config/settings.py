"""Application settings for AgentSec AI."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

load_dotenv()


class DatabaseSettings(BaseModel):
    url: str = Field(default="postgresql+asyncpg://agentsec:agentsec123@localhost:5432/agentsecdb")
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="agentsec")
    password: str = Field(default="agentsec123")
    name: str = Field(default="agentsecdb")


class RedisSettings(BaseModel):
    url: str = Field(default="redis://localhost:6379/0")
    host: str = Field(default="redis")
    port: int = Field(default=6379)


class JWTSettings(BaseModel):
    secret_key: str = Field(default="dev-secret")
    algorithm: str = Field(default="HS256")
    access_token_expires_minutes: int = Field(default=60)
    refresh_token_expires_days: int = Field(default=7)
    admin_username: str = Field(default="admin")
    admin_password: str = Field(default="")
    enabled: bool = Field(default=False)


class CelerySettings(BaseModel):
    broker_url: str = Field(default="redis://redis:6379/0")
    result_backend: str = Field(default="redis://redis:6379/0")


class AISettings(BaseModel):
    anthropic_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")


class ScanSettings(BaseModel):
    max_concurrent_scans: int = Field(default=5)
    scan_timeout_seconds: int = Field(default=3600)
    tool_timeout_seconds: int = Field(default=300)
    rate_limit_per_minute: int = Field(default=30)
    dns_resolvers: str = Field(default="1.1.1.1,8.8.8.8")


class ToolSettings(BaseModel):
    tools_base_path: str = Field(default="/opt/tools")
    wordlists_path: str = Field(default="/opt/wordlists")
    nuclei_templates_path: str = Field(default="/opt/nuclei-templates")
    subdomain_wordlist: str = Field(default="/opt/wordlists/subdomains.txt")
    dns_wordlist: str = Field(default="/opt/wordlists/dns.txt")
    directory_wordlist: str = Field(default="/opt/wordlists/directories.txt")
    subfinder_path: str = Field(default="/usr/local/bin/subfinder")
    amass_path: str = Field(default="/usr/local/bin/amass")
    nmap_path: str = Field(default="/usr/bin/nmap")
    nuclei_path: str = Field(default="/usr/local/bin/nuclei")
    httpx_path: str = Field(default="/usr/local/bin/httpx")
    naabu_path: str = Field(default="/usr/local/bin/naabu")
    katana_path: str = Field(default="/usr/local/bin/katana")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="AgentSec AI")
    app_env: str = Field(default="development")
    app_debug: bool = Field(default=True)
    secret_key: str = Field(default="dev-secret")
    allowed_hosts: str = Field(default="localhost,127.0.0.1")
    storage_backend: str = Field(default="json")

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)
    ai: AISettings = Field(default_factory=AISettings)
    scan: ScanSettings = Field(default_factory=ScanSettings)
    tools: ToolSettings = Field(default_factory=ToolSettings)

    @model_validator(mode="before")
    @classmethod
    def apply_environment_overrides(cls, data: object) -> object:
        """Apply environment variables to the nested settings models before validation."""

        if not isinstance(data, dict):
            return data

        env = os.environ

        if "app_name" not in data and "APP_NAME" in env:
            data["app_name"] = env["APP_NAME"]
        if "app_env" not in data and "APP_ENV" in env:
            data["app_env"] = env["APP_ENV"]
        if "app_debug" not in data and "APP_DEBUG" in env:
            data["app_debug"] = env["APP_DEBUG"].lower() in {"1", "true", "yes", "on"}
        if "secret_key" not in data and "SECRET_KEY" in env:
            data["secret_key"] = env["SECRET_KEY"]
        if "allowed_hosts" not in data and "ALLOWED_HOSTS" in env:
            data["allowed_hosts"] = env["ALLOWED_HOSTS"]
        if "storage_backend" not in data and "STORAGE_BACKEND" in env:
            data["storage_backend"] = env["STORAGE_BACKEND"]

        database_data = data.setdefault("database", {})
        if isinstance(database_data, dict):
            if "url" not in database_data and "DATABASE_URL" in env:
                database_data["url"] = env["DATABASE_URL"]
            if "host" not in database_data and "POSTGRES_HOST" in env:
                database_data["host"] = env["POSTGRES_HOST"]
            if "port" not in database_data and "POSTGRES_PORT" in env:
                database_data["port"] = int(env["POSTGRES_PORT"])
            if "user" not in database_data and "POSTGRES_USER" in env:
                database_data["user"] = env["POSTGRES_USER"]
            if "password" not in database_data and "POSTGRES_PASSWORD" in env:
                database_data["password"] = env["POSTGRES_PASSWORD"]
            if "name" not in database_data and "POSTGRES_DB" in env:
                database_data["name"] = env["POSTGRES_DB"]

        redis_data = data.setdefault("redis", {})
        if isinstance(redis_data, dict):
            if "host" not in redis_data and "REDIS_HOST" in env:
                redis_data["host"] = env["REDIS_HOST"]
            if "port" not in redis_data and "REDIS_PORT" in env:
                redis_data["port"] = int(env["REDIS_PORT"])
            if "url" not in redis_data and "REDIS_URL" in env:
                redis_data["url"] = env["REDIS_URL"]

        jwt_data = data.setdefault("jwt", {})
        if isinstance(jwt_data, dict):
            if "secret_key" not in jwt_data and "JWT_SECRET_KEY" in env:
                jwt_data["secret_key"] = env["JWT_SECRET_KEY"]
            if "algorithm" not in jwt_data and "JWT_ALGORITHM" in env:
                jwt_data["algorithm"] = env["JWT_ALGORITHM"]
            if "access_token_expires_minutes" not in jwt_data and "JWT_ACCESS_TOKEN_EXPIRE_MINUTES" in env:
                jwt_data["access_token_expires_minutes"] = int(env["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"])
            if "refresh_token_expires_days" not in jwt_data and "JWT_REFRESH_TOKEN_EXPIRE_DAYS" in env:
                jwt_data["refresh_token_expires_days"] = int(env["JWT_REFRESH_TOKEN_EXPIRE_DAYS"])
            if "admin_username" not in jwt_data and "ADMIN_USERNAME" in env:
                jwt_data["admin_username"] = env["ADMIN_USERNAME"]
            if "admin_password" not in jwt_data and "ADMIN_PASSWORD" in env:
                jwt_data["admin_password"] = env["ADMIN_PASSWORD"]
            if "enabled" not in jwt_data and "AUTH_ENABLED" in env:
                jwt_data["enabled"] = env["AUTH_ENABLED"].lower() in {"1", "true", "yes", "on"}

        celery_data = data.setdefault("celery", {})
        if isinstance(celery_data, dict):
            if "broker_url" not in celery_data and "CELERY_BROKER_URL" in env:
                celery_data["broker_url"] = env["CELERY_BROKER_URL"]
            if "result_backend" not in celery_data and "CELERY_RESULT_BACKEND" in env:
                celery_data["result_backend"] = env["CELERY_RESULT_BACKEND"]

        ai_data = data.setdefault("ai", {})
        if isinstance(ai_data, dict):
            if "anthropic_api_key" not in ai_data and "ANTHROPIC_API_KEY" in env:
                ai_data["anthropic_api_key"] = env["ANTHROPIC_API_KEY"]
            if "openai_api_key" not in ai_data and "OPENAI_API_KEY" in env:
                ai_data["openai_api_key"] = env["OPENAI_API_KEY"]

        scan_data = data.setdefault("scan", {})
        if isinstance(scan_data, dict):
            if "max_concurrent_scans" not in scan_data and "MAX_CONCURRENT_SCANS" in env:
                scan_data["max_concurrent_scans"] = int(env["MAX_CONCURRENT_SCANS"])
            if "scan_timeout_seconds" not in scan_data and "SCAN_TIMEOUT_SECONDS" in env:
                scan_data["scan_timeout_seconds"] = int(env["SCAN_TIMEOUT_SECONDS"])
            if "tool_timeout_seconds" not in scan_data and "TOOL_TIMEOUT_SECONDS" in env:
                scan_data["tool_timeout_seconds"] = int(env["TOOL_TIMEOUT_SECONDS"])
            if "rate_limit_per_minute" not in scan_data and "SCAN_RATE_LIMIT_PER_MINUTE" in env:
                scan_data["rate_limit_per_minute"] = int(env["SCAN_RATE_LIMIT_PER_MINUTE"])
            if "dns_resolvers" not in scan_data and "DNS_RESOLVERS" in env:
                scan_data["dns_resolvers"] = env["DNS_RESOLVERS"]

        tools_data = data.setdefault("tools", {})
        if isinstance(tools_data, dict):
            if "tools_base_path" not in tools_data and "TOOLS_BASE_PATH" in env:
                tools_data["tools_base_path"] = env["TOOLS_BASE_PATH"]
            if "wordlists_path" not in tools_data and "WORDLISTS_PATH" in env:
                tools_data["wordlists_path"] = env["WORDLISTS_PATH"]
            if "nuclei_templates_path" not in tools_data and "NUCLEI_TEMPLATES_PATH" in env:
                tools_data["nuclei_templates_path"] = env["NUCLEI_TEMPLATES_PATH"]
            if "subdomain_wordlist" not in tools_data and "SUBDOMAIN_WORDLIST" in env:
                tools_data["subdomain_wordlist"] = env["SUBDOMAIN_WORDLIST"]
            if "dns_wordlist" not in tools_data and "DNS_WORDLIST" in env:
                tools_data["dns_wordlist"] = env["DNS_WORDLIST"]
            if "directory_wordlist" not in tools_data and "DIRECTORY_WORDLIST" in env:
                tools_data["directory_wordlist"] = env["DIRECTORY_WORDLIST"]
            if "subfinder_path" not in tools_data and "SUBFINDER_PATH" in env:
                tools_data["subfinder_path"] = env["SUBFINDER_PATH"]
            if "amass_path" not in tools_data and "AMASS_PATH" in env:
                tools_data["amass_path"] = env["AMASS_PATH"]
            if "nmap_path" not in tools_data and "NMAP_PATH" in env:
                tools_data["nmap_path"] = env["NMAP_PATH"]
            if "nuclei_path" not in tools_data and "NUCLEI_PATH" in env:
                tools_data["nuclei_path"] = env["NUCLEI_PATH"]
            if "httpx_path" not in tools_data and "HTTPX_PATH" in env:
                tools_data["httpx_path"] = env["HTTPX_PATH"]
            if "naabu_path" not in tools_data and "NAABU_PATH" in env:
                tools_data["naabu_path"] = env["NAABU_PATH"]
            if "katana_path" not in tools_data and "KATANA_PATH" in env:
                tools_data["katana_path"] = env["KATANA_PATH"]

        return data


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

__all__ = ["Settings", "settings", "get_settings"]
