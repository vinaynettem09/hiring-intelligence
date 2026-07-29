"""Hiring-process timeline vocabulary. Each kind is DERIVED from an authoritative,
append-only record (invitation, consent, submission, evaluation run, decision) — the
timeline introduces no new state, it only makes the existing facts explainable."""

from enum import StrEnum


class TimelineEventKind(StrEnum):
    INVITATION_SENT = "INVITATION_SENT"
    INVITATION_OPENED = "INVITATION_OPENED"
    CONSENT_GRANTED = "CONSENT_GRANTED"
    CONSENT_WITHDRAWN = "CONSENT_WITHDRAWN"
    WORK_SAMPLE_SUBMITTED = "WORK_SAMPLE_SUBMITTED"
    EVALUATION_GENERATED = "EVALUATION_GENERATED"
    DECISION_RECORDED = "DECISION_RECORDED"
