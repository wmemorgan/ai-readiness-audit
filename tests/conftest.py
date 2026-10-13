"""Shared test helpers for building complete assessments."""

from __future__ import annotations

from collections.abc import Mapping

from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.questions import QUESTIONS, questions_for


def uniform_answers(band: Band) -> dict[str, Band]:
    """Every question answered at the same band."""
    return {q.id: band for q in QUESTIONS}


def answers_with_dimension(base: Band, dimension_key: str, dimension_band: Band) -> dict[str, Band]:
    """Every question at ``base`` except one dimension pinned to ``dimension_band``."""
    answers = uniform_answers(base)
    for question in questions_for(dimension_key):
        answers[question.id] = dimension_band
    return answers


def all_question_ids() -> tuple[str, ...]:
    return tuple(q.id for q in QUESTIONS)


def complete(mapping: Mapping[str, Band]) -> bool:
    return set(mapping) == {q.id for q in QUESTIONS}
