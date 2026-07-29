"""Review-queue vocabulary.

`QueueStage` is **derived** from authoritative domain data (CandidateEvaluation status +
submission + Invitation + latest Evaluation) — it is NOT a stored, mutable workflow column.
The queue reflects the real world; it never becomes a second source of truth.
"""

from enum import StrEnum


class QueueStage(StrEnum):
    """Where a candidate evaluation sits in the review workflow. Derived, never persisted."""

    AWAITING_INVITATION = "AWAITING_INVITATION"  # added, no invitation issued (recruiter to act)
    AWAITING_CANDIDATE = "AWAITING_CANDIDATE"  # invited, not yet submitted (waiting on candidate)
    READY_FOR_EVALUATION = "READY_FOR_EVALUATION"  # submitted, no evaluation yet (recruiter to act)
    NEEDS_REVIEW = "NEEDS_REVIEW"  # evaluated, ESCALATE or MIXED (recruiter to act)
    EVALUATED = "EVALUATED"  # evaluated, decisive proceed/do-not-proceed (completed)


class QueueFilter(StrEnum):
    """Lightweight workflow filters — only the ones that solve a real recruiter need."""

    ALL = "all"
    NEEDS_ATTENTION = "needs_attention"  # NEEDS_REVIEW + READY_FOR_EVALUATION + AWAITING_INVITATION
    READY = "ready"  # READY_FOR_EVALUATION
    WAITING = "waiting"  # AWAITING_CANDIDATE (waiting on the candidate)
    COMPLETED = "completed"  # EVALUATED


# Stages that require the RECRUITER to act (vs. waiting on the candidate or already done).
ATTENTION_STAGES = frozenset(
    {QueueStage.NEEDS_REVIEW, QueueStage.READY_FOR_EVALUATION, QueueStage.AWAITING_INVITATION}
)
