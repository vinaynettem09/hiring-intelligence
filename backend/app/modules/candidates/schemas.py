"""Pydantic DTOs for candidate intake. Identity (Candidate) and its per-campaign
participation (CandidateEvaluation) are distinct shapes, mirroring the models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.modules.candidates.enums import EvaluationStatus


class AddCandidateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    resume_object_key: str | None = Field(default=None, max_length=512)


class CandidateSummary(BaseModel):
    """The identity view (PII). Kept separate so evaluation payloads can omit it."""

    id: str
    name: str
    email: EmailStr


class CandidateEvaluationResponse(BaseModel):
    """The result of adding a candidate to a campaign: the AI-visible evaluation record,
    with the candidate summary attached for the recruiter-facing response."""

    id: str
    campaign_id: str
    candidate: CandidateSummary
    status: EvaluationStatus
    created_at: datetime


class RosterEntry(BaseModel):
    """One row of a campaign's roster — the recruiter-facing view (includes candidate
    PII; distinct from anything the AI sees).

    The `has_evaluation` / `latest_*` fields let the roster choose the right contextual
    action (Generate vs. View) and show a glanceable status without an N+1 of evaluation
    reads. They are a read-model convenience only — the AI/evaluation contracts are
    unchanged, and the recommendation is exposed as its stable string value."""

    evaluation_id: str
    candidate: CandidateSummary
    status: EvaluationStatus
    has_resume: bool
    created_at: datetime
    has_evaluation: bool = False
    latest_recommendation: str | None = None
    latest_run_number: int | None = None


class RosterResponse(BaseModel):
    items: list[RosterEntry]
    total: int
    missing_resume: int  # a "needs attention" count for the roster header
    limit: int
    offset: int


class CandidateImportIssue(BaseModel):
    """One non-imported row from a bulk import, with a human-readable reason."""

    row: int  # 1-based row number in the file (excluding the header)
    email: str | None
    outcome: Literal["skipped", "failed"]  # skipped = already in campaign; failed = invalid
    reason: str


class CandidateImportSummary(BaseModel):
    """Per-row outcome of a CSV import — never a single pass/fail. Each row is processed
    independently, so one bad row cannot reject the file."""

    total: int
    imported: int
    skipped: int  # already in the campaign
    failed: int  # validation errors
    issues: list[CandidateImportIssue]  # the skipped + failed rows, with reasons
