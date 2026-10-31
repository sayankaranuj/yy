"""Administrator-managed target authorization routes."""

import ipaddress
import re
import secrets
from urllib.parse import urlsplit

import httpx

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from backend.api.auth import require_admin
from backend.config.settings import settings
from backend.config.database import AsyncSessionFactory
from backend.repositories import ActiveApiRepository
from backend.storage import AuthorizationRequestStore, TargetStore

router = APIRouter(prefix="/targets", tags=["targets"])
_store = TargetStore()
_request_store = AuthorizationRequestStore()


def normalize_target(value: str) -> str:
    """Normalize a host or public IP for exact allowlist matching."""

    target = value.strip().lower().rstrip(".")
    if "://" in target:
        parsed = urlsplit(target)
        if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
            raise ValueError("target must be a valid host or HTTP(S) URL")
        host = (parsed.hostname or "").rstrip(".")
        if parsed.query or parsed.fragment:
            raise ValueError("target URL must not include a query or fragment")
        if parsed.path not in {"", "/"}:
            if host in {"github.com", "gitlab.com", "bitbucket.org"}:
                components = [item for item in parsed.path.split("/") if item]
                if len(components) != 2 or any(
                    component in {".", ".."}
                    or not re.fullmatch(r"[A-Za-z0-9_.-]+", component)
                    for component in components
                ):
                    raise ValueError("repository URL must identify one repository")
                port = f":{parsed.port}" if parsed.port else ""
                return f"{host}{port}{parsed.path.rstrip('/')}"
            # Web targets are approved at host/port scope; the scan may still
            # retain and request the specific path supplied by the user.
            target = host
            if parsed.port:
                target = f"{host}:{parsed.port}"
        else:
            target = host
        if parsed.port:
            target = f"{host}:{parsed.port}"
    if not target or any(char in target for char in "\r\n\x00"):
        raise ValueError("target must be a valid host or HTTP(S) URL")
    if re.search(r"[<>]|(;|&&|\|\||`)|(--|/\*)", target):
        raise ValueError("target contains unsafe characters")
    host = target.rsplit(":", 1)[0] if target.count(":") == 1 and target.rsplit(":", 1)[1].isdigit() else target
    is_local = host in {"localhost", "127.0.0.1", "::1"}
    if is_local and settings.app_env.lower() == "development":
        return target
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        if len(host) > 253 or not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host):
            raise ValueError("target must be a valid host")
    else:
        if not address.is_global:
            raise ValueError("private or non-routable targets are not allowed")
    return target


class TargetApprovalRequest(BaseModel):
    target: str = Field(min_length=1)
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        return normalize_target(value)


class TargetApproval(BaseModel):
    id: int
    target: str
    approved_by: str
    reason: str
    enabled: bool
    ownership_verified: bool = False


class VerificationRequest(BaseModel):
    target: str = Field(min_length=1)
    method: str

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        return normalize_target(value)

    @field_validator("method")
    @classmethod
    def validate_method(cls, value: str) -> str:
        if value not in {"dns_txt", "http"}:
            raise ValueError("method must be dns_txt or http")
        return value


class VerificationChallenge(BaseModel):
    target: str
    method: str
    token: str
    instructions: str
    auto_approved: bool = False


class VerificationResult(BaseModel):
    target: str
    method: str
    verified: bool
    detail: str = ""


class AuthorizationRequestCreate(BaseModel):
    target: str = Field(min_length=1, max_length=500)
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        return normalize_target(value)


class AuthorizationDecision(BaseModel):
    decision: str
    note: str = Field(default="", max_length=1000)

    @field_validator("decision")
    @classmethod
    def validate_decision(cls, value: str) -> str:
        if value not in {"approve", "reject"}:
            raise ValueError("decision must be approve or reject")
        return value


@router.get("", response_model=list[TargetApproval])
async def list_targets() -> list[TargetApproval]:
    records = (
        await _store.list_records_async()
        if settings.storage_backend.lower() == "postgres"
        else _store.list_records()
    )
    return [TargetApproval(**record) for record in records]


@router.post("", response_model=TargetApproval, status_code=status.HTTP_201_CREATED)
async def approve_target(
    payload: TargetApprovalRequest,
    administrator: str = Depends(require_admin),
) -> TargetApproval:
    if not _store.is_verified(payload.target):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="verify target ownership before administrator approval",
        )
    if settings.storage_backend.lower() == "postgres":
        from backend.repositories import ActiveApiRepository
        from backend.config.database import AsyncSessionFactory

        async with AsyncSessionFactory() as session:
            record = await ActiveApiRepository(session).approve_target(
                payload.target, administrator, payload.reason
            )
    else:
        record = _store.approve(payload.target, administrator, payload.reason)
    return TargetApproval(**record)


