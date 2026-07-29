"""Centralized version constants + the governed prompt loader.

Every evaluation proposal carries provenance (see schemas.Provenance) so we can later
reconstruct *exactly* how it was produced. Versions are declared here in ONE place —
never sprinkled as string literals — and bumped deliberately when a contract changes.
The prompt version is the source-of-truth file `prompts/evaluation/VERSION`, so editing
the prompt and forgetting to bump provenance is impossible.
"""

from pathlib import Path

# Schema/algorithm contract versions. Bump when the shape or the computation changes.
INPUT_SCHEMA_VERSION = "eval-input-v1"
OUTPUT_SCHEMA_VERSION = "eval-proposal-v1"
# v2 (Story 5.4A): sufficiency x decisiveness, replacing v1's coverage-only heuristic
# (TD-016). Historical Evaluations keep whatever version they were written under.
CONFIDENCE_ALGORITHM_VERSION = "confidence-v2"

_PROMPT_DIR = Path(__file__).parent / "prompts" / "evaluation"


def prompt_version() -> str:
    """The governed prompt contract's version (from prompts/evaluation/VERSION)."""
    return (_PROMPT_DIR / "VERSION").read_text(encoding="utf-8").strip()


def load_prompt(name: str) -> str:
    """Read a governed prompt template by filename (e.g. 'system.md'). Templates are not
    used by the mock provider in Story 5.1; they define the contract the real provider
    adapter will render, and their version is recorded in provenance today."""
    return (_PROMPT_DIR / name).read_text(encoding="utf-8")
