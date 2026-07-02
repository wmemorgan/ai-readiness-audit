"""The assessment use-case: banded answers in, a ReadinessReport out.

Pure orchestration over the domain. Given a complete set of answers it produces the hero
deliverable — an advisory, banded readiness report with prioritized remediation and a
routing call to action. It performs no I/O.
"""

from __future__ import annotations

from collections.abc import Mapping

from ..domain.models import Band, ReadinessReport
from ..domain.remediation import prioritized_remediation
from ..domain.scoring import (
    DEFAULT_CONTRACT,
    ScoringContract,
    overall_band,
    overall_score,
    required_question_ids,
    score_dimensions,
)

ADVISORY_NOTICE = (
    "This is an advisory readiness diagnostic, not a certification. It describes structural "
    "readiness against the AI-Readiness Standard; it is not a guarantee that any particular "
    "AI deployment will succeed."
)

ROUTING_CTA = (
    "Close the gaps this diagnostic surfaced: the prioritized remediation list above is the "
    "starting point for a readiness engagement."
)

_VERDICTS: dict[Band, str] = {
    Band.L1: "Ad hoc — establish accountability and a written policy before building.",
    Band.L2: "Emerging — formalize ownership and name your AI-specific risks.",
    Band.L3: "Defined — you have the foundations; invest in controls and measurement next.",
    Band.L4: "Governed — strong footing; tighten assurance and third-party posture.",
    Band.L5: "Optimized — continuous assurance in place; sustain and audit it.",
}


class IncompleteAssessment(ValueError):
    """Raised when required answers are missing."""


def assess(
    answers: Mapping[str, Band], contract: ScoringContract = DEFAULT_CONTRACT
) -> ReadinessReport:
    """Score a complete assessment into a ReadinessReport."""
    missing = required_question_ids() - set(answers)
    if missing:
        raise IncompleteAssessment(f"missing answers for: {sorted(missing)}")

    dimension_results = score_dimensions(answers, contract)
    band = overall_band(dimension_results, contract)
    score = overall_score(dimension_results, contract)
    remediation = prioritized_remediation(dimension_results)

    return ReadinessReport(
        overall_score=score,
        overall_band=band,
        verdict=_VERDICTS[band],
        dimension_results=dimension_results,
        prioritized_remediation=remediation,
        advisory_notice=ADVISORY_NOTICE,
        routing_cta=ROUTING_CTA,
    )
