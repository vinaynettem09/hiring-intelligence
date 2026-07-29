"""Provider-output validation. The provider is **untrusted**: its raw `ProviderResult`
must survive grounding and policy checks before any of it becomes an `EvaluationProposal`.
Malformed or ungrounded output must never leak forward as a valid evaluation.

These are pure functions over the (already schema-parsed) provider result and the input
it was given. They return a small result object rather than raising, so the orchestrator
can map each failure to the right taxonomy entry.
"""

from dataclasses import dataclass, field

from app.modules.intelligence.enums import RecommendationProposal
from app.modules.intelligence.schemas import EvaluationInput
from app.platform.ai import ProviderResult


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    errors: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def passed(cls) -> "CheckResult":
        return cls(ok=True)

    @classmethod
    def failed(cls, *errors: str) -> "CheckResult":
        return cls(ok=False, errors=tuple(errors))


def evidence_ids(evaluation_input: EvaluationInput) -> set[str]:
    """Every evidence id legally citable for this evaluation. A citation to anything
    outside this set (an invented id, or evidence from another evaluation) is ungrounded."""
    return {item.evidence_id for task in evaluation_input.tasks for item in task.evidence}


def evidence_to_task(evaluation_input: EvaluationInput) -> dict[str, str]:
    """Map each evidence id to the task it belongs to. Used to derive citation task links
    ourselves — we never trust a provider-supplied task id."""
    return {
        item.evidence_id: task.task_id for task in evaluation_input.tasks for item in task.evidence
    }


def validate_grounding(result: ProviderResult, evaluation_input: EvaluationInput) -> CheckResult:
    """No substantive competency claim without evidence, and no citation to evidence that
    is not present in the input.

    Rules:
      * every competency assessment must carry ≥1 citation;
      * every cited `evidence_id` must exist in this evaluation's input.
    (An ESCALATE with *zero* assessments makes no claims, so it is vacuously grounded —
    but any assessment that IS present must be fully grounded.)
    """
    legal = evidence_ids(evaluation_input)
    errors: list[str] = []
    for assessment in result.competency_assessments:
        if not assessment.citations:
            errors.append(f"assessment_without_citations:{assessment.competency}")
            continue
        for citation in assessment.citations:
            if citation.evidence_id not in legal:
                errors.append(f"unknown_evidence_id:{citation.evidence_id}")
    # Strengths and concerns are material claims too — they must be grounded, never an
    # uncited narrative side channel (an "insufficient evidence" assessment must not sit
    # beside an uncited "excellent leadership" strength).
    for kind, observations in (("strength", result.strengths), ("concern", result.concerns)):
        for observation in observations:
            if not observation.citations:
                errors.append(f"{kind}_without_citations")
                continue
            for citation in observation.citations:
                if citation.evidence_id not in legal:
                    errors.append(f"unknown_evidence_id:{citation.evidence_id}")
    return CheckResult.passed() if not errors else CheckResult.failed(*errors)


def validate_policy(result: ProviderResult, evaluation_input: EvaluationInput) -> CheckResult:
    """Governed structural policy checks on the raw output. Story 5.1 enforces the
    machine-checkable ones; content-level policy (sensitive-attribute inference) is
    governed by the prompt contract and is a documented extension point here.

    Checks:
      * `recommendation` is in the fixed vocabulary;
      * any provider self-signal is a sane number in [0, 1].
    """
    errors: list[str] = []
    if not _is_member(result.recommendation):
        errors.append(f"recommendation_out_of_vocabulary:{result.recommendation}")
    for signal in _all_signals(result):
        if not 0.0 <= signal <= 1.0:
            errors.append(f"signal_out_of_range:{signal}")
    return CheckResult.passed() if not errors else CheckResult.failed(*errors)


def _is_member(value: str) -> bool:
    try:
        RecommendationProposal(value)
    except ValueError:
        return False
    return True


def _all_signals(result: ProviderResult) -> list[float]:
    signals: list[float] = []
    if result.provider_confidence is not None:
        signals.append(result.provider_confidence)
    signals.extend(a.signal for a in result.competency_assessments if a.signal is not None)
    return signals
