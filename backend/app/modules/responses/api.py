"""Candidate work-sample routes (magic-link trust model — no recruiter JWT).

- POST /candidate/work-sample          — load the frozen work sample + the candidate's drafts.
- POST /candidate/work-sample/response — save (upsert) a draft response to one task.

Token in the body; the evaluation/tenant are resolved server-side. Draft responses are
mutable working state — not Evidence (that's Story 4.5). Every call re-checks the three
gates (valid invitation, active consent, active campaign + frozen work sample).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.responses.schemas import (
    CandidateWorkSample,
    LoadWorkSampleRequest,
    SavedResponse,
    SaveResponseRequest,
    SubmissionResult,
    SubmitWorkSampleRequest,
)
from app.modules.responses.service import CandidateWorkSampleService
from app.shared.db import get_session

router = APIRouter(tags=["candidate-work-sample"])


@router.post("/candidate/work-sample")
async def load_work_sample(
    payload: LoadWorkSampleRequest,
    session: AsyncSession = Depends(get_session),
) -> CandidateWorkSample:
    return await CandidateWorkSampleService(session).get_work_sample(payload.token)


@router.post("/candidate/work-sample/response")
async def save_response(
    payload: SaveResponseRequest,
    session: AsyncSession = Depends(get_session),
) -> SavedResponse:
    return await CandidateWorkSampleService(session).save_response(
        payload.token, payload.task_id, payload.response_text
    )


@router.post("/candidate/work-sample/submit")
async def submit_work_sample(
    payload: SubmitWorkSampleRequest,
    session: AsyncSession = Depends(get_session),
) -> SubmissionResult:
    # Token only — the server derives the evaluation and owns the drafts. Atomic,
    # consent-gated, idempotent; promotes final drafts into immutable Evidence.
    return await CandidateWorkSampleService(session).submit(payload.token)
