"""Review-queue API — the recruiter's operational inbox for evaluation work.

GET /review-queue — a single, tenant-scoped read model (never assembled from many calls).
Tenant comes from the verified token; the queue only ever reflects the caller's org.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.review.enums import QueueFilter
from app.modules.review.schemas import ReviewQueueResponse
from app.modules.review.service import ReviewQueueService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["review"])


@router.get("/review-queue")
async def get_review_queue(
    auth: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
    queue_filter: Annotated[QueueFilter, Query(alias="filter")] = QueueFilter.ALL,
    campaign_id: Annotated[str | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ReviewQueueResponse:
    return await ReviewQueueService(session, auth.organization_id).get_queue(
        queue_filter=queue_filter,
        campaign_id=campaign_id,
        search=search,
        limit=limit,
        offset=offset,
    )
