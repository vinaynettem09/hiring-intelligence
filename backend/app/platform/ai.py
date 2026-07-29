"""AI provider platform seam.

The intelligence domain depends on the narrow `AIProvider` Protocol — never on a
concrete SDK. Anthropic/Bedrock/OpenAI concepts live *only* behind an adapter that
implements this Protocol; nothing provider-specific leaks into services, schemas, or
domain code. Story 5.1 ships exactly one implementation, `DeterministicMockAIProvider`,
and makes **no** network/model call.

A provider receives one immutable, validated `EvaluationInput` (already PII-minimized by
the assembler) and returns a `ProviderResult` — the provider's *raw, untrusted* output.
The provider result is NOT domain state: the intelligence pipeline schema-validates,
grounding-validates, policy-validates, and computes its own confidence before anything
becomes an `EvaluationProposal`. The provider never sees a DB session, repository,
request, auth context, or Candidate PII — only the DTO it is handed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:  # avoid a runtime import cycle — the seam only needs the type here
    from app.modules.intelligence.schemas import EvaluationInput


class ProviderError(Exception):
    """A provider failed to produce a result (timeout, transport, upstream error).

    The pipeline maps this to a `PROVIDER_UNAVAILABLE` *system* failure — never to
    "insufficient candidate evidence". We must not tell a recruiter the candidate's
    evidence was thin when the truth is that our provider broke.
    """


class ProviderDescriptor(BaseModel):
    """Who produced a result — copied verbatim into provenance. Static per provider."""

    model_config = ConfigDict(frozen=True)

    provider: str
    model: str
    model_version: str


class ProviderCitation(BaseModel):
    """A provider's claim that a piece of evidence supports an assessment. UNTRUSTED:
    the pipeline verifies every `evidence_id` exists in the input before accepting it,
    and derives the task link itself (never trusts a provider-supplied task/excerpt)."""

    evidence_id: str


class ProviderCompetencyAssessment(BaseModel):
    competency: str
    assessment: str
    citations: list[ProviderCitation] = Field(default_factory=list)
    # The provider's OWN internal signal, if any. Retained for observability but it is
    # NOT our confidence — the platform computes confidence separately (INV: confidence
    # is ours, not the model's).
    signal: float | None = None


class ProviderObservation(BaseModel):
    """A strength or concern. It carries citations too, so it can be **grounded** — a
    material claim about the candidate can never be an uncited narrative side channel
    (grounding validation rejects an observation with no citation to present evidence)."""

    text: str
    citations: list[ProviderCitation] = Field(default_factory=list)


class ProviderUsage(BaseModel):
    """Operational token accounting reported by a provider (if available). Persisted on a
    successful Evaluation for cost/latency observability — NOT part of any judgment."""

    model_config = ConfigDict(frozen=True)

    input_tokens: int
    output_tokens: int


class ProviderResult(BaseModel):
    """A provider's raw, untrusted structured output. `recommendation` is a free string
    here on purpose: coercing it into our enum is a *validation* step in the pipeline, so
    a garbage value becomes `INVALID_PROVIDER_OUTPUT` rather than a construction error."""

    competency_assessments: list[ProviderCompetencyAssessment] = Field(default_factory=list)
    strengths: list[ProviderObservation] = Field(default_factory=list)
    concerns: list[ProviderObservation] = Field(default_factory=list)
    recommendation: str
    provider_confidence: float | None = None
    usage: ProviderUsage | None = None  # operational only; never feeds confidence/judgment


class AIProvider(Protocol):
    """The one seam the intelligence orchestrator depends on. Concrete providers
    (mock now, a real adapter later) implement it; the orchestrator is injected with one
    and never names a concrete type."""

    @property
    def descriptor(self) -> ProviderDescriptor: ...

    async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult: ...


class DeterministicMockAIProvider:
    """A pure, deterministic stand-in for a real model — the ONLY provider in Story 5.1.

    Same `EvaluationInput` → same `ProviderResult`, always (no randomness, no clock, no
    network). It produces a *structurally realistic* proposal — one grounded assessment
    per competency, citing that competency's evidence — so the whole pipeline (validation,
    confidence, provenance) and later the UI can be exercised end-to-end. It encodes **no
    real judgement**: every assessment is explicitly marked ``[MOCK]`` and the
    recommendation is a fixed placeholder, so mock output can never masquerade as
    intelligence or quietly become production logic.
    """

    _RECOMMENDATION = "PROCEED"  # a fixed placeholder — NOT a judgement about anyone

    @property
    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(provider="mock", model="deterministic-mock", model_version="v1")

    async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
        # Map each competency to the evidence of the tasks that measure it, so every
        # assessment is grounded in real evidence ids from the input.
        evidence_by_competency: dict[str, list[str]] = {}
        for task in evaluation_input.tasks:
            evidence_ids = [item.evidence_id for item in task.evidence]
            for competency in task.competencies:
                evidence_by_competency.setdefault(competency, []).extend(evidence_ids)

        assessments = [
            ProviderCompetencyAssessment(
                competency=competency.name,
                assessment=(
                    f"[MOCK] Deterministic placeholder assessment for "
                    f"'{competency.name}'. This is not a real evaluation."
                ),
                citations=[
                    ProviderCitation(evidence_id=evidence_id)
                    for evidence_id in evidence_by_competency.get(competency.name, [])
                ],
            )
            for competency in evaluation_input.role.competencies
        ]
        # Ground strengths/concerns in the first available evidence id (empty if none, so
        # the mock never emits an uncited claim). Clearly marked [MOCK].
        first_evidence = next(
            (item.evidence_id for task in evaluation_input.tasks for item in task.evidence), None
        )
        observations = [ProviderCitation(evidence_id=first_evidence)] if first_evidence else []
        return ProviderResult(
            competency_assessments=assessments,
            strengths=(
                [ProviderObservation(text="[MOCK] Placeholder strength.", citations=observations)]
                if observations
                else []
            ),
            concerns=(
                [ProviderObservation(text="[MOCK] Placeholder concern.", citations=observations)]
                if observations
                else []
            ),
            recommendation=self._RECOMMENDATION,
            # A raw provider signal; platform confidence ignores it. Deliberately NOT a
            # round number so a test can prove the persisted confidence is the platform's,
            # not this.
            provider_confidence=0.42,
        )


def get_ai_provider() -> AIProvider:
    """Select the provider from governed config (`AI_PROVIDER`). Default and test value is
    `mock` (the deterministic in-process provider — no network, no cost). `anthropic`
    requires explicit configuration (API key). An unknown value FAILS CLEARLY — we never
    silently fall back to the mock, which could make fake intelligence look real."""
    from app.config import get_settings  # local import avoids a settings import cycle

    provider = get_settings().ai_provider
    if provider == "mock":
        return DeterministicMockAIProvider()
    if provider == "anthropic":
        # Lazy import so the SDK is only touched when Anthropic is actually selected.
        from app.platform.anthropic_provider import build_anthropic_provider

        return build_anthropic_provider(get_settings())
    if provider == "gemini":
        from app.platform.gemini_provider import build_gemini_provider

        return build_gemini_provider(get_settings())
    raise ValueError(
        f"Unknown AI_PROVIDER '{provider}' (expected 'mock', 'anthropic', or 'gemini')."
    )
