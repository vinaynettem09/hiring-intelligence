"""FastAPI routes for the identity module.

- POST /auth/signup — create an organization + its first admin user (Story 1.1).
- GET  /me          — stubbed request context until auth lands (Story 1.2).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identity.schemas import (
    AccessTokenResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    MeResponse,
    RefreshRequest,
    SignupRequest,
    SignupResponse,
)
from app.modules.identity.service import IdentityService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["identity"])


@router.post("/auth/signup", status_code=201)
async def signup(
    payload: SignupRequest,
    session: AsyncSession = Depends(get_session),
) -> SignupResponse:
    return await IdentityService(session).signup(payload)


@router.post("/auth/login")
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> LoginResponse:
    return await IdentityService(session).login(payload)


@router.post("/auth/refresh")
async def refresh(
    payload: RefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> AccessTokenResponse:
    return await IdentityService(session).refresh(payload)


@router.post("/auth/logout", status_code=204)
async def logout(
    payload: LogoutRequest,
    session: AsyncSession = Depends(get_session),
) -> None:
    # Present the refresh token to revoke it. No auth required — works even if the
    # access token has expired. Idempotent.
    await IdentityService(session).logout(payload)


@router.get("/me")
async def me(
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> MeResponse:
    # Protected: require_auth 401s unless a verified token populated the envelope.
    # The user id comes from the token (auth.user_id), never from the request.
    return await IdentityService(session).get_identity(auth.user_id)
