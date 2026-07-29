"""Deterministic PII minimizer — the transient AI-safe projection of candidate text.
Evidence itself is never mutated; the assembler applies this on the way to the provider."""

from app.platform.pii import DeterministicPIIMinimizer


def _m(text: str) -> str:
    return DeterministicPIIMinimizer().minimize(text).text


def _redactions(text: str) -> int:
    return DeterministicPIIMinimizer().minimize(text).redactions


def test_redacts_email() -> None:
    out = _m("Reach me at ada.lovelace@example.com any time.")
    assert "ada.lovelace@example.com" not in out
    assert "[redacted:email]" in out


def test_redacts_url() -> None:
    out = _m("My portfolio is https://ada.dev/work and www.ada.dev too.")
    assert "ada.dev" not in out
    assert out.count("[redacted:url]") == 2


def test_redacts_phone_but_keeps_ordinary_numbers() -> None:
    out = _m("Call +1 (415) 555-2671. I have 5 years and shipped 3 systems in 2024.")
    assert "555" not in out
    assert "[redacted:phone]" in out
    # Small, non-phone numbers survive — they can be job-relevant signal.
    assert "5 years" in out
    assert "2024" in out


def test_redacts_explicit_self_identification() -> None:
    out = _m("My name is Grace Hopper and I built compilers.")
    assert "Grace Hopper" not in out
    assert "[redacted:name]" in out
    assert "built compilers" in out  # the substance is preserved


def test_is_deterministic() -> None:
    text = "I'm Ada, email ada@x.com, phone +1 415 555 2671, site https://x.com."
    assert _m(text) == _m(text)


def test_does_not_mutate_or_lose_substance() -> None:
    text = "I normalized the table, then wrote a windowed query to dedupe rows."
    assert _m(text) == text  # nothing PII-like → unchanged


def test_handles_empty() -> None:
    assert _m("") == ""


def test_redacts_street_address() -> None:
    out = _m("I live at 123 Main Street and commute daily.")
    assert "123 Main Street" not in out
    assert "[redacted:address]" in out


def test_reports_redaction_count() -> None:
    # email + url + phone = 3 redactions; the count never carries the values.
    n = _redactions("Email a@b.com, site https://x.com, phone +1 415 555 2671.")
    assert n == 3
    assert _redactions("Just a plain job-relevant answer.") == 0
