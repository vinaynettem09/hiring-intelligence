"""Hiring-timeline API — the exportable audit trail for one candidate evaluation.

GET /evaluations/{candidate_evaluation_id}/timeline — a coherent, chronological record
assembled from authoritative append-only sources (no new business logic). Tenant-scoped;
a pure read (request-scoped session). (Route hangs off /evaluations for consistency — see
TD-018 on the eventual candidate-evaluation aggregate root.)
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.timeline.schemas import HiringTimelineResponse
from app.modules.timeline.service import TimelineService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(prefix="/evaluations", tags=["timeline"])


@router.get("/{candidate_evaluation_id}/timeline")
async def get_timeline(
    candidate_evaluation_id: str,
    auth: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> HiringTimelineResponse:
    return await TimelineService(session, auth.organization_id).get_timeline(
        candidate_evaluation_id
    )
