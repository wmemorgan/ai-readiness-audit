"""AC-14 support: every dimension has a complete banded question set."""

from __future__ import annotations

from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.questions import QUESTIONS, questions_for
from ai_readiness_audit.domain.rubric import DIMENSIONS


def test_every_dimension_has_questions() -> None:
    for dim in DIMENSIONS:
        assert questions_for(dim.key), f"{dim.key} has no questions"


def test_question_ids_are_unique() -> None:
    ids = [q.id for q in QUESTIONS]
    assert len(ids) == len(set(ids))


def test_every_question_offers_the_full_band_ladder() -> None:
    for q in QUESTIONS:
        bands = [opt.band for opt in q.options]
        assert bands == [Band.L1, Band.L2, Band.L3, Band.L4, Band.L5]
        assert all(opt.label for opt in q.options)


def test_every_question_belongs_to_a_locked_dimension() -> None:
    keys = {d.key for d in DIMENSIONS}
    assert all(q.dimension_key in keys for q in QUESTIONS)
