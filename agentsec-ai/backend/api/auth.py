"""Authentication routes for AgentSec AI."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
import time
from collections import defaultdict
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, Request, status, Depends
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy import select

from backend.config.settings import settings
from backend.config.database import AsyncSessionFactory
from backend.models.user import RefreshSession, User, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])
login_attempts: dict[str, list[float]] = defaultdict(list)
lock = {}


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        scheme, salt_hex, digest_hex = stored.split("$", 2)
        if scheme != "scrypt":
            return False
        digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


class LoginRequest(BaseModel):
    """Request payload for logging in."""

    username: str
    password: str


class RegistrationRequest(BaseModel):
    email: str
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=12)


class RefreshRequest(BaseModel):
    refresh_token: str


class UserRecord(BaseModel):
    id: str
    email: str
    username: str
    role: str
    is_active: bool


class AuthResponse(BaseModel):
    """Authenticated user payload returned by the API."""

    username: str
    role: str
    token: str
    refresh_token: str | None = None


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, request: Request) -> AuthResponse:
    """Issue a signed access token for the configured operator account."""

    if not settings.jwt.enabled or not settings.jwt.admin_password:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="authentication is not configured")
    now = time.monotonic()
    attempts = [stamp for stamp in login_attempts[payload.username] if now - stamp < 60]
    login_attempts[payload.username] = attempts
    if len(attempts) >= 5:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="too many login attempts")

    async with AsyncSessionFactory() as session:
        user = await session.scalar(
            select(User).where((User.username == payload.username) | (User.email == payload.username))
        )
        valid_admin = hmac.compare_digest(payload.username, settings.jwt.admin_username) and hmac.compare_digest(
            hashlib.sha256(payload.password.encode()).hexdigest(),
            hashlib.sha256(settings.jwt.admin_password.encode()).hexdigest(),
        )
        if user is not None:
            if not user.is_active or (user.locked_until and user.locked_until > datetime.now(timezone.utc)):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="account unavailable")
            valid_user = _verify_password(payload.password, user.hashed_password)
        else:
            valid_user = False
        if not valid_admin and not valid_user:
            login_attempts[payload.username].append(now)
            if user is not None:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
                await session.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
        if user is not None:
            user.failed_login_attempts = 0
            user.last_login = datetime.now(timezone.utc)
            await session.commit()
        username = user.username if user is not None else settings.jwt.admin_username
        role = user.role.value.lower() if user is not None else "admin"
        user_id = str(user.id) if user is not None else "admin"
        refresh = await _create_refresh_session(session, user_id, request, None)
    token = _access_token(username, role, user_id)
    return AuthResponse(username=username, role=role, token=token, refresh_token=refresh)


def _access_token(username: str, role: str, user_id: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_expires_minutes)
    return jwt.encode(
        {"sub": username, "user_id": user_id, "role": role, "exp": expires},
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )


async def _create_refresh_session(session, user_id: str, request: Request | None, replaced_by: str | None) -> str:
    raw = secrets.token_urlsafe(48)
    row = RefreshSession(
        user_id=user_id,
        token_hash=hashlib.sha256(raw.encode()).hexdigest(),
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expires_days),
        replaced_by=replaced_by,
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
    )
    session.add(row)
    await session.commit()
    return raw


@router.post("/register", response_model=UserRecord, status_code=status.HTTP_201_CREATED)
async def register(payload: RegistrationRequest) -> UserRecord:
    """Create a normal analyst account."""

    async with AsyncSessionFactory() as session:
        existing = await session.scalar(select(User).where((User.email == payload.email) | (User.username == payload.username)))
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=_hash_password(payload.password),
            role=UserRole.ANALYST,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserRecord(id=str(user.id), email=user.email, username=user.username, role=user.role.value, is_active=user.is_active)


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(payload: RefreshRequest, request: Request) -> AuthResponse:
    token_hash = hashlib.sha256(payload.refresh_token.encode()).hexdigest()
    async with AsyncSessionFactory() as session:
        row = await session.scalar(select(RefreshSession).where(RefreshSession.token_hash == token_hash))
        if row is None or row.revoked_at is not None or row.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")
        if row.replaced_by:
            row.revoked_at = datetime.now(timezone.utc)
            await session.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token reuse detected")
        user = None if row.user_id == "admin" else await session.get(User, UUID(row.user_id))
        if row.user_id != "admin" and (user is None or not user.is_active):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="account unavailable")
        replacement = await _create_refresh_session(session, row.user_id, request, None)
        row.replaced_by = hashlib.sha256(replacement.encode()).hexdigest()
        row.revoked_at = datetime.now(timezone.utc)
        await session.commit()
        username = user.username if user is not None else settings.jwt.admin_username
        role = user.role.value.lower() if user is not None else "admin"
        user_id = str(user.id) if user is not None else "admin"
        return AuthResponse(username=username, role=role, token=_access_token(username, role, user_id), refresh_token=replacement)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: RefreshRequest) -> None:
    token_hash = hashlib.sha256(payload.refresh_token.encode()).hexdigest()
    async with AsyncSessionFactory() as session:
        row = await session.scalar(select(RefreshSession).where(RefreshSession.token_hash == token_hash))
        if row:
            row.revoked_at = datetime.now(timezone.utc)
            await session.commit()


@router.get("/me", response_model=AuthResponse)
async def get_current_user(authorization: str = Header(default="")) -> AuthResponse:
    """Return the current authenticated user."""

    if not settings.jwt.enabled:
        return AuthResponse(username="admin", role="admin", token="test-token")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required")
    token = authorization[7:]
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        username = payload["sub"]
        role = payload.get("role", "operator")
    except (JWTError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    return AuthResponse(username=username, role=role, token=token)


def require_admin(authorization: str = Header(default="")) -> str:
    """Validate that a request is from the configured administrator."""

    if not settings.jwt.enabled or not settings.jwt.admin_password:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="administrator authentication is not configured",
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required")
    try:
        payload = jwt.decode(
            authorization[7:],
            settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm],
        )
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token") from exc
    username = payload.get("sub")
    role = payload.get("role")
    if not isinstance(role, str) or role.casefold() != "admin" or not isinstance(username, str):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="administrator access required")
    return username
