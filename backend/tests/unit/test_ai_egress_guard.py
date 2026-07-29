"""Egress guard (Story 8.1): CI and tests must NEVER be able to contact a live model.

This is a *structural* regression guard, not a "we just don't set the key" hope. It proves:
  1. The governed default provider is the deterministic in-process mock.
  2. `get_ai_provider()` under default settings returns that mock (no network client built).
  3. Importing the provider seam does not import a real vendor SDK as a side effect —
     the real adapters are lazy-imported only when explicitly selected.

If a future change makes a live provider reachable by default, or eagerly imports a vendor
SDK at module load, one of these fails — before it can silently egress candidate evidence.
"""

import ast
from pathlib import Path

import app.platform.ai as ai_module
from app.config import Settings
from app.platform.ai import DeterministicMockAIProvider, get_ai_provider


def test_default_provider_is_mock() -> None:
    # The governed default is the deterministic mock — safe, free, offline.
    assert Settings().ai_provider == "mock"


def test_get_ai_provider_returns_mock_under_default_settings() -> None:
    # No API key, default config -> the in-process mock. Never a network-backed client.
    assert isinstance(get_ai_provider(), DeterministicMockAIProvider)


def _module_level_imports(source: str) -> set[str]:
    """The module's TOP-LEVEL import targets only (imports nested inside functions — i.e.
    lazy imports — are intentionally excluded)."""
    tree = ast.parse(source)
    targets: set[str] = set()
    for node in tree.body:  # module scope only — not ast.walk
        if isinstance(node, ast.Import):
            targets.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            targets.add(node.module or "")
    return targets


def test_seam_does_not_import_a_vendor_sdk_at_module_scope() -> None:
    # Structural (order-independent): the seam must lazy-import real adapters/SDKs inside
    # get_ai_provider(), never at module load — so merely importing it can't reach the network.
    source = Path(ai_module.__file__).read_text(encoding="utf-8")
    forbidden = ("anthropic", "google", "genai", "gemini")
    offenders = {
        target
        for target in _module_level_imports(source)
        if any(token in target for token in forbidden)
    }
    assert not offenders, f"seam imports a vendor SDK/adapter at module scope: {offenders}"
