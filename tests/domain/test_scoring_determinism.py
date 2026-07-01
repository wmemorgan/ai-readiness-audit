"""AC-1 / AC-10: identical answers replay to identical bands; the contract is explicit."""

from __future__ import annotations

from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.scoring import DEFAULT_CONTRACT
from ai_readiness_audit.interface.sample_org import sample_answers


def test_identical_answers_replay_to_identical_report() -> None:
    answers = sample_answers()
    first = assess(answers)
    second = assess(dict(answers))
    assert first.overall_band == second.overall_band
    assert first.overall_score == second.overall_score
    assert [r.band for r in first.dimension_results] == [r.band for r in second.dimension_results]
    assert [r.score for r in first.dimension_results] == [r.score for r in second.dimension_results]


def test_repeated_scoring_is_stable_across_many_runs() -> None:
    answers = sample_answers()
    bands = {assess(dict(answers)).overall_band for _ in range(50)}
    assert len(bands) == 1


def test_contract_exposes_explicit_weights() -> None:
    for weight in DEFAULT_CONTRACT.dimension_weights.values():
        assert isinstance(weight, float)
        assert weight > 0
    assert isinstance(DEFAULT_CONTRACT.question_weight, float)


def test_uniform_answers_land_on_that_band() -> None:
    for band in Band:
        answers = {qid: band for qid in sample_answers()}
        assert assess(answers).overall_band == band
