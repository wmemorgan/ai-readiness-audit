"""AC-3: the report renders all seven dimension bands plus the overall band."""

from __future__ import annotations

from html import escape

from ai_readiness_audit.adapters.html_report import HtmlReportRenderer
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.rubric import DIMENSIONS
from ai_readiness_audit.interface.sample_org import sample_answers


def test_html_contains_every_dimension_and_the_overall_band() -> None:
    report = assess(sample_answers())
    html = HtmlReportRenderer().render(report)
    for dim in DIMENSIONS:
        assert escape(dim.name) in html
    assert "Overall readiness" in html
    assert report.overall_band.title in html


def test_html_is_a_complete_document() -> None:
    html = HtmlReportRenderer().render(assess(sample_answers()))
    assert html.startswith("<!doctype html>")
    assert html.rstrip().endswith("</html>")
