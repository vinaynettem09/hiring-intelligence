"""Human decision API — the accountable act after AI evaluation + recruiter review.

- POST /evaluations/{candidate_evaluation_id}/decisions — record a decision (append-only).
- GET  /evaluations/{candidate_evaluation_id}/decisions — latest + full history.

Keyed by candidate_evaluation_id to sit alongside the evaluation read/execution routes.
Tenant + actor come from the verified token; a pure request-scoped session (no long call).
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.decisions.schemas import (
    DecisionHistoryResponse,
    DecisionView,
    RecordDecisionRequest,
)
from app.modules.decisions.service import DecisionService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(prefix="/evaluations", tags=["decisions"])


@router.post("/{candidate_evaluation_id}/decisions", status_code=201)
async def record_decision(
    candidate_evaluation_id: str,
    payload: RecordDecisionRequest,
    auth: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DecisionView:
    return await DecisionService(session, auth).record(candidate_evaluation_id, payload)


@router.get("/{candidate_evaluation_id}/decisions")
async def get_decisions(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DecisionHistoryResponse:
    return await DecisionService(session, auth).get_history(candidate_evaluation_id)
