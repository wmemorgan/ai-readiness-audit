"""Authored copy for the AI-Readiness Standard — the standard's own product language.

Centralized so a single edit changes every surface. These are data (no I/O), so they live in
the pure domain alongside the rubric they describe. The public standards named here inform the
diagnostic; they do not define the bands.
"""

from __future__ import annotations

from .models import Dimension

STANDARD_HEADLINE = "The AI-Readiness Standard"
STANDARD_SUBTITLE = "Seven dimensions. Five levels. One honest picture of where you stand."

TAGLINE = (
    "A deterministic AI-readiness diagnostic aligned to ISO/IEC 42001 domains "
    "and NIST AI RMF functions"
)
STANDARD_DESCRIPTOR = (
    "An audit-grade readiness standard aligned to ISO/IEC 42001 domains "
    "and NIST AI RMF functions"
)
THESIS = "These standards inform the diagnostic; they do not define the bands."


def lineage_line(dimension: Dimension, score: float) -> str:
    """Render a dimension's standards lineage and score for a report line."""
    return (
        f"Lineage: {dimension.iso_lineage} · NIST AI RMF: {dimension.nist_function} "
        f"· score {score:.2f}/5"
    )
