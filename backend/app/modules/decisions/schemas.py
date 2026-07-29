"""Decision DTOs. A decision is a human action recorded against a candidate evaluation;
it references (never embeds) the AI evaluation run that informed it."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.decisions.enums import DecisionType


class RecordDecisionRequest(BaseModel):
    decision: DecisionType
    rationale: str | None = Field(default=None, max_length=4000)
    # Optional: the Evaluation run the recruiter is deciding against. Validated to belong
    # to this candidate evaluation if supplied.
    evaluation_id: str | None = None


class DecisionView(BaseModel):
    id: str
    decision: DecisionType
    rationale: str | None
    decided_by_email: str  # the accountable person (we have email, not a display name)
    decided_at: datetime
    informed_by_run_number: int | None  # the referenced Evaluation run, if any
    created_at: datetime


class DecisionHistoryResponse(BaseModel):
    """Latest decision + the full append-only history (newest first). `latest` is null
    before any decision is recorded."""

    candidate_evaluation_id: str
    latest: DecisionView | None
    decisions: list[DecisionView]
