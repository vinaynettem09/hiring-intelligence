"""Platform confidence — computed by US, never taken from the model.

**Semantics (read this before touching the numbers).** Confidence is a bounded [0, 1]
signal of *how reliably the available evidence supports this evaluation proposal* — an
evidence-sufficiency / evaluation-reliability measure. It is NOT a calibrated probability
that the candidate will succeed on the job, NOT the probability the AI is correct, NOT a
hiring probability, and NOT the strength of the recommendation. Until we have outcome data
to calibrate against, that is the only honest reading.

Consequently, confidence is **orthogonal to direction**: `DO_NOT_PROCEED` with HIGH
confidence (strong, one-sided evidence the candidate is below the bar) and `PROCEED` with
HIGH confidence are both valid. What lowers confidence is *insufficient* or *ambiguous*
evidence, never the direction of the call.

The provider's own `provider_confidence` / per-assessment `signal` are retained for
observability but never feed this number — the model does not own our confidence.

Why v2 (see TD-016). v1 was ``0.5·competency_coverage + 0.5·evidence_coverage`` — pure
*coverage*. It answered "was there evidence, and did the model assess the competencies?"
and so returned ~1.0 for strong, weak, AND genuinely mixed evidence alike (the first live
Gemini A-G run scored fixtures A/B/C/G all at 1.0). Coverage is necessary but not
sufficient for reliability: evidence that points *both* ways is real but does not support a
confident single-direction proposal. v2 keeps coverage as the *sufficiency* term and
multiplies it by a *decisiveness* term derived from how one-sided vs. mixed the model's
grounded observations are.

What v2 deliberately does NOT do:
  * It does not read evidence length — verbose fluff cannot raise it and a concise answer
    cannot lower it (the calculator never sees evidence text, only structure/ids).
  * It does not invent a pseudo-probability. Both terms are transparent, bounded ratios.
  * It does not (and structurally cannot) detect a *confidently wrong* model that fabricates
    a clean one-sided assessment from thin evidence. That is a model-quality failure, caught
    by the behavioral A-G regression gates and the model's own ESCALATE behavior — not by
    this number (see TD-016 residual notes).
"""

from typing import Protocol

from app.modules.intelligence.schemas import EvaluationInput
from app.modules.intelligence.versions import CONFIDENCE_ALGORITHM_VERSION
from app.platform.ai import ProviderResult

# --- SUFFICIENCY: is there enough grounded material to assess the role? --------------- #
# Kept explicit and summing to 1.0. This is the (renamed) v1 core.
_COMPETENCY_COVERAGE_WEIGHT = 0.5
_EVIDENCE_COVERAGE_WEIGHT = 0.5

# --- DECISIVENESS: how one-sided vs. ambiguous is the grounded evidence? -------------- #
# When the model surfaces both supporting (strengths) and opposing (concerns) grounded
# observations, the evidence is mixed and a single-direction proposal is less reliable, so
# confidence is discounted toward this floor. A fully one-sided result (all strengths OR all
# concerns) is decisive → factor 1.0. A result that surfaces NO observation either way is
# treated as thin signal and also floored. Never below this floor: mixedness lowers
# certainty, it does not erase a real, well-covered assessment.
_DECISIVENESS_FLOOR = 0.5

# A provider that itself escalated is telling us it lacked enough to assess responsibly —
# cap confidence low so the honesty floor keeps the exposed outcome an ESCALATE.
_ESCALATION_CONFIDENCE_CAP = 0.2


class ConfidenceCalculator(Protocol):
    """The seam. Given the input and the (validated) provider result, return confidence
    in [0, 1]. Implementations must be deterministic — same inputs, same number."""

    @property
    def version(self) -> str: ...

    def compute(self, evaluation_input: EvaluationInput, result: ProviderResult) -> float: ...


class DeterministicConfidenceCalculator:
    """Confidence v2 — deterministic, factor-based, honest about being a heuristic.

    ``confidence = sufficiency x decisiveness`` (then capped when the provider escalated),
    where both factors are in [0, 1] and read only the immutable input + the *validated*
    provider result (no evidence text, no provider self-confidence):

      * **sufficiency** — ``0.5·competency_coverage + 0.5·evidence_coverage``:
          - competency_coverage = role competencies that received a *grounded* assessment
            (an assessment citing ≥1 present evidence id) / total role competencies;
          - evidence_coverage   = tasks that actually carry submitted evidence / total tasks.
      * **decisiveness** — how one-sided the model's grounded strengths/concerns are:
          - all on one side (decisive) → 1.0;
          - evenly split (maximally ambiguous / mixed) → the floor;
          - none surfaced at all (thin signal) → the floor.

    We deliberately do NOT dress this up as a statistical probability.
    """

    @property
    def version(self) -> str:
        return CONFIDENCE_ALGORITHM_VERSION

    def compute(self, evaluation_input: EvaluationInput, result: ProviderResult) -> float:
        sufficiency = self._sufficiency(evaluation_input, result)
        decisiveness = self._decisiveness(result)
        score = sufficiency * decisiveness
        if result.recommendation == "ESCALATE":
            score = min(score, _ESCALATION_CONFIDENCE_CAP)
        return round(score, 4)

    # --- sufficiency ------------------------------------------------------------------ #

    @classmethod
    def _sufficiency(cls, evaluation_input: EvaluationInput, result: ProviderResult) -> float:
        return _COMPETENCY_COVERAGE_WEIGHT * cls._competency_coverage(
            evaluation_input, result
        ) + _EVIDENCE_COVERAGE_WEIGHT * cls._evidence_coverage(evaluation_input)

    @staticmethod
    def _competency_coverage(evaluation_input: EvaluationInput, result: ProviderResult) -> float:
        competencies = {c.name for c in evaluation_input.role.competencies}
        if not competencies:
            return 0.0
        legal_evidence = {i.evidence_id for t in evaluation_input.tasks for i in t.evidence}
        assessed = {
            a.competency
            for a in result.competency_assessments
            if a.competency in competencies
            and any(c.evidence_id in legal_evidence for c in a.citations)
        }
        return len(assessed) / len(competencies)

    @staticmethod
    def _evidence_coverage(evaluation_input: EvaluationInput) -> float:
        if not evaluation_input.tasks:
            return 0.0
        with_evidence = sum(1 for t in evaluation_input.tasks if t.evidence)
        return with_evidence / len(evaluation_input.tasks)

    # --- decisiveness ----------------------------------------------------------------- #

    @staticmethod
    def _decisiveness(result: ProviderResult) -> float:
        """1.0 when the grounded observations are one-sided (decisive), falling to the
        floor as they become evenly split (ambiguous). No observations at all → floor
        (thin signal). Direction-agnostic: it reads the *balance* of strengths vs.
        concerns, never which way the recommendation points."""
        strengths = len(result.strengths)
        concerns = len(result.concerns)
        total = strengths + concerns
        if total == 0:
            return _DECISIVENESS_FLOOR
        # balance ∈ [0, 0.5]: 0 = fully one-sided, 0.5 = evenly split.
        balance = min(strengths, concerns) / total
        # Map balance 0 → 1.0 and balance 0.5 → floor, linearly.
        return 1.0 - (1.0 - _DECISIVENESS_FLOOR) * (balance / 0.5)
