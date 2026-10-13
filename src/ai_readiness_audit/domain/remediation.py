"""Gap extraction and prioritized remediation ordering.

Ordering reflects real failure order: Governance & Decision Rights and Measurement &
Assurance gaps surface first (they are where organizations fail first), then remaining
gaps by severity. Ordering is deterministic and total — ties break on a stable key.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .models import Band, Dimension, DimensionResult, Gap
from .questions import questions_for
from .rubric import DIMENSIONS, REMEDIATION_FIRST

# A question scoring at or below this band is treated as a gap worth surfacing.
GAP_THRESHOLD: Band = Band.L3

# The most gaps to name per dimension in its result.
MAX_GAPS_PER_DIMENSION: int = 3

_DIMENSION_ORDER: dict[str, int] = {d.key: i for i, d in enumerate(DIMENSIONS)}


def _priority_rank(dimension_key: str) -> int:
    return 0 if dimension_key in REMEDIATION_FIRST else 1


def gaps_for_dimension(dimension: Dimension, answers: Mapping[str, Band]) -> tuple[Gap, ...]:
    """Return up to ``MAX_GAPS_PER_DIMENSION`` gaps, most severe first."""
    gaps: list[Gap] = []
    for question in questions_for(dimension.key):
        band = answers[question.id]
        if band <= GAP_THRESHOLD:
            gaps.append(
                Gap(
                    dimension_key=dimension.key,
                    dimension_name=dimension.name,
                    question_id=question.id,
                    prompt=question.prompt,
                    current_band=band,
                    severity=int(Band.L5) - int(band),
                    priority_rank=_priority_rank(dimension.key),
                )
            )
    gaps.sort(key=lambda g: (-g.severity, g.question_id))
    return tuple(gaps[:MAX_GAPS_PER_DIMENSION])


def prioritized_remediation(dimension_results: Sequence[DimensionResult]) -> tuple[Gap, ...]:
    """Flatten and order every surfaced gap across dimensions.

    Sort key: priority rank (governance + measurement first), then severity (desc),
    then the locked dimension order, then question id — a total, stable ordering.
    """
    all_gaps: list[Gap] = []
    for result in dimension_results:
        all_gaps.extend(result.gaps)

    all_gaps.sort(
        key=lambda g: (
            g.priority_rank,
            -g.severity,
            _DIMENSION_ORDER[g.dimension_key],
            g.question_id,
        )
    )
    return tuple(all_gaps)
