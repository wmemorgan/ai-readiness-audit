"""The ratified rubric lock: seven dimensions, their examination-domain lineage, and the bands.

This is the single source of truth for scoring, questions, and report labels. The seven
dimensions and the five bands are a locked contract — the calibration and lock tests fail
on any drift. Each dimension traces to a public IT-examination domain, which is what makes
the diagnostic a defensible standard rather than a checklist.
"""

from __future__ import annotations

from .models import Band, Dimension

DIMENSIONS: tuple[Dimension, ...] = (
    Dimension(
        key="governance_decision_rights",
        name="Governance & Decision Rights",
        ffiec_domain="Management + Audit oversight",
        core_question=(
            "Is there an accountable executive, a written AI policy, and defined approval gates?"
        ),
    ),
    Dimension(
        key="risk_control_posture",
        name="Risk & Control Posture",
        ffiec_domain="Risk Management + Information Security",
        core_question=(
            "Are AI-specific risks — hallucination, data leakage, prompt injection, blast "
            "radius, drift — named and mapped to controls with human-in-loop gates by severity?"
        ),
    ),
    Dimension(
        key="data_readiness",
        name="Data Readiness",
        ffiec_domain="Operations",
        core_question=(
            "Is data accessible, governed, quality-assured, lineage-traceable, and "
            "rights/licensing-cleared for AI use?"
        ),
    ),
    Dimension(
        key="security_privacy",
        name="Security & Privacy",
        ffiec_domain="Information Security",
        core_question=(
            "Are access controls, PII handling, model/data isolation, and third-party "
            "processing posture defined and disclosed?"
        ),
    ),
    Dimension(
        key="talent_operating_model",
        name="Talent & Operating Model",
        ffiec_domain="Development & Acquisition + Management",
        core_question=(
            "Are skills present or sourced, roles defined (build / operate / govern), and "
            "run-state ownership assigned?"
        ),
    ),
    Dimension(
        key="third_party_concentration_risk",
        name="Third-Party & Concentration Risk",
        ffiec_domain="Outsourcing",
        core_question=(
            "Is model/vendor concentration understood, contractually controlled, and portable, "
            "with a bounded dependency blast radius?"
        ),
    ),
    Dimension(
        key="measurement_assurance",
        name="Measurement & Assurance",
        ffiec_domain="Audit",
        core_question=(
            "Can you evaluate outputs? Is there an eval harness? Do you measure failure "
            "severity, test real scenarios, and evaluate the evaluation itself?"
        ),
    ),
)

# The public frameworks the standard rests on. These are citations, never the headline.
CITED_FRAMEWORKS: tuple[str, ...] = (
    "FFIEC IT Examination Handbook — Work Program",
    "NIST AI Risk Management Framework (AI RMF 1.0)",
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
