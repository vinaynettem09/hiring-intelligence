"""Deterministic fingerprint of the AI-safe input.

A stable SHA-256 over a canonical serialization of the **PII-minimized**
`EvaluationInput`. Because the input is already minimized, the fingerprint is over the
*safe* representation — two candidates whose raw text differed only in redacted PII can
still fingerprint-match, which is exactly what we want.

Purpose: reproducibility, idempotency, debugging, future content-hash caching, and proving
whether two runs actually used identical input. Never uses Python's salted `hash()`.
"""

import hashlib
import json

from app.modules.intelligence.schemas import EvaluationInput

_ALGORITHM = "sha256"


def fingerprint_input(evaluation_input: EvaluationInput) -> str:
    """A stable `sha256:<hex>` fingerprint. Canonicalization is deterministic (sorted
    keys, no insignificant whitespace), so the same safe input always yields the same
    fingerprint across processes and runs."""
    canonical = json.dumps(
        evaluation_input.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"{_ALGORITHM}:{digest}"
