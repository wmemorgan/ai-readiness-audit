"""A bundled sample organization, so demo mode runs with zero input.

The answers describe a mid-early organization with clear governance and measurement gaps —
enough to exercise every dimension and show how remediation is prioritized.
"""

from __future__ import annotations

from collections.abc import Mapping

from ..domain.models import Band

_SAMPLE: dict[str, Band] = {
    # Governance & Decision Rights — weak
    "gov-1": Band.L2,
    "gov-2": Band.L1,
    "gov-3": Band.L2,
    # Risk & Control Posture — emerging
    "risk-1": Band.L3,
    "risk-2": Band.L2,
    "risk-3": Band.L2,
    # Data Readiness — defined
    "data-1": Band.L4,
    "data-2": Band.L3,
    "data-3": Band.L3,
    # Security & Privacy — defined
    "sec-1": Band.L4,
    "sec-2": Band.L3,
    "sec-3": Band.L3,
    # Talent & Operating Model — defined
    "talent-1": Band.L3,
    "talent-2": Band.L3,
    "talent-3": Band.L2,
    # Third-Party & Concentration Risk — weak
    "tp-1": Band.L2,
    "tp-2": Band.L2,
    "tp-3": Band.L1,
    # Measurement & Assurance — weakest
    "meas-1": Band.L2,
    "meas-2": Band.L1,
    "meas-3": Band.L1,
}


def sample_answers() -> Mapping[str, Band]:
    """Return the bundled sample organization's answers."""
    return dict(_SAMPLE)
