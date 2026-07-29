"""Review-queue service — assembles the recruiter's operational inbox from the read model.

One tenant-scoped read model call for the page + one for the whole-queue summary. Stage is
authoritative (derived in SQL); this layer only maps rows to DTOs and marks which stages
require the recruiter (vs. waiting on the candidate or already complete).
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.review.enums import ATTENTION_STAGES, QueueFilter, QueueStage
from app.modules.review.repository import ReviewQueueRepository
from app.modules.review.schemas import (
    ReviewQueueItem,
    ReviewQueueResponse,
    ReviewQueueSummary,
)


class ReviewQueueService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._repo = ReviewQueueRepository(session, tenant_id)

    async def get_queue(
        self,
        *,
        queue_filter: QueueFilter = QueueFilter.ALL,
        campaign_id: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> ReviewQueueResponse:
        rows, total = await self._repo.fetch_page(
            queue_filter=queue_filter,
            campaign_id=campaign_id,
            search=search,
            limit=limit,
            offset=offset,
        )
        items = [
            ReviewQueueItem(
                candidate_evaluation_id=row.candidate_evaluation_id,
                candidate_name=row.candidate_name,
                candidate_email=row.candidate_email,
                campaign_id=row.campaign_id,
                role_title=row.role_title,
                stage=QueueStage(row.stage),
                needs_attention=QueueStage(row.stage) in ATTENTION_STAGES,
                recommendation=row.recommendation,
                confidence=row.confidence,
                run_number=row.run_number,
                decision=row.decision,
                last_activity_at=row.last_activity_at,
            )
            for row in rows
        ]
        counts = await self._repo.stage_counts()
        summary = ReviewQueueSummary(
            needs_review=counts.get(QueueStage.NEEDS_REVIEW.value, 0),
            ready_to_evaluate=counts.get(QueueStage.READY_FOR_EVALUATION.value, 0),
            awaiting_invitation=counts.get(QueueStage.AWAITING_INVITATION.value, 0),
            waiting_on_candidate=counts.get(QueueStage.AWAITING_CANDIDATE.value, 0),
            completed=counts.get(QueueStage.EVALUATED.value, 0),
            total=sum(counts.values()),
        )
        return ReviewQueueResponse(
            items=items, summary=summary, total=total, limit=limit, offset=offset
        )
