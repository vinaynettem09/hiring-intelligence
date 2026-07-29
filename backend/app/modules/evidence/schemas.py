"""Recruiter-facing DTOs for inspecting submitted evidence.

This is the **source** a recruiter drills into from an evaluation citation
(Claim -> Citation -> Source evidence). It is the recruiter's authorized view of what the
candidate actually submitted — NOT the AI's PII-minimized input, and NOT raw provider
output. `evidence_id` / `task_id` are the same ids the evaluation's citations carry, so the
UI can match a citation to its source; they are internal ids, never shown as primary labels.
"""

from datetime import datetime

from pydantic import BaseModel


class SubmittedEvidenceItem(BaseModel):
    evidence_id: str  # matches an evaluation citation's evidence_id (internal id, not a label)
    task_id: str  # the frozen work-sample task this evidence answers
    task_number: int  # human-friendly position (display_order + 1) — "Task 1", "Task 2", ...
    task_prompt: str
    evidence_intent: str  # what the task was designed to elicit (recruiter-facing)
    response_text: str  # the candidate's verbatim submitted answer (immutable snapshot)
    captured_at: datetime


class SubmittedEvidenceResponse(BaseModel):
    candidate_evaluation_id: str
    items: list[SubmittedEvidenceItem]
