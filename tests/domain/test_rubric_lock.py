"""AC-9 / AC-13: the encoded rubric equals the ratified lock; standards lineage intact."""

from __future__ import annotations

from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.rubric import DIMENSIONS

# The ratified lock (SPEC-2026-0701 Table R): key -> (name, iso_lineage, nist_function).
LOCKED: dict[str, tuple[str, str, str]] = {
    "governance_decision_rights": (
        "Governance & Decision Rights",
        "ISO/IEC 42001 Cl. 5 (Leadership) + ISO/IEC 38507 (AI governance)",
        "GOVERN",
    ),
    "risk_control_posture": (
        "Risk & Control Posture",
        "ISO/IEC 23894 (AI risk mgmt) + ISO/IEC 42001 Cl. 6 (Planning)",
        "MAP + MANAGE",
    ),
    "data_readiness": (
        "Data Readiness",
        "ISO/IEC 42001 Annex A (Data for AI) + ISO/IEC 5259 (data quality)",
        "MAP",
    ),
    "security_privacy": (
        "Security & Privacy",
        "ISO/IEC 27001 (ISMS) + ISO/IEC 27701 (Privacy)",
        "MANAGE (GenAI Profile risk themes)",
    ),
    "talent_operating_model": (
        "Talent & Operating Model",
        "ISO/IEC 42001 Cl. 7 (Support — competence & awareness)",
        "GOVERN",
    ),
    "third_party_concentration_risk": (
        "Third-Party & Concentration Risk",
        "ISO/IEC 42001 Annex A (Suppliers) + ISO/IEC 27036 (supplier sec.)",
        "GOVERN + MANAGE",
    ),
    "measurement_assurance": (
        "Measurement & Assurance",
        "ISO/IEC 42001 Cl. 9 (Performance eval) + ISO/IEC 42005 (impact)",
        "MEASURE",
    ),
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
        name, iso_lineage, nist_function = LOCKED[dim.key]
        assert dim.name == name
        assert dim.iso_lineage == iso_lineage
        assert dim.nist_function == nist_function
        assert dim.core_question  # every dimension carries its core question


def test_five_bands_with_locked_names() -> None:
    assert [b.value for b in Band] == [1, 2, 3, 4, 5]
    assert {b.value: b.title for b in Band} == LOCKED_BANDS
