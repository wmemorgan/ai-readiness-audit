"""Shared prompt construction for narration providers.

Builds a prompt from a *finished* report only. It reads bands and gaps — never raw answers,
weights, or cut-lines — so a provider cannot reconstruct or influence the score.
"""

from __future__ import annotations

from ...domain.models import ReadinessReport


def narration_prompt(report: ReadinessReport) -> str:
    dimensions = "\n".join(
        f"- {r.dimension.name}: {r.band.title}" for r in report.dimension_results
    )
    gaps = "\n".join(
        f"- {g.dimension_name}: {g.prompt}" for g in report.prioritized_remediation
    )
    return (
        "Write a concise, plain-language summary of this AI-readiness result for an executive. "
        "Do not invent a score or change any band; narrate only what is given.\n\n"
        f"Overall band: {report.overall_band.title} ({report.overall_band.name})\n"
        f"Verdict: {report.verdict}\n\n"
        f"By dimension:\n{dimensions}\n\n"
        f"Prioritized gaps:\n{gaps}\n"
    )
