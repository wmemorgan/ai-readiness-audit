"""Deterministic scoring: banded answers -> dimension bands -> an overall band.

The scoring contract is locked and reproducible. It exposes explicit per-dimension
weights, explicit question weights (default equal), and explicit band cut-lines
(:mod:`banding`). No clock, randomness, network, or model call participates — an identical
set of answers always yields an identical band. That property is guaranteed structurally:
this module imports only sibling domain modules, none of which perform I/O.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .banding import band_from_score
from .models import Band, DimensionResult
from .questions import QUESTIONS, questions_for
from .remediation import gaps_for_dimension
from .rubric import DIMENSIONS


@dataclass(frozen=True)
class ScoringContract:
    """The locked, inspectable scoring configuration.

    ``dimension_weights`` weight the per-dimension scores when forming the overall score.
    ``question_weight`` is the per-question weight within a dimension (uniform by default).
    Defaults are equal weighting, which keeps the overall band a faithful mean of the
    dimension bands. Remediation *ordering* is handled separately (see :mod:`remediation`).
    """

    dimension_weights: Mapping[str, float]
    question_weight: float = 1.0

    def weight_for(self, dimension_key: str) -> float:
        return self.dimension_weights.get(dimension_key, 1.0)


DEFAULT_CONTRACT = ScoringContract(
    dimension_weights={d.key: 1.0 for d in DIMENSIONS},
    question_weight=1.0,
)

# Answers map a question id to the band the respondent selected.
Answers = Mapping[str, Band]


def _dimension_score(dimension_key: str, answers: Answers, contract: ScoringContract) -> float:
    questions = questions_for(dimension_key)
    weight = contract.question_weight
    total = sum(int(answers[q.id]) * weight for q in questions)
    return total / (len(questions) * weight)


def score_dimensions(
    answers: Answers, contract: ScoringContract = DEFAULT_CONTRACT
) -> tuple[DimensionResult, ...]:
    """Score every locked dimension into a band plus its surfaced gaps."""
    results: list[DimensionResult] = []
    for dim in DIMENSIONS:
        score = _dimension_score(dim.key, answers, contract)
        band = band_from_score(score)
        gaps = gaps_for_dimension(dim, answers)
        results.append(DimensionResult(dimension=dim, score=score, band=band, gaps=gaps))
    return tuple(results)


def overall_score(
    dimension_results: tuple[DimensionResult, ...], contract: ScoringContract = DEFAULT_CONTRACT
) -> float:
    """Combine dimension scores into an overall 1.0..5.0 score under the locked weights."""
    weighted = sum(r.score * contract.weight_for(r.dimension.key) for r in dimension_results)
    total_weight = sum(contract.weight_for(r.dimension.key) for r in dimension_results)
    return weighted / total_weight


def overall_band(
    dimension_results: tuple[DimensionResult, ...], contract: ScoringContract = DEFAULT_CONTRACT
) -> Band:
    """Assign the overall band from the overall score using the locked cut-lines."""
    return band_from_score(overall_score(dimension_results, contract))


def required_question_ids() -> frozenset[str]:
    """The complete set of question ids an assessment must answer."""
    return frozenset(q.id for q in QUESTIONS)
