"""AC-12: the report ends with a routing CTA framed as closing the surfaced gaps."""

from __future__ import annotations

from ai_readiness_audit.adapters.html_report import HtmlReportRenderer
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.interface.sample_org import sample_answers


def test_cta_is_present_and_gap_framed() -> None:
    report = assess(sample_answers())
    assert "close the gaps" in report.routing_cta.lower()


def test_cta_never_claims_certification() -> None:
    report = assess(sample_answers())
    html = HtmlReportRenderer().render(report).lower()
    assert "certified" not in html
