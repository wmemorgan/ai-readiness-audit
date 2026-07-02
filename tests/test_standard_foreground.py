"""AC-7: the authored Standard is the headline; ISO/NIST inform it; FFIEC is cited only."""

from __future__ import annotations

from pathlib import Path

from ai_readiness_audit.adapters.html_report import HtmlReportRenderer
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.copy import STANDARD_HEADLINE
from ai_readiness_audit.interface.sample_org import sample_answers

ROOT = Path(__file__).resolve().parents[1]
CITE_MARKERS = ("Built on", "Cites")


def _first_index(text: str, needle: str) -> int:
    idx = text.find(needle)
    return idx if idx >= 0 else 10**9


def test_readme_headlines_the_standard_and_confines_ffiec_to_citations() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "AI-Readiness Standard" in readme
    # ISO/IEC and NIST may appear anywhere (product language + lineage).
    assert "ISO/IEC 42001" in readme
    assert "NIST AI RMF" in readme
    # FFIEC may appear only from the Standards Lineage / Built on / Cites onward.
    lineage_at = min(
        _first_index(readme, "Standards Lineage"),
        _first_index(readme, "Built on"),
    )
    assert _first_index(readme, "FFIEC") >= lineage_at


def test_html_leads_with_the_standard_and_cites_ffiec_only_in_the_footer() -> None:
    html = HtmlReportRenderer().render(assess(sample_answers()))
    cite_at = min(_first_index(html, marker) for marker in CITE_MARKERS)
    assert _first_index(html, STANDARD_HEADLINE) < cite_at
    # FFIEC appears only in the footer citations.
    assert _first_index(html, "FFIEC") > cite_at
