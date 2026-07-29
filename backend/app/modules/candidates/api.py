"""FastAPI routes for candidate intake.

- GET  /campaigns/{id}/candidates        — the campaign roster (Story 3.3).
- POST /campaigns/{id}/candidates        — add one candidate (Story 3.1).
- POST /campaigns/{id}/candidates/import — bulk add from a CSV file (Story 3.2).

Protected: `require_auth` supplies the tenant (from the verified token), passed to the
service; never read from the body or path.
"""

import csv
import io

from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.candidates.schemas import (
    AddCandidateRequest,
    CandidateEvaluationResponse,
    CandidateImportSummary,
    RosterResponse,
)
from app.modules.candidates.service import CandidateService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["candidates"])


@router.get("/campaigns/{campaign_id}/candidates")
async def list_roster(
    campaign_id: str,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> RosterResponse:
    return await CandidateService(session, auth.organization_id).list_roster(
        campaign_id, limit=limit, offset=offset
    )


@router.post("/campaigns/{campaign_id}/candidates", status_code=201)
async def add_candidate(
    campaign_id: str,
    payload: AddCandidateRequest,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> CandidateEvaluationResponse:
    # Another org's campaign is indistinguishable from a missing one → 404.
    return await CandidateService(session, auth.organization_id).add_to_campaign(
        campaign_id, payload
    )


@router.post("/campaigns/{campaign_id}/candidates/import")
async def import_candidates(
    campaign_id: str,
    file: UploadFile,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> CandidateImportSummary:
    # Parse the CSV here (transport concern); the service applies the per-row rules.
    # Headers are matched case-insensitively: name, email, resume_object_key (optional).
    raw = await file.read()
    text = raw.decode("utf-8-sig", errors="replace")  # tolerate a BOM from Excel exports
    reader = csv.DictReader(io.StringIO(text))
    rows = [
        {(key or "").strip().lower(): (value or "").strip() for key, value in record.items()}
        for record in reader
    ]
    service = CandidateService(session, auth.organization_id)
    return await service.import_candidates(campaign_id, rows)
