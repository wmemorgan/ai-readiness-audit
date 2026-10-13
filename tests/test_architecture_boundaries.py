"""The domain core imports no outer layer — verified by static analysis of the source.

This is a self-contained guard (no external tool needed). The import-linter contract in CI
enforces the same rule across every module and dependency direction.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "ai_readiness_audit"
FORBIDDEN_FOR_DOMAIN = ("adapters", "application", "interface", "config")


def _imports(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_domain_modules_do_not_import_outer_layers() -> None:
    for module_path in (SRC / "domain").rglob("*.py"):
        for imported in _imports(module_path):
            for banned in FORBIDDEN_FOR_DOMAIN:
                assert f"ai_readiness_audit.{banned}" not in imported, (
                    f"{module_path.name} imports outer layer {banned}"
                )


def test_narration_does_not_import_the_scoring_core() -> None:
    for module_path in (SRC / "adapters" / "narration").rglob("*.py"):
        for imported in _imports(module_path):
            assert "domain.scoring" not in imported
            assert "domain.remediation" not in imported
            assert "application.assess" not in imported
