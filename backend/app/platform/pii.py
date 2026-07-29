"""PII minimization platform seam.

`Evidence.response_text` is candidate-authored free text and can contain a name, email,
employer, phone, URL, or address ("My name is Sam, reach me at sam@x.com, 123 Main St").
So evidence is **not** automatically PII-free. Before any candidate text crosses the AI
boundary — and, from Story 5.3, may egress to an external model — it passes through a
`PIIMinimizer`, which returns a **transient, minimized projection**; the authoritative
`Evidence` row is never mutated (auditability + candidate-authored truth are preserved).

Story 5.3 hardens the deterministic minimizer (TD-009): it now covers emails, URLs,
phone numbers, explicit self-identification ("my name is / I'm / this is / call me"),
and obvious street-address patterns. It is **deterministic and local** (no NER, no second
AI call) and errs toward over-redaction. It also reports a **redaction count** so callers
can log `pii_redactions_count` — never *what* was redacted.

**Residual risk (documented, not solved):** regex is not NER. Names without a
self-identifying lead-in, unusual contact formats, employer/location mentions, and
handles inside code answers may pass through. This is a floor for MVP external egress, not
a guarantee. Stronger minimization (NER / provider-side redaction) remains future work.
The **caller must fail closed** if minimization raises — never send raw Evidence.
"""

import re
from dataclasses import dataclass
from typing import Protocol

_EMAIL_MASK = "[redacted:email]"
_URL_MASK = "[redacted:url]"
_PHONE_MASK = "[redacted:phone]"
_NAME_MASK = "[redacted:name]"
_ADDRESS_MASK = "[redacted:address]"

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_URL_RE = re.compile(r"\b(?:https?://|www\.)[^\s<>]+", re.IGNORECASE)
# A run that looks like a phone number — only redacted if it carries ≥7 digits, so
# "2024" / "5 years" / "top 3" survive.
_PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d\s().\-]{5,}\d")
# Explicit self-identification: a literal lead-in + Capitalized name-like tokens.
_NAME_RE = re.compile(
    r"(?i)\b(my name is|i am|i'm|this is|name:|call me)\s+"
    r"(?P<name>[A-Z][A-Za-z'.\-]+(?:\s+[A-Z][A-Za-z'.\-]+){0,2})"
)
# Obvious street address: number + word(s) + a street-type suffix.
_ADDRESS_RE = re.compile(
    r"\b\d{1,5}\s+\w+(?:\s+\w+)?\s+"
    r"(?:street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr|court|ct|way|circle)\b\.?",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MinimizationResult:
    """The AI-safe projection plus how many redactions were applied (for safe logging —
    never carries the redacted values)."""

    text: str
    redactions: int


class PIIMinimizer(Protocol):
    """The seam the AI boundary depends on. Pure (no I/O, no mutation of inputs)."""

    def minimize(self, text: str) -> MinimizationResult: ...


class DeterministicPIIMinimizer:
    """Regex-based, deterministic minimizer. No randomness, no network, no model.

    Order matters: URLs first (so an email-looking fragment in a URL is handled as a URL),
    then emails, addresses, the "my name is …" pattern, then phone-like digit runs last.
    """

    def minimize(self, text: str) -> MinimizationResult:
        if not text:
            return MinimizationResult(text, 0)
        count = 0
        redacted, hits = _URL_RE.subn(_URL_MASK, text)
        count += hits
        redacted, hits = _EMAIL_RE.subn(_EMAIL_MASK, redacted)
        count += hits
        redacted, hits = _ADDRESS_RE.subn(_ADDRESS_MASK, redacted)
        count += hits
        redacted, hits = _NAME_RE.subn(lambda m: f"{m.group(1)} {_NAME_MASK}", redacted)
        count += hits

        phone_hits = 0

        def _phone(match: re.Match[str]) -> str:
            nonlocal phone_hits
            span = match.group(0)
            if sum(character.isdigit() for character in span) >= 7:
                phone_hits += 1
                return _PHONE_MASK
            return span

        redacted = _PHONE_CANDIDATE_RE.sub(_phone, redacted)
        count += phone_hits
        return MinimizationResult(redacted, count)


def get_pii_minimizer() -> PIIMinimizer:
    """The default minimizer. A single seam so a stronger implementation can replace it
    everywhere at once."""
    return DeterministicPIIMinimizer()
