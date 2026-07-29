"""Developer-only baseline diff (Story 5.4A). NOT run in CI.

Diffs two A-G baseline files written by `run_quality_eval.py` so a prompt/model/confidence
change can be reviewed against the SAME synthetic inputs instead of by feel. Aligns by
fixture key and reports, per fixture, what moved across: recommendation, confidence,
escalation, competency assessments, strengths, concerns, citations, latency, and token
usage. Pure and offline — it only reads two JSON files.

    uv run python scripts/compare_baselines.py <old_baseline.json> <new_baseline.json>
"""

import json
import sys
from pathlib import Path
from typing import Any

_MARK = "  <-- changed"


def _load(path: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return data


def _by_fixture(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["fixture"]: entry for entry in payload.get("results", [])}


def _dimensions(entry: dict[str, Any] | None) -> dict[str, Any]:
    """The comparable signals for one fixture's outcome (tolerates a failed outcome)."""
    if entry is None:
        return {"present": False}
    outcome = entry.get("outcome", {})
    proposal = outcome.get("proposal")
    usage = outcome.get("usage") or {}
    if proposal is None:
        failure = outcome.get("failure") or {}
        return {
            "present": True,
            "recommendation": f"FAILED:{failure.get('reason')}",
            "confidence": None,
            "escalation": None,
            "assessments": 0,
            "citations": 0,
            "strengths": 0,
            "concerns": 0,
            "latency_ms": entry.get("latency_ms"),
            "input_tokens": None,
            "output_tokens": None,
        }
    return {
        "present": True,
        "recommendation": proposal.get("recommendation"),
        "confidence": proposal.get("confidence"),
        "escalation": proposal.get("escalation_reason"),
        "assessments": len(proposal.get("competency_assessments", [])),
        "citations": sum(
            len(a.get("evidence_citations", [])) for a in proposal.get("competency_assessments", [])
        ),
        "strengths": len(proposal.get("strengths", [])),
        "concerns": len(proposal.get("concerns", [])),
        "latency_ms": entry.get("latency_ms"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
    }


_FIELDS = (
    "recommendation",
    "confidence",
    "escalation",
    "assessments",
    "citations",
    "strengths",
    "concerns",
    "latency_ms",
    "input_tokens",
    "output_tokens",
)


def _header(label: str, payload: dict[str, Any]) -> str:
    return (
        f"{label}: {payload.get('provider')} / {payload.get('model')} / "
        f"{payload.get('prompt_version')} / {payload.get('confidence_algorithm_version')}"
    )


def _run(old_path: str, new_path: str) -> int:
    old, new = _load(old_path), _load(new_path)
    print(_header("OLD", old))
    print(_header("NEW", new))
    print()

    old_by, new_by = _by_fixture(old), _by_fixture(new)
    keys = sorted(set(old_by) | set(new_by))
    changed_fixtures = 0

    for key in keys:
        o, n = _dimensions(old_by.get(key)), _dimensions(new_by.get(key))
        diffs = [f for f in _FIELDS if o.get(f) != n.get(f)]
        # Recommendation / escalation moves are the ones a reviewer cares about most.
        material = any(f in diffs for f in ("recommendation", "escalation"))
        flag = " ***RECOMMENDATION MOVED***" if material else ""
        status = "changed" if diffs else "same"
        print(f"[{key}] {status}{flag}")
        if not o["present"]:
            print("    (absent in OLD)")
        if not n["present"]:
            print("    (absent in NEW)")
        for field in _FIELDS:
            ov, nv = o.get(field), n.get(field)
            if ov != nv:
                print(f"    {field}: {ov} -> {nv}{_MARK}")
        if diffs:
            changed_fixtures += 1
        print()

    print(f"{changed_fixtures}/{len(keys)} fixtures changed.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python scripts/compare_baselines.py <old_baseline.json> <new_baseline.json>")
        raise SystemExit(2)
    raise SystemExit(_run(sys.argv[1], sys.argv[2]))
