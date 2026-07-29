"""Review-queue DTOs — recruiter-facing operational information only.

Carries the authoritative state (stage, recommendation, confidence) but NO display copy:
the frontend owns all recruiter language via `components/ai/presentation.ts`, so the queue
and the evaluation workspace never drift into two vocabularies. No model/provider/token
data here (that belongs only in the evaluation detail's technical section).
"""

from datetime import datetime

from pydantic import BaseModel

from app.modules.review.enums import QueueStage


class ReviewQueueItem(BaseModel):
    candidate_evaluation_id: str
    candidate_name: str
    candidate_email: str
    campaign_id: str
    role_title: str
    stage: QueueStage
    needs_attention: bool
    # Present only once an evaluation exists. Raw values — the frontend maps them to humane
    # labels / confidence levels (recommendation is never a candidate-quality score).
    recommendation: str | None
    confidence: float | None
    run_number: int | None
    # The latest HUMAN decision, if one has been recorded (badge only — the AI never
    # writes this, and it does not change the row's stage or order). Raw value; the
    # frontend maps it to humane copy.
    decision: str | None
    last_activity_at: datetime


class ReviewQueueSummary(BaseModel):
    """Whole-queue counts (independent of the active filter/search) so the recruiter always
    sees the true shape of the workload."""

    needs_review: int  # NEEDS_REVIEW (ESCALATE / MIXED)
    ready_to_evaluate: int  # READY_FOR_EVALUATION
    awaiting_invitation: int  # AWAITING_INVITATION
    waiting_on_candidate: int  # AWAITING_CANDIDATE
    completed: int  # EVALUATED
    total: int


class ReviewQueueResponse(BaseModel):
    items: list[ReviewQueueItem]
    summary: ReviewQueueSummary
    total: int  # rows matching the current filter/search (for pagination)
    limit: int
    offset: int
