"""Candidate-facing DTOs — deliberately distinct from the recruiter work-sample DTO.

The candidate sees only what they may: company, role, the task prompts/instructions,
their own draft, and progress. They never see evidence_intent, competency mappings, the
hiring bar, or any internal configuration. A test asserts these fields are absent.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class CandidateTaskView(BaseModel):
    task_id: str
    order: int  # 1-based position
    prompt: str
    instructions: str | None
    expected_effort_minutes: int | None
    response_text: str  # the candidate's own draft (empty if not started)


class CandidateWorkSample(BaseModel):
    organization_name: str
    role_title: str
    title: str
    introduction: str | None
    estimated_minutes: int
    tasks: list[CandidateTaskView]
    submitted: bool
    submitted_at: datetime | None


class SubmitWorkSampleRequest(BaseModel):
    # Token only — the server owns the drafts and the frozen tasks. The client never
    # re-sends response text at submission (no client/server divergence).
    token: str


class SubmissionResult(BaseModel):
    organization_name: str
    role_title: str
    submitted_at: datetime
    evidence_count: int


class SaveResponseRequest(BaseModel):
    token: str
    task_id: str
    # Defensive size limit only — no "too short to score" nudging, no word quotas.
    response_text: str = Field(max_length=20000)


class LoadWorkSampleRequest(BaseModel):
    token: str


class SavedResponse(BaseModel):
    task_id: str
    updated_at: datetime
