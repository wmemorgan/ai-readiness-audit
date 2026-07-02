"""A deterministic narration provider — no key, no network, useful for demos and tests."""

from __future__ import annotations

from ...domain.models import ReadinessReport


class MockNarrationProvider:
    """Produces plain-language narration from a finished report, deterministically."""

    def narrate(self, report: ReadinessReport) -> str:
        lead = (
            f"Your organization scores at {report.overall_band.title} "
            f"({report.overall_band.name}) overall. {report.verdict}"
        )
        if not report.prioritized_remediation:
            return lead + " No high-leverage gaps were surfaced."
        top = report.prioritized_remediation[0]
        return (
            f"{lead} The highest-priority place to start is "
            f"{top.dimension_name}: {top.prompt}"
        )
