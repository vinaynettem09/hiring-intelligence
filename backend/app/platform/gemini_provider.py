"""Gemini provider adapter — a THIRD implementation of the `AIProvider` seam, so the same
governed intelligence pipeline and A-G synthetic harness can run through Google's Gemini
Developer API (free tier) without the domain knowing which model answered.

Everything Gemini-specific lives ONLY here. It reuses the provider-independent governed
prompt/schema/parse (`evaluation_prompt.py`), so the egress boundary and `ProviderResult`
contract are identical to the other providers. Gemini adapts to us, never the reverse.

⚠️ DATA POLICY — SYNTHETIC ONLY. The Gemini **free tier** may use submitted content to
improve Google's products. Therefore this provider is for our **synthetic A-G fixtures
only**. Do NOT select `AI_PROVIDER=gemini` for real candidate evaluations while on the
free tier — real Evidence must not egress to a data-retaining free tier. (See TD-017.)

The SDK is imported lazily (only when Gemini is selected + built), so the app and the whole
test suite run without `google-genai` installed. Tests inject a fake client — CI makes ZERO
real model calls.

NOTE: verified against current official Gemini API docs (2026-07-28): SDK `google-genai`
(`from google import genai`, `genai.Client()`), the current **Interactions API**
(`interactions.create(model, input, system_instruction, response_format, generation_config)`
→ `.output_text`), structured JSON via `response_format`, key env `GEMINI_API_KEY`, Flash
model `gemini-3.6-flash`. Token usage is on `interaction.usage` as `total_input_tokens` /
`total_output_tokens` (verified 2026-07-28). The exact async surface, timeout param, and
error classes are still parsed **defensively** and confirmed on the first live run (TD-017).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Protocol

from app.platform.ai import ProviderDescriptor, ProviderError, ProviderResult, ProviderUsage
from app.platform.evaluation_prompt import (
    OUTPUT_SCHEMA,
    parse_structured_output,
    render_evaluation,
)
from app.shared.logging import get_logger

if TYPE_CHECKING:
    from app.config.settings import Settings
    from app.modules.intelligence.schemas import EvaluationInput

_log = get_logger(__name__)


class GeminiClient(Protocol):
    """The minimal async surface the adapter needs — satisfied by the real google-genai
    async Interactions client and by a fake in tests."""

    @property
    def interactions(self) -> Any: ...


class GeminiAIProvider:
    def __init__(self, client: GeminiClient, *, model: str) -> None:
        self._client = client
        self._model = model

    @property
    def descriptor(self) -> ProviderDescriptor:
        # Exact model id in provenance — never merely "Gemini".
        return ProviderDescriptor(provider="gemini", model=self._model, model_version=self._model)

    async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
        rendered = render_evaluation(evaluation_input)
        try:
            interaction = await self._client.interactions.create(
                model=self._model,
                system_instruction=rendered.system,
                input=rendered.user,
                # Force structured JSON constrained by our schema (still re-validated by us).
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": OUTPUT_SCHEMA,
                },
            )
        except Exception as exc:
            # Safe metadata only — never the prompt, payload, response, key, or PII.
            _log.warning("gemini.call_failed", model=self._model, error_type=type(exc).__name__)
            raise ProviderError("The evaluation provider call failed.") from exc

        _log.info(
            "gemini.call_succeeded",
            model=self._model,
            # google-genai exposes a per-response id; best-effort + safe.
            response_id=getattr(interaction, "response_id", None),
        )
        result = _parse(interaction, rendered.id_map)
        return result


def _parse(interaction: Any, id_map: dict[str, str]) -> ProviderResult:
    text = getattr(interaction, "output_text", None)
    if not isinstance(text, str):
        return ProviderResult(recommendation="MALFORMED_OUTPUT", usage=_usage(interaction))
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return ProviderResult(recommendation="MALFORMED_OUTPUT", usage=_usage(interaction))
    if not isinstance(data, dict):
        return ProviderResult(recommendation="MALFORMED_OUTPUT", usage=_usage(interaction))
    result = parse_structured_output(data, id_map)
    return result.model_copy(update={"usage": _usage(interaction)})


def _usage(interaction: Any) -> ProviderUsage | None:
    """Extract token usage. The current Interactions API exposes it on `interaction.usage`
    as `total_input_tokens` / `total_output_tokens` (verified against ai.google.dev docs,
    2026-07-28) — the first live baseline showed None because the earlier code only looked
    for generateContent-era names. We try the verified names first, then fall back to older
    aliases, and log (without values) if usage is present but unrecognized so a future SDK
    rename is caught on the next run rather than silently dropping to None."""
    usage = getattr(interaction, "usage", None) or getattr(interaction, "usage_metadata", None)
    if usage is None:
        return None
    input_tokens = _first_int(
        usage, ("total_input_tokens", "input_tokens", "prompt_token_count", "prompt_tokens")
    )
    output_tokens = _first_int(
        usage,
        ("total_output_tokens", "output_tokens", "candidates_token_count", "completion_tokens"),
    )
    if input_tokens is None or output_tokens is None:
        # Usage object present but neither known name matched — surface the *attribute
        # names* (never values/PII) so the mapping can be corrected without guessing.
        attrs = [name for name in dir(usage) if not name.startswith("_")]
        _log.warning("gemini.usage_unparsed", available_attributes=attrs)
        return None
    return ProviderUsage(input_tokens=input_tokens, output_tokens=output_tokens)


def _first_int(obj: Any, names: tuple[str, ...]) -> int | None:
    for name in names:
        value = getattr(obj, name, None)
        if isinstance(value, int):
            return value
    return None


def build_gemini_provider(settings: Settings) -> GeminiAIProvider:
    """Construct the real adapter. Lazily imports the SDK and requires an explicit API key —
    misconfiguration FAILS CLEARLY (never silently falls back to the mock)."""
    if not settings.gemini_api_key:
        raise ValueError("AI_PROVIDER=gemini requires GEMINI_API_KEY to be configured.")
    try:
        from google import genai  # lazy: only when Gemini is actually selected
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise ValueError(
            "AI_PROVIDER=gemini requires the 'google-genai' package to be installed."
        ) from exc

    # Timeout is set on the client (http options, milliseconds). The async surface is
    # `client.aio` in google-genai; exact Interactions wiring confirmed at live run (TD-017).
    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options={"timeout": int(settings.gemini_timeout_seconds * 1000)},
    )
    return GeminiAIProvider(client.aio, model=settings.gemini_model)
