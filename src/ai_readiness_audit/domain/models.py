"""Core value objects for the AI Readiness Audit.

This module is part of the pure domain core: it has no I/O, no framework
dependencies, and no knowledge of how answers arrive or how reports leave.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Band(IntEnum):
    """The five-level organizational maturity band, low to high.

    The names are the authored AI-Readiness Standard vocabulary; the integer
    values are the deterministic scoring levels a banded answer contributes.
    """

    L1 = 1  # Ad hoc
    L2 = 2  # Emerging
    L3 = 3  # Defined
    L4 = 4  # Governed
    L5 = 5  # Optimized

    @property
    def title(self) -> str:
        return _BAND_TITLES[self]

    @property
    def summary(self) -> str:
        return _BAND_SUMMARIES[self]


_BAND_TITLES: dict[Band, str] = {
    Band.L1: "Ad hoc",
    Band.L2: "Emerging",
    Band.L3: "Defined",
    Band.L4: "Governed",
    Band.L5: "Optimized",
}

_BAND_SUMMARIES: dict[Band, str] = {
    Band.L1: "No policy, no owner, no named risks; experimentation without structure.",
    Band.L2: "Pockets of activity; informal ownership; risks unnamed.",
    Band.L3: "Policy and an accountable owner exist; risks named; basic controls; repeatable.",
    Band.L4: "Controls tested; measurement in place; data governed; human-in-loop by severity.",
    Band.L5: "Continuous assurance; severity-weighted evaluation; autonomous-ready governance.",
}


@dataclass(frozen=True)
class Dimension:
    """One readiness dimension, mapped to the public examination domain it rests on."""

    key: str
    name: str
    ffiec_domain: str
    core_question: str


@dataclass(frozen=True)
class AnswerOption:
    """A selectable answer, carrying the maturity band it evidences."""

    band: Band
    label: str


@dataclass(frozen=True)
class Question:
    """A banded self-assessment question belonging to exactly one dimension."""

    id: str
    dimension_key: str
    prompt: str
    options: tuple[AnswerOption, ...]


@dataclass(frozen=True)
class Gap:
    """A named weakness surfaced by a below-target answer."""

    dimension_key: str
    dimension_name: str
    question_id: str
    prompt: str
    current_band: Band
    severity: int  # distance below the top band; higher = more urgent
    priority_rank: int  # lower rank surfaces first in remediation ordering


@dataclass(frozen=True)
class DimensionResult:
    """The scored outcome for one dimension."""

    dimension: Dimension
    score: float
    band: Band
    gaps: tuple[Gap, ...]


@dataclass(frozen=True)
class ReadinessReport:
    """The hero deliverable: an advisory, banded readiness assessment.

    A ReadinessReport is a description of structural readiness. It is advisory,
    not a certification, and never a guarantee that a given AI deployment will succeed.
    """

    overall_score: float
    overall_band: Band
    verdict: str
    dimension_results: tuple[DimensionResult, ...]
    prioritized_remediation: tuple[Gap, ...]
    advisory_notice: str
    routing_cta: str
