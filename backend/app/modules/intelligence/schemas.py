"""AI-boundary DTOs — the only shapes that cross into (and out of) the AI pipeline.

Two families:

* **Input** (`EvaluationInput` and nested) — the *only legal* thing a provider may see.
  Built by the assembler from the Frozen Role Profile + Frozen Work Sample Tasks +
  Immutable Evidence (already PII-minimized). It is **immutable** (frozen) and contains
  **no identity fields** — no name, email, phone, résumé, invitation, or consent data.
  Every field here has to justify why the model needs it; fields are not copied merely
  because they exist in the database.

* **Output** (`EvaluationProposal` and nested, plus `EvaluationOutcome`) — the validated,
  grounded, platform-confidence-scored *proposal*. This is NOT a decision (there is no
  `HiringDecision`, `hire`, or `reject` here). A provider's raw output (platform.ai
  `ProviderResult`) only becomes one of these after schema + grounding + policy
  validation and platform confidence calculation.

Raw SQLAlchemy models, sessions, repositories, requests, and auth context never appear
in these types — that is the whole point of the boundary.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.intelligence.enums import (
    EscalationReason,
    EvaluationFailureReason,
    RecommendationProposal,
)
from app.platform.ai import ProviderUsage

# --------------------------------------------------------------------------- #
# INPUT — the only legal AI input path (INV-012). Immutable; no PII.
# --------------------------------------------------------------------------- #


class EvidenceItem(BaseModel):
    """One immutable piece of submitted evidence, projected for the AI. `text` is the
    PII-**minimized** projection of `Evidence.response_text` — never the raw row."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str  # internal id, for provenance/citation — not identity
    text: str  # PII-minimized candidate-authored text (UNTRUSTED content, see prompt contract)


class TaskEvidenceInput(BaseModel):
    """A frozen work-sample task and the evidence submitted against it."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    prompt: str
    evidence_intent: str  # what this task was designed to elicit (recruiter-authored, trusted)
    competencies: tuple[str, ...]  # competency names this task measures
    evidence: tuple[EvidenceItem, ...] = ()


class CompetencyContext(BaseModel):
    """A competency the role is assessed on — from the frozen Role Profile."""

    model_config = ConfigDict(frozen=True)

    name: str
    definition: str | None = None  # the recruiter's description of what 'good' means


class RoleContext(BaseModel):
    """The frozen role calibration the evaluation is measured against."""

    model_config = ConfigDict(frozen=True)

    role_title: str
    bar: str  # the hiring standard, in words
    competencies: tuple[CompetencyContext, ...]


class EvaluationInput(BaseModel):
    """The complete, immutable, PII-minimized input handed to a provider. This is the
    ONLY object that legally crosses the AI boundary (INV-012)."""

    model_config = ConfigDict(frozen=True)

    evaluation_id: str  # pseudonymous link — NOT identity
    role: RoleContext
    tasks: tuple[TaskEvidenceInput, ...]


# --------------------------------------------------------------------------- #
# OUTPUT — validated proposal (+ provenance) or a typed failure.
# --------------------------------------------------------------------------- #


class EvidenceCitation(BaseModel):
    """A verified link from an assessment to real evidence in the input. The `task_id` is
    derived by the platform from the evidence id — we never trust a provider's task claim,
    and (Story 5.1) we do not carry model-generated excerpts (INV: don't trust the model
    to quote). Excerpts, if ever shown, will be derived/verified against Evidence text."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str
    task_id: str


class CompetencyAssessment(BaseModel):
    """A grounded, per-competency observation. Every substantive assessment MUST carry ≥1
    citation to evidence present in the input (grounding validation enforces this)."""

    model_config = ConfigDict(frozen=True)

    competency: str
    assessment: str
    evidence_citations: tuple[EvidenceCitation, ...]
    provider_signal: float | None = None  # the provider's own signal — NOT platform confidence


class GroundedObservation(BaseModel):
    """A strength or concern — a material claim about the candidate, so it MUST be grounded
    in cited evidence (no uncited narrative side channel; grounding validation enforces it)."""

    model_config = ConfigDict(frozen=True)

    text: str
    evidence_citations: tuple[EvidenceCitation, ...]


class EvidenceCoverage(BaseModel):
    """How much of the role/instrument the evaluation could actually stand on — a driver
    of confidence and a transparency signal for the recruiter later."""

    model_config = ConfigDict(frozen=True)

    competencies_total: int
    competencies_assessed: int
    tasks_total: int
    tasks_with_evidence: int


class Provenance(BaseModel):
    """Enough to reconstruct *how* a proposal was produced. Present on every outcome —
    success or failure — so even a failure is attributable to a provider/version."""

    model_config = ConfigDict(frozen=True)

    provider: str
    model: str
    model_version: str
    prompt_version: str
    input_schema_version: str
    output_schema_version: str
    confidence_algorithm_version: str
    generated_at: datetime


class EvaluationProposal(BaseModel):
    """The validated, grounded, platform-scored proposal. A PROPOSAL for a human — never
    an authoritative decision. `confidence` is an evaluation-reliability signal in
    [0, 1], NOT a probability the candidate will succeed (see confidence.py / docs)."""

    model_config = ConfigDict(frozen=True)

    recommendation: RecommendationProposal
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_rationale: str
    escalation_reason: EscalationReason | None = None  # set only when recommendation == ESCALATE
    competency_assessments: tuple[CompetencyAssessment, ...]
    strengths: tuple[GroundedObservation, ...]
    concerns: tuple[GroundedObservation, ...]
    evidence_coverage: EvidenceCoverage
    provenance: Provenance


class EvaluationFailure(BaseModel):
    """A typed, PII-free reason the pipeline produced no valid proposal. Distinct from an
    ESCALATE proposal: this is a system condition, not a statement about the candidate."""

    model_config = ConfigDict(frozen=True)

    reason: EvaluationFailureReason
    message: str  # safe, recruiter-safe summary — never contains evidence text or PII


class EvaluationOutcome(BaseModel):
    """The single return type of the pipeline: exactly one of `proposal` / `failure`,
    plus provenance and the input fingerprint either way. `succeeded` is the one thing
    callers branch on. `input_fingerprint` identifies the exact PII-safe input used —
    present on failures too (reproducibility/debugging)."""

    model_config = ConfigDict(frozen=True)

    provenance: Provenance
    input_fingerprint: str
    proposal: EvaluationProposal | None = None
    failure: EvaluationFailure | None = None
    usage: ProviderUsage | None = None  # operational token accounting (success only)

    @property
    def succeeded(self) -> bool:
        return self.proposal is not None
