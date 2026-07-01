"""The pure domain core: models, the rubric lock, questions, scoring, banding, remediation.

Nothing in this package performs I/O or imports a framework. That purity is what makes the
scoring reproducible and is enforced by the architecture-boundary test and the import contract.
"""

from __future__ import annotations

from .banding import band_from_score
from .models import (
    AnswerOption,
    Band,
    Dimension,
    DimensionResult,
    Gap,
    Question,
    ReadinessReport,
)
from .questions import QUESTIONS, questions_for
from .remediation import gaps_for_dimension, prioritized_remediation
from .rubric import CITED_FRAMEWORKS, DIMENSIONS
from .scoring import (
    DEFAULT_CONTRACT,
    ScoringContract,
    overall_band,
    overall_score,
    required_question_ids,
    score_dimensions,
)

__all__ = [
    "AnswerOption",
    "Band",
    "CITED_FRAMEWORKS",
    "DEFAULT_CONTRACT",
    "DIMENSIONS",
    "Dimension",
    "DimensionResult",
    "Gap",
    "QUESTIONS",
    "Question",
    "ReadinessReport",
    "ScoringContract",
    "band_from_score",
    "gaps_for_dimension",
    "overall_band",
    "overall_score",
    "prioritized_remediation",
    "questions_for",
    "required_question_ids",
    "score_dimensions",
]
