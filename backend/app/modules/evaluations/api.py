"""Evaluation execution + read API (recruiter-facing). Tenant comes from the verified
token (never the body); a cross-tenant id reads as 404. No DB models cross the boundary.

- POST /evaluations/{id}/evaluate  — idempotent; optional `Idempotency-Key` header guards
  a double-click; returns the current run (creates run 1 if none exists).
- POST /evaluations/{id}/rerun      — explicit new immutable run.
- GET  /evaluations/{id}            — latest run in full + run history summary.

Still deterministic-mock only: no real model, no external call.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.modules.evaluations.schemas import EvaluationDetail, EvaluationHistoryResponse
from app.modules.evaluations.service import EvaluationExecutionService
from app.modules.evidence.schemas import SubmittedEvidenceResponse
from app.modules.evidence.service import SubmittedEvidenceReadService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session, get_session_factory

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

# Evaluation execution owns its OWN session/transaction boundaries (TD-011): it must not
# hold a DB transaction open across the provider call, so it takes the factory, not a
# request-scoped session. This is the one documented exception to one-request/one-session.
SessionFactory = Annotated[async_sessionmaker[AsyncSession], Depends(get_session_factory)]


@router.post("/{candidate_evaluation_id}/evaluate")
async def evaluate(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    factory: SessionFactory,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> EvaluationDetail:
    return await EvaluationExecutionService(factory, auth).evaluate(
        candidate_evaluation_id, idempotency_key=idempotency_key
    )


@router.post("/{candidate_evaluation_id}/rerun", status_code=201)
async def rerun(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    factory: SessionFactory,
) -> EvaluationDetail:
    return await EvaluationExecutionService(factory, auth).rerun(candidate_evaluation_id)


@router.get("/{candidate_evaluation_id}")
async def get_history(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    factory: SessionFactory,
) -> EvaluationHistoryResponse:
    return await EvaluationExecutionService(factory, auth).get_history(candidate_evaluation_id)


@router.get("/{candidate_evaluation_id}/evidence")
async def get_submitted_evidence(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SubmittedEvidenceResponse:
    """The submitted evidence behind an evaluation's citations (Claim -> Citation ->
    Source). A pure read, so it uses a normal request-scoped session (not the factory)."""
    return await SubmittedEvidenceReadService(
        session, auth.organization_id
    ).get_for_candidate_evaluation(candidate_evaluation_id)
