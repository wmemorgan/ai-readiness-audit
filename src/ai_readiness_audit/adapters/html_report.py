"""HTML renderer for a ReadinessReport.

The rendered report leads with the authored AI-Readiness Standard and the advisory notice
(uncertainty-forward, above the fold). Each dimension shows its ISO/IEC lineage and NIST AI RMF
function. The public standards the standard rests on appear only as citations in a footer.
"""

from __future__ import annotations

from html import escape

from ..domain.copy import STANDARD_HEADLINE, STANDARD_SUBTITLE, lineage_line
from ..domain.models import DimensionResult, ReadinessReport

# Built on / Cites — the public standards the AI-Readiness Standard rests on. This footer is the
# only place a report reproduces the citation list; FFIEC appears here as method inspiration only.
CITATIONS: tuple[str, ...] = (
    "ISO/IEC 42001:2023 — AI management systems (iso.org/standard/42001)",
    "ISO/IEC 23894, 38507, 42005, 27001, 27701, 5259 series, 27036",
    "NIST AI RMF 1.0 (AI 100-1) + Generative AI Profile (AI 600-1)",
    "FFIEC IT Examination Handbook Work Program — method inspiration "
    "(tiered objectives → procedures → evidence, by domain)",
)


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
            f"<p>{escape(STANDARD_SUBTITLE)}</p>"
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
                f'<p class="lineage">{escape(lineage_line(dim, result.score))}</p>'
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
        items = "".join(f"<li>{escape(name)}</li>" for name in CITATIONS)
        return (
            "<footer>"
            "<h2>Built on / Cites</h2>"
            "<p>The standard rests on these public standards and frameworks:</p>"
            f"<ul>{items}</ul>"
            "</footer>"
        )
