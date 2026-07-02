"""AC-2: band-boundary correctness across every L1..L5 cut-line, per dimension and overall.

This suite is the calibration gate: it fails if any crafted fixture lands outside its
intended band, or if the cut-lines drift.
"""

from __future__ import annotations

import pytest
from tests.conftest import answers_with_dimension, uniform_answers

from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.banding import band_from_score
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.rubric import DIMENSIONS

# Score just below / at each cut-line -> the expected band.
CUT_LINE_CASES = [
    (1.0, Band.L1),
    (1.49, Band.L1),
    (1.5, Band.L2),
    (2.49, Band.L2),
    (2.5, Band.L3),
    (3.49, Band.L3),
    (3.5, Band.L4),
    (4.49, Band.L4),
    (4.5, Band.L5),
    (5.0, Band.L5),
]


@pytest.mark.parametrize(("score", "expected"), CUT_LINE_CASES)
def test_band_from_score_respects_every_cut_line(score: float, expected: Band) -> None:
    assert band_from_score(score) == expected


@pytest.mark.parametrize("band", list(Band))
def test_uniform_assessment_lands_in_intended_overall_band(band: Band) -> None:
    assert assess(uniform_answers(band)).overall_band == band


@pytest.mark.parametrize("dim", [d.key for d in DIMENSIONS])
@pytest.mark.parametrize("band", list(Band))
def test_each_dimension_lands_in_its_intended_band(dim: str, band: Band) -> None:
    report = assess(answers_with_dimension(Band.L3, dim, band))
    result = next(r for r in report.dimension_results if r.dimension.key == dim)
    assert result.band == band


def test_a_single_low_answer_cannot_silently_pass_as_high() -> None:
    # A dimension of two L5s and one L1 averages 3.67 -> L4, never L5.
    answers = uniform_answers(Band.L5)
    answers["gov-1"] = Band.L1
    report = assess(answers)
    governance = next(
        r for r in report.dimension_results if r.dimension.key == "governance_decision_rights"
    )
    assert governance.band == Band.L4
