"""AC-9 / AC-13: the encoded rubric equals the ratified lock, FFIEC lineage intact."""

from __future__ import annotations

from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.rubric import DIMENSIONS

# The ratified lock (SPEC-2026-0701 Table R): key -> (name, FFIEC domain).
LOCKED: dict[str, tuple[str, str]] = {
    "governance_decision_rights": ("Governance & Decision Rights", "Management + Audit oversight"),
    "risk_control_posture": ("Risk & Control Posture", "Risk Management + Information Security"),
    "data_readiness": ("Data Readiness", "Operations"),
    "security_privacy": ("Security & Privacy", "Information Security"),
    "talent_operating_model": (
        "Talent & Operating Model",
        "Development & Acquisition + Management",
    ),
    "third_party_concentration_risk": ("Third-Party & Concentration Risk", "Outsourcing"),
    "measurement_assurance": ("Measurement & Assurance", "Audit"),
}

LOCKED_BANDS: dict[int, str] = {
    1: "Ad hoc",
    2: "Emerging",
    3: "Defined",
    4: "Governed",
    5: "Optimized",
}


def test_exactly_seven_dimensions_in_locked_order() -> None:
    assert tuple(d.key for d in DIMENSIONS) == tuple(LOCKED)


def test_each_dimension_matches_the_lock() -> None:
    for dim in DIMENSIONS:
        name, ffiec = LOCKED[dim.key]
        assert dim.name == name
        assert dim.ffiec_domain == ffiec
        assert dim.core_question  # every dimension carries its examination question


def test_five_bands_with_locked_names() -> None:
    assert [b.value for b in Band] == [1, 2, 3, 4, 5]
    assert {b.value: b.title for b in Band} == LOCKED_BANDS
