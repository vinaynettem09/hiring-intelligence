"""Recruiter-facing Evaluation DTOs — what the (future) Epic 5 AI UI will consume
(AIRecommendationCard / ConfidenceMeter / EvidenceTimeline / ReasoningCard / RiskBadge).
These — not ORM models — cross the API boundary. No raw provider payload, no candidate PII.

Naming preserves the boundary: this is a *proposal/assessment*, never a decision. The
`confidence` field is a platform-computed evidence-**reliability** signal in [0, 1], NOT a
probability of on-the-job success — the `confidence_rationale` says so in words.
"""

from datetime import datetime

from pydantic import BaseModel

from app.modules.intelligence.enums import (
    EscalationReason,
    RecommendationProposal,
)


class CitationView(BaseModel):
    """A verified link to immutable Evidence (and its frozen task). Ids, not model quotes —
    excerpts, if ever shown, will be derived from authoritative Evidence by us."""

    evidence_id: str
    task_id: str


class CompetencyAssessmentView(BaseModel):
    competency: str
    assessment: str
    provider_signal: float | None
    citations: list[CitationView]


class ObservationView(BaseModel):
    """A strength or concern with its grounding citations — no uncited claims reach the UI."""

    text: str
    citations: list[CitationView]


class EvidenceCoverageView(BaseModel):
    competencies_total: int
    competencies_assessed: int
    tasks_total: int
    tasks_with_evidence: int


class ProvenanceView(BaseModel):
    provider: str
    model: str
    model_version: str
    prompt_version: str
    input_schema_version: str
    output_schema_version: str
    confidence_algorithm_version: str
    generated_at: datetime


class EvaluationDetail(BaseModel):
    """One Evaluation run in full — enough to render the recommendation, the reasoning,
    the evidence trail, and full provenance."""

    id: str
    candidate_evaluation_id: str
    run_number: int
    recommendation: RecommendationProposal
    confidence: float
    confidence_rationale: str
    escalation_reason: EscalationReason | None
    competency_assessments: list[CompetencyAssessmentView]
    strengths: list[ObservationView]
    concerns: list[ObservationView]
    evidence_coverage: EvidenceCoverageView
    provenance: ProvenanceView
    input_fingerprint: str
    input_tokens: int | None
    output_tokens: int | None
    created_at: datetime


class EvaluationRunSummary(BaseModel):
    """A lightweight history row — no assessments/citations (fetch detail separately)."""

    id: str
    run_number: int
    recommendation: RecommendationProposal
    confidence: float
    model: str
    prompt_version: str
    created_at: datetime


class EvaluationHistoryResponse(BaseModel):
    """The recruiter read model for a candidate evaluation: the latest run in full, plus
    enough history to know earlier runs exist. `latest` is null before any evaluation."""

    candidate_evaluation_id: str
    run_count: int
    latest: EvaluationDetail | None
    runs: list[EvaluationRunSummary]
