"""Candidate-facing consent routes (magic-link trust model — no recruiter JWT).

- POST /candidate/consent        — the disclosure + current consent state for a token.
- POST /candidate/consent/grant  — grant consent for the token's evaluation (idempotent).

The token (in the body) resolves the evaluation and tenant server-side. The client never
sends an evaluation id or organization id, so cross-evaluation / cross-tenant consent is
structurally impossible.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.consent.schemas import ConsentStateResponse, ConsentTokenRequest
from app.modules.consent.service import ConsentService
from app.shared.db import get_session

router = APIRouter(tags=["consent"])


@router.post("/candidate/consent")
async def get_consent_state(
    payload: ConsentTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> ConsentStateResponse:
    return await ConsentService(session).get_state(payload.token)


@router.post("/candidate/consent/grant")
async def grant_consent(
    payload: ConsentTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> ConsentStateResponse:
    return await ConsentService(session).grant(payload.token)
