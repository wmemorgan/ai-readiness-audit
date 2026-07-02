"""The ratified rubric lock: seven dimensions, their standards lineage, and the bands.

This is the single source of truth for scoring, questions, and report labels. The seven
dimensions and the five bands are a locked contract — the calibration and lock tests fail on
any drift. Each dimension is traced to its ISO/IEC lineage domains and its NIST AI RMF function.
These standards inform the diagnostic; they do not define the bands, which are this standard's
own authored contribution.
"""

from __future__ import annotations

from .models import Band, Dimension

DIMENSIONS: tuple[Dimension, ...] = (
    Dimension(
        key="governance_decision_rights",
        name="Governance & Decision Rights",
        iso_lineage="ISO/IEC 42001 Cl. 5 (Leadership) + ISO/IEC 38507 (AI governance)",
        nist_function="GOVERN",
        core_question=(
            "Is there an accountable executive, a written AI policy, and defined approval gates?"
        ),
    ),
    Dimension(
        key="risk_control_posture",
        name="Risk & Control Posture",
        iso_lineage="ISO/IEC 23894 (AI risk mgmt) + ISO/IEC 42001 Cl. 6 (Planning)",
        nist_function="MAP + MANAGE",
        core_question=(
            "Are AI-specific risks — hallucination, data leakage, prompt injection, blast "
            "radius, drift — named and mapped to controls with human-in-loop gates by severity?"
        ),
    ),
    Dimension(
        key="data_readiness",
        name="Data Readiness",
        iso_lineage="ISO/IEC 42001 Annex A (Data for AI) + ISO/IEC 5259 (data quality)",
        nist_function="MAP",
        core_question=(
            "Is data accessible, governed, quality-assured, lineage-traceable, and "
            "rights/licensing-cleared for AI use?"
        ),
    ),
    Dimension(
        key="security_privacy",
        name="Security & Privacy",
        iso_lineage="ISO/IEC 27001 (ISMS) + ISO/IEC 27701 (Privacy)",
        nist_function="MANAGE (GenAI Profile risk themes)",
        core_question=(
            "Are access controls, PII handling, model/data isolation, and third-party "
            "processing posture defined and disclosed?"
        ),
    ),
    Dimension(
        key="talent_operating_model",
        name="Talent & Operating Model",
        iso_lineage="ISO/IEC 42001 Cl. 7 (Support — competence & awareness)",
        nist_function="GOVERN",
        core_question=(
            "Are skills present or sourced, roles defined (build / operate / govern), and "
            "run-state ownership assigned?"
        ),
    ),
    Dimension(
        key="third_party_concentration_risk",
        name="Third-Party & Concentration Risk",
        iso_lineage="ISO/IEC 42001 Annex A (Suppliers) + ISO/IEC 27036 (supplier sec.)",
        nist_function="GOVERN + MANAGE",
        core_question=(
            "Is model/vendor concentration understood, contractually controlled, and portable, "
            "with a bounded dependency blast radius?"
        ),
    ),
    Dimension(
        key="measurement_assurance",
        name="Measurement & Assurance",
        iso_lineage="ISO/IEC 42001 Cl. 9 (Performance eval) + ISO/IEC 42005 (impact)",
        nist_function="MEASURE",
        core_question=(
            "Can you evaluate outputs? Is there an eval harness? Do you measure failure "
            "severity, test real scenarios, and evaluate the evaluation itself?"
        ),
    ),
)

_DIMENSIONS_BY_KEY: dict[str, Dimension] = {d.key: d for d in DIMENSIONS}

# Highest-priority dimensions for remediation ordering: these fail first in the real world,
# so their gaps surface first regardless of raw severity.
REMEDIATION_FIRST: tuple[str, ...] = (
    "governance_decision_rights",
    "measurement_assurance",
)


def dimension(key: str) -> Dimension:
    """Return the locked dimension for a key, or raise if the key is unknown."""
    try:
        return _DIMENSIONS_BY_KEY[key]
    except KeyError as exc:  # pragma: no cover - guards against caller error
        raise KeyError(f"unknown dimension key: {key!r}") from exc


def all_bands() -> tuple[Band, ...]:
    """Return the five bands, low to high."""
    return tuple(Band)
