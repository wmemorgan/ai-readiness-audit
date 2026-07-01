"""AC-4: governance + measurement gaps surface first, then by severity."""

from __future__ import annotations

from tests.conftest import uniform_answers

from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.rubric import REMEDIATION_FIRST


def test_governance_and_measurement_lead_the_remediation_list() -> None:
    # All dimensions weak, so every dimension surfaces gaps of equal severity.
    report = assess(uniform_answers(Band.L2))
    ordered_dims = [gap.dimension_key for gap in report.prioritized_remediation]
    leading = ordered_dims[:6]  # two priority dimensions x 3 questions each
    assert set(leading) == set(REMEDIATION_FIRST)


def test_more_severe_gaps_outrank_less_severe_within_priority() -> None:
    answers = uniform_answers(Band.L3)
    # Make one governance question the most severe gap.
    answers["gov-2"] = Band.L1
    report = assess(answers)
    first = report.prioritized_remediation[0]
    assert first.question_id == "gov-2"
    assert first.current_band == Band.L1


def test_a_fully_optimized_org_has_no_remediation() -> None:
    report = assess(uniform_answers(Band.L5))
    assert report.prioritized_remediation == ()
