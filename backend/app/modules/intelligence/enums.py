"""Intelligence vocabulary — recommendation proposals, escalation reasons, and the
pipeline failure taxonomy. All are StrEnum so their `.value` is a stable machine string.

Naming is deliberate. This module produces a **proposal**, never a decision: there is
no `HiringDecision`, no `hire`, no `reject`. AI proposes; the domain / a human decides.
"""

from enum import StrEnum


class RecommendationProposal(StrEnum):
    """What the AI *proposes* — a recommendation for a human, not an authoritative
    outcome. `ESCALATE` is a first-class, successful proposal (see EscalationReason)."""

    STRONG_PROCEED = "STRONG_PROCEED"
    PROCEED = "PROCEED"
    MIXED = "MIXED"
    DO_NOT_PROCEED = "DO_NOT_PROCEED"
    ESCALATE = "ESCALATE"


class EscalationReason(StrEnum):
    """Why a *successful* proposal is ESCALATE. This is not an error — it means the
    system judges the evidence too thin, or its own confidence too low, to responsibly
    propose a direction, so it defers to a human. Orthogonal to the failure taxonomy."""

    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"  # provider itself judged evidence too thin
    LOW_CONFIDENCE = "LOW_CONFIDENCE"  # platform confidence fell below the honesty floor


class EvaluationFailureReason(StrEnum):
    """Why the pipeline could NOT produce a valid proposal at all — a *system* condition,
    never a statement about the candidate. Distinct from ESCALATE (a valid proposal).
    This taxonomy will drive Epic 5's failure UX (a broken provider must never read to a
    recruiter as 'the candidate's evidence was insufficient')."""

    INVALID_PROVIDER_OUTPUT = "INVALID_PROVIDER_OUTPUT"  # unparseable / out-of-vocabulary output
    UNGROUNDED_OUTPUT = "UNGROUNDED_OUTPUT"  # claims not backed by cited, present evidence
    POLICY_VIOLATION = "POLICY_VIOLATION"  # output breached a governed policy check
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"  # provider raised / timed out / transport error
