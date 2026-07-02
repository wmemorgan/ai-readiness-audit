"""AC-7: the authored Standard is the headline; public frameworks appear only as citations."""

from __future__ import annotations

from pathlib import Path

from ai_readiness_audit.adapters.html_report import STANDARD_HEADLINE, HtmlReportRenderer
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.interface.sample_org import sample_answers

ROOT = Path(__file__).resolve().parents[1]
CANON = ("FFIEC", "NIST")
CITE_MARKERS = ("Built on", "Cites")


def _first_index(text: str, needle: str) -> int:
    idx = text.find(needle)
    return idx if idx >= 0 else 10**9


def test_readme_headlines_the_standard_before_any_canon() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "AI-Readiness Standard" in readme
    cite_at = min(_first_index(readme, marker) for marker in CITE_MARKERS)
    for name in CANON:
        assert _first_index(readme, name) > cite_at, f"{name} must appear only as a citation"


def test_html_leads_with_the_standard_not_the_frameworks() -> None:
    html = HtmlReportRenderer().render(assess(sample_answers()))
    cite_at = min(_first_index(html, marker) for marker in CITE_MARKERS)
    assert _first_index(html, STANDARD_HEADLINE) < cite_at
    for name in CANON:
        assert _first_index(html, name) > cite_at