@router.post("/verification", response_model=VerificationChallenge)
async def create_verification(payload: VerificationRequest) -> VerificationChallenge:
    token = secrets.token_urlsafe(32)
    _store.create_verification(payload.target, payload.method, token)
    host = payload.target.rsplit(":", 1)[0] if payload.target.count(":") == 1 and payload.target.rsplit(":", 1)[1].isdigit() else payload.target
    auto_approved = settings.app_env.lower() == "development" and host in {"localhost", "127.0.0.1", "::1"}
    if auto_approved:
        _store.mark_verified(payload.target, payload.method, token)
        if settings.storage_backend.lower() == "postgres":
            async with AsyncSessionFactory() as session:
                await ActiveApiRepository(session).approve_target(
                    payload.target, "development-local", "Development-local authorized target"
                )
        else:
            _store.approve(payload.target, "development-local", "Development-local authorized target")
    if payload.method == "dns_txt":
        instructions = f"Publish TXT record _agentsec-verification.{payload.target} with value {token}"
    else:
        instructions = (
            f"Serve the exact token {token} at "
            f"https://{payload.target}/.well-known/agentsec-verification.txt"
        )
    return VerificationChallenge(
        target=payload.target,
        method=payload.method,
        token=token,
        instructions=instructions,
        auto_approved=auto_approved,
    )


@router.post("/verification/verify", response_model=VerificationResult)
async def verify_target(payload: VerificationRequest) -> VerificationResult:
    records = _store._read()
    record = next((item for item in records if item["target"] == payload.target), None)
    if record is None or record.get("verification_method") != payload.method:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="verification challenge not found")
    token = record.get("verification_token", "")
    verified = False
    detail = "Verification value did not match."
    if payload.method == "http":
        try:
            async with httpx.AsyncClient(follow_redirects=False, timeout=10) as client:
                response = await client.get(
                    f"https://{payload.target}/.well-known/agentsec-verification.txt"
                )
            verified = response.status_code == 200 and response.text.strip() == token
            if response.status_code != 200:
                detail = f"Verification file returned HTTP {response.status_code}."
            elif "<html" in response.text[:1000].lower() or "<!doctype" in response.text[:1000].lower():
                detail = (
                    "The verification URL returned the website HTML fallback. "
                    "Deploy public/.well-known/agentsec-verification.txt as a plain-text file "
                    "containing the current challenge token."
                )
            elif not verified:
                detail = "Verification URL returned content, but it was not the current challenge token."
        except httpx.HTTPError:
            detail = "The verification URL could not be reached."
    else:
        try:
            import dns.resolver

            answers = await __import__("asyncio").to_thread(
                dns.resolver.resolve,
                f"_agentsec-verification.{payload.target}",
                "TXT",
            )
            values = [b"".join(answer.strings).decode("utf-8") for answer in answers]
            verified = token in values
        except ImportError:
            detail = "DNS verification is unavailable because dnspython is not installed."
        except (OSError, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
            detail = "The required DNS TXT record was not found."
    if verified:
        _store.mark_verified(payload.target, payload.method, token)
        detail = "Ownership verified."
    return VerificationResult(
        target=payload.target,
        method=payload.method,
        verified=verified,
        detail=detail,
    )


@router.delete("/{target}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_target(target: str, _administrator: str = Depends(require_admin)) -> None:
    normalized = normalize_target(target)
    revoked = (
        await _store.revoke_async(normalized)
        if settings.storage_backend.lower() == "postgres"
        else _store.revoke(normalized)
    )
    if not revoked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="approved target not found")


@router.post("/requests", status_code=status.HTTP_201_CREATED)
async def create_authorization_request(
    payload: AuthorizationRequestCreate,
    requester: str = Depends(require_admin),
) -> dict:
    if settings.storage_backend.lower() == "postgres":
        async with AsyncSessionFactory() as session:
            record = await ActiveApiRepository(session).create_authorization_request(
                payload.target, payload.reason, requester
            )
    else:
        record = _request_store.create(payload.target, payload.reason, requester)
    return record


@router.get("/requests")
async def list_authorization_requests(
    _administrator: str = Depends(require_admin),
) -> list[dict]:
    if settings.storage_backend.lower() == "postgres":
        async with AsyncSessionFactory() as session:
            return await ActiveApiRepository(session).list_authorization_requests()
    return _request_store.list_records()


@router.post("/requests/{request_id}/decision")
async def review_authorization_request(
    request_id: int,
    payload: AuthorizationDecision,
    administrator: str = Depends(require_admin),
) -> dict:
    if settings.storage_backend.lower() == "postgres":
        async with AsyncSessionFactory() as session:
            record = await ActiveApiRepository(session).review_authorization_request(
                request_id, payload.decision, administrator, payload.note
            )
    else:
        request = next(
            (
                item for item in _request_store.list_records()
                if item["id"] == request_id and item["status"] == "pending"
            ),
            None,
        )
        if request is None:
            record = None
        else:
            if payload.decision == "approve":
                _store.approve_manual(
                    request["target"], administrator, payload.note or request["reason"]
                )
            record = _request_store.review(
                request_id, payload.decision, administrator, payload.note
            )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="authorization request is missing or no longer pending",
        )
    return record
