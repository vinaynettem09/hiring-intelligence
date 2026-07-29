"""Hiring-timeline DTOs — a coherent, chronological, exportable record of exactly what
happened during one candidate's hiring process. Recruiter-facing (candidate PII is
recruiter-authorized context, as on the roster). Summaries are factual and PII-minimal —
free-text (e.g. a decision rationale) is never inlined here."""

from datetime import datetime

from pydantic import BaseModel

from app.modules.timeline.enums import TimelineEventKind


class TimelineEntry(BaseModel):
    kind: TimelineEventKind
    at: datetime
    actor_type: str  # "recruiter" | "candidate" | "system"
    actor: str | None  # a specific person's email, where one is accountable (else None)
    summary: str  # factual, PII-minimal — self-describing for the exported audit view


class HiringTimelineResponse(BaseModel):
    candidate_evaluation_id: str
    candidate_name: str
    candidate_email: str
    role_title: str
    entries: list[TimelineEntry]  # chronological, oldest first
