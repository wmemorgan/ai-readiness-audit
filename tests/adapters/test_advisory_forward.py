"""AC-8: the advisory notice is uncertainty-forward — above the fold, not buried."""

from __future__ import annotations

from ai_readiness_audit.adapters.html_report import HtmlReportRenderer
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.interface.sample_org import sample_answers


def test_advisory_notice_renders_before_the_dimensions_and_cta() -> None:
    report = assess(sample_answers())
    html = HtmlReportRenderer().render(report)
    advisory_at = html.find("advisory readiness diagnostic, not a certification")
    dimensions_at = html.find("By dimension")
    cta_at = html.find(report.routing_cta)
    assert advisory_at != -1
    assert advisory_at < dimensions_at < cta_at


def test_report_states_it_is_not_a_guarantee() -> None:
    report = assess(sample_answers())
    assert "not a certification" in report.advisory_notice
    assert "not a guarantee" in report.advisory_notice
