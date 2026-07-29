"""Gemini adapter tests — with a FAKE client (CI makes ZERO real model calls).

Covers: structured-output success, pseudonymous-id mapping, the MANDATORY egress-payload
PII/UUID-exclusion test, error→sanitized ProviderError, malformed output, unknown citation,
usage extraction, provenance, and end-to-end validation through the shared pipeline.
"""

import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

from app.config.settings import Settings
from app.modules.intelligence.assembler import EvaluationInputAssembler
from app.modules.intelligence.enums import EvaluationFailureReason
from app.modules.intelligence.schemas import (
    CompetencyContext,
    EvaluationInput,
    EvidenceItem,
    RoleContext,
    TaskEvidenceInput,
)
from app.modules.intelligence.service import IntelligenceService
from app.platform.ai import ProviderError, get_ai_provider
from app.platform.gemini_provider import GeminiAIProvider

# --- fake Gemini Interactions client ----------------------------------------- #


class _Usage:
    def __init__(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


class _Interaction:
    def __init__(self, output_text: str, usage: _Usage | None) -> None:
        self.output_text = output_text
        self.usage = usage
        self.response_id = "resp_test_123"


class _FakeInteractions:
    def __init__(self, interaction: _Interaction | None, error: Exception | None) -> None:
        self._interaction = interaction
        self._error = error
        self.calls = 0
        self.captured: dict[str, object] | None = None

    async def create(self, **kwargs: object) -> _Interaction:
        self.calls += 1
        self.captured = kwargs
        if self._error is not None:
            raise self._error
        assert self._interaction is not None
        return self._interaction


class _FakeClient:
    def __init__(
        self, *, interaction: _Interaction | None = None, error: Exception | None = None
    ) -> None:
        self.interactions = _FakeInteractions(interaction, error)


def _output_json(*, citations: tuple[str, ...] = ("E1",), recommendation: str = "PROCEED") -> str:
    return json.dumps(
        {
            "competency_assessments": [
                {
                    "competency": "SQL",
                    "assessment": "Uses a windowed CTE.",
                    "citations": [{"evidence_id": c} for c in citations],
                }
            ],
            "strengths": [
                {"text": "Set-based reasoning.", "citations": [{"evidence_id": citations[0]}]}
            ],
            "concerns": [],
            "recommendation": recommendation,
        }
    )


def _interaction(**kwargs: object) -> _Interaction:
    return _Interaction(_output_json(**kwargs), _Usage(200, 60))  # type: ignore[arg-type]


def _provider(client: _FakeClient) -> GeminiAIProvider:
    return GeminiAIProvider(client, model="gemini-test")


def _input() -> EvaluationInput:
    return EvaluationInput(
        evaluation_id="eval-1",
        role=RoleContext(
            role_title="Data Engineer", bar="senior", competencies=(CompetencyContext(name="SQL"),)
        ),
        tasks=(
            TaskEvidenceInput(
                task_id="task-1",
                prompt="Dedupe a table.",
                evidence_intent="SQL reasoning.",
                competencies=("SQL",),
                evidence=(EvidenceItem(evidence_id="ev-internal-uuid", text="I used a CTE."),),
            ),
        ),
    )


# --- success + id mapping + usage + provenance ------------------------------- #


async def test_success_maps_ids_and_extracts_usage() -> None:
    result = await _provider(_FakeClient(interaction=_interaction())).evaluate(_input())
    assert result.recommendation == "PROCEED"
    assert result.competency_assessments[0].citations[0].evidence_id == "ev-internal-uuid"
    assert result.strengths[0].citations[0].evidence_id == "ev-internal-uuid"
    assert result.usage is not None
    assert result.usage.input_tokens == 200
    assert result.usage.output_tokens == 60


async def test_descriptor_records_exact_model() -> None:
    provider = _provider(_FakeClient(interaction=_interaction()))
    assert provider.descriptor.provider == "gemini"
    assert provider.descriptor.model == "gemini-test"


# --- MANDATORY: egress payload excludes PII and internal ids ----------------- #


async def test_egress_payload_excludes_pii_and_internal_ids(session: AsyncSession) -> None:
    setup = await submitted_evaluation(
        session,
        candidate_name="Grace Hopper",
        candidate_email="grace.hopper@navy.mil",
        competencies=("SQL",),
        answers=(
            "My name is Grace Hopper, email grace.hopper@navy.mil, call +1 415 555 2671. "
            "I used a windowed CTE to dedupe.",
        ),
    )
    evaluation_input = await EvaluationInputAssembler(session, setup.tenant).build(
        setup.evaluation_id
    )
    internal_evidence_id = evaluation_input.tasks[0].evidence[0].evidence_id

    client = _FakeClient(interaction=_interaction())
    await _provider(client).evaluate(evaluation_input)

    payload = json.dumps(client.interactions.captured, default=str)
    assert "Grace Hopper" not in payload
    assert "grace.hopper@navy.mil" not in payload
    assert "555" not in payload
    assert internal_evidence_id not in payload
    assert setup.evaluation_id not in payload
    assert "[E1]" in payload
    assert "Data Engineer" in payload
    assert "windowed CTE to dedupe" in payload


# --- error / malformed / unknown citation ------------------------------------ #


@pytest.mark.parametrize("error", [TimeoutError("t"), ConnectionError("c"), RuntimeError("429")])
async def test_provider_errors_map_to_sanitized_provider_error(error: Exception) -> None:
    client = _FakeClient(error=error)
    with pytest.raises(ProviderError) as exc:
        await _provider(client).evaluate(_input())
    assert str(exc.value) == "The evaluation provider call failed."
    assert "429" not in str(exc.value)
    assert client.interactions.calls == 1  # no adapter retry loop


async def test_non_json_output_is_malformed() -> None:
    interaction = _Interaction("not json at all", _Usage(1, 1))
    result = await _provider(_FakeClient(interaction=interaction)).evaluate(_input())
    assert result.recommendation == "MALFORMED_OUTPUT"


async def test_invented_citation_stays_unmapped() -> None:
    result = await _provider(_FakeClient(interaction=_interaction(citations=("E99",)))).evaluate(
        _input()
    )
    cited = result.competency_assessments[0].citations[0].evidence_id
    assert cited == "E99"
    assert cited != "ev-internal-uuid"


# --- end-to-end through the shared pipeline (validators still run) ------------ #


async def test_gemini_output_validated_end_to_end(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session, competencies=("SQL",))
    provider = _provider(_FakeClient(interaction=_interaction(citations=("E1",))))
    outcome = await IntelligenceService(session, setup.tenant, provider=provider).evaluate(
        setup.evaluation_id
    )
    assert outcome.succeeded
    assert outcome.usage is not None
    assert outcome.usage.input_tokens == 200


async def test_invented_citation_is_ungrounded_end_to_end(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session, competencies=("SQL",))
    provider = _provider(_FakeClient(interaction=_interaction(citations=("E99",))))
    outcome = await IntelligenceService(session, setup.tenant, provider=provider).evaluate(
        setup.evaluation_id
    )
    assert not outcome.succeeded
    assert outcome.failure is not None
    assert outcome.failure.reason == EvaluationFailureReason.UNGROUNDED_OUTPUT


# --- provider selection: no silent fallback ---------------------------------- #


def test_gemini_selection_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    get_ai_provider.cache_clear() if hasattr(get_ai_provider, "cache_clear") else None
    from app.config import settings as settings_module

    settings_module.get_settings.cache_clear()
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        get_ai_provider()
    settings_module.get_settings.cache_clear()


def test_unknown_provider_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.config import settings as settings_module

    settings_module.get_settings.cache_clear()
    monkeypatch.setenv("AI_PROVIDER", "nonsense")
    with pytest.raises(ValueError, match="Unknown AI_PROVIDER"):
        get_ai_provider()
    settings_module.get_settings.cache_clear()


def test_settings_expose_gemini_config() -> None:
    s = Settings(gemini_api_key="k", gemini_model="gemini-3.6-flash")
    assert s.gemini_model == "gemini-3.6-flash"
