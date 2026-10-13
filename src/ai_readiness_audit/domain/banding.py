"""Band assignment from a numeric score via explicit, locked cut-lines.

The cut-lines are fixed at the half-integer boundaries. They are part of the locked
scoring contract: an identical score always maps to an identical band.
"""

from __future__ import annotations

from .models import Band

# Lower bound (inclusive) of each band on the 1.0..5.0 score scale.
BAND_CUT_LINES: tuple[tuple[float, Band], ...] = (
    (4.5, Band.L5),
    (3.5, Band.L4),
    (2.5, Band.L3),
    (1.5, Band.L2),
    (1.0, Band.L1),
)


def band_from_score(score: float) -> Band:
    """Map a 1.0..5.0 score to its band using the locked cut-lines."""
    for lower_bound, band in BAND_CUT_LINES:
        if score >= lower_bound:
            return band
    return Band.L1
