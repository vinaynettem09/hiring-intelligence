"""Architecture regression gates (Story 8.2).

Executable, repo-wide guards on the boundaries our design depends on. Unlike a single
module's test, these walk the WHOLE `app/` tree via AST, so a violation anywhere — a new
file, a careless import in an unrelated module — fails the build:

  1. Vendor AI SDKs (`anthropic`, `google.genai`) are confined to their two adapter modules
     AND imported lazily there — so merely importing the app can never reach a model provider
     (the structural backbone of the AI-egress guarantee, generalized beyond the seam).
  2. The intelligence package never imports Candidate PII or mutable draft/response models —
     the AI side of the house cannot even name them.
  3. Production code never imports test-only modules.

These encode INV-012 (AI boundary), the AI/PII privacy boundary, and the provider ACL.
"""

import ast
from pathlib import Path

import app

_APP_ROOT = Path(app.__file__).resolve().parent
_APP_FILES = sorted(_APP_ROOT.rglob("*.py"))

# The ONLY modules permitted to touch a real vendor SDK. Everything else must go through the
# `AIProvider` seam (app/platform/ai.py), which selects an adapter lazily.
_ADAPTER_FILES = {"anthropic_provider.py", "gemini_provider.py"}
# Match the TOP-LEVEL package of an import (`anthropic`, `google.genai`) — not a substring,
# so our own adapter module path `app.platform.anthropic_provider` is NOT mistaken for the SDK.
_VENDOR_SDK_ROOTS = {"anthropic", "google"}


def _is_vendor_sdk(target: str) -> bool:
    return target.split(".")[0] in _VENDOR_SDK_ROOTS


def _imports(tree: ast.AST, *, _in_func: bool = False) -> list[tuple[str, bool]]:
    """Every import in the tree as (target, is_module_scope). An import nested inside a
    function/method is `is_module_scope=False` (i.e. lazy — not executed at import time)."""
    out: list[tuple[str, bool]] = []
    for child in ast.iter_child_nodes(tree):
        if isinstance(child, ast.Import):
            out.extend((alias.name, not _in_func) for alias in child.names)
        elif isinstance(child, ast.ImportFrom):
            out.append((child.module or "", not _in_func))
        elif isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
            out.extend(_imports(child, _in_func=True))
        else:
            out.extend(_imports(child, _in_func=_in_func))
    return out


def _parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"))


def test_app_tree_is_non_empty() -> None:
    # Guards against a broken glob silently making every other test here vacuously pass.
    assert len(_APP_FILES) > 50


def test_vendor_ai_sdk_is_confined_to_adapters_and_lazy() -> None:
    offenders: list[str] = []
    for path in _APP_FILES:
        for target, is_module_scope in _imports(_parse(path)):
            if not _is_vendor_sdk(target):
                continue
            where = path.relative_to(_APP_ROOT)
            if path.name not in _ADAPTER_FILES:
                offenders.append(f"{where}: imports vendor SDK '{target}' outside an adapter")
            elif is_module_scope:
                offenders.append(f"{where}: vendor SDK '{target}' at module scope (must be lazy)")
    assert not offenders, "AI-egress boundary violated:\n" + "\n".join(offenders)


def test_intelligence_never_imports_pii_or_draft_models() -> None:
    forbidden = ("candidates.models", "modules.responses")
    offenders: list[str] = []
    for path in _APP_FILES:
        if "intelligence" not in path.parts:
            continue
        for target, _ in _imports(_parse(path)):
            if any(f in target for f in forbidden):
                offenders.append(f"{path.relative_to(_APP_ROOT)}: imports '{target}'")
    assert not offenders, "intelligence reached PII/draft models:\n" + "\n".join(offenders)


def test_production_code_never_imports_tests() -> None:
    offenders: list[str] = []
    for path in _APP_FILES:
        for target, _ in _imports(_parse(path)):
            if target.split(".")[0] in {"tests", "support"}:
                offenders.append(f"{path.relative_to(_APP_ROOT)}: imports test module '{target}'")
    assert not offenders, "production code imports tests:\n" + "\n".join(offenders)
