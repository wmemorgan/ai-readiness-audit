"""HTML renderer for a ReadinessReport.

The rendered report leads with the authored AI-Readiness Standard and the advisory notice
(uncertainty-forward, above the fold). The public frameworks the standard rests on appear
only as citations in a footer — never as the headline.
"""

from __future__ import annotations

from html import escape

from ..domain.models import DimensionResult, ReadinessReport
from ..domain.rubric import CITED_FRAMEWORKS

STANDARD_HEADLINE = "The AI-Readiness Standard"
STANDARD_TAGLINE = "Seven dimensions. Five levels. One honest picture of where you stand."


class HtmlReportRenderer:
    """Implements the ReportRenderer port."""

    def render(self, report: ReadinessReport) -> str:
        parts: list[str] = [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{escape(STANDARD_HEADLINE)} — Readiness Report</title>",
            "</head>",
            "<body>",
            "<main>",
            self._headline(),
            self._advisory(report),
            self._overall(report),
            self._dimensions(report),
            self._remediation(report),
            self._cta(report),
            self._citations(),
            "</main>",
            "</body>",
            "</html>",
        ]
        return "\n".join(parts)

    def _headline(self) -> str:
        return (
            "<header>"
            f"<h1>{escape(STANDARD_HEADLINE)}</h1>"
            f"<p>{escape(STANDARD_TAGLINE)}</p>"
            "</header>"
        )

    def _advisory(self, report: ReadinessReport) -> str:
        # Rendered immediately after the headline so it is above the fold.
        notice = escape(report.advisory_notice)
        return f'<section class="advisory"><strong>{notice}</strong></section>'

    def _overall(self, report: ReadinessReport) -> str:
        band = report.overall_band
        return (
            '<section class="overall">'
            f"<h2>Overall readiness: {escape(band.title)} ({band.name})</h2>"
            f"<p>{escape(report.verdict)}</p>"
            "</section>"
        )

    def _dimensions(self, report: ReadinessReport) -> str:
        rows: list[str] = ['<section class="dimensions"><h2>By dimension</h2><ul>']
        for result in report.dimension_results:
            dim = result.dimension
            rows.append(
                "<li>"
                f"<h3>{escape(dim.name)} — {escape(result.band.title)} ({result.band.name})</h3>"
                f'<p class="ffiec">Examination lineage: {escape(dim.ffiec_domain)}</p>'
                + self._dimension_gaps(result)
                + "</li>"
            )
        rows.append("</ul></section>")
        return "".join(rows)

    def _dimension_gaps(self, result: DimensionResult) -> str:
        if not result.gaps:
            return "<p>No high-leverage gaps at this level.</p>"
        items = "".join(f"<li>{escape(gap.prompt)}</li>" for gap in result.gaps)
        return f"<p>Highest-leverage gaps:</p><ul>{items}</ul>"

    def _remediation(self, report: ReadinessReport) -> str:
        if not report.prioritized_remediation:
            return (
                '<section class="remediation"><h2>Prioritized remediation</h2>'
                "<p>None.</p></section>"
            )
        items = "".join(
            f"<li>{escape(gap.dimension_name)}: {escape(gap.prompt)}</li>"
            for gap in report.prioritized_remediation
        )
        return (
            '<section class="remediation">'
            "<h2>Prioritized remediation</h2>"
            f"<ol>{items}</ol>"
            "</section>"
        )

    def _cta(self, report: ReadinessReport) -> str:
        return f'<section class="cta"><p>{escape(report.routing_cta)}</p></section>'

    def _citations(self) -> str:
        items = "".join(f"<li>{escape(name)}</li>" for name in CITED_FRAMEWORKS)
        return (
            "<footer>"
            "<h2>Built on / Cites</h2>"
            "<p>The standard rests on these public frameworks:</p>"
            f"<ul>{items}</ul>"
            "</footer>"
        )
