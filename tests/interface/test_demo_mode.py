"""AC-5: demo mode renders the full report on the bundled sample org with zero input."""

from __future__ import annotations

from html import escape

from ai_readiness_audit.domain.rubric import DIMENSIONS
from ai_readiness_audit.interface.cli import main


def test_demo_runs_with_no_input_and_covers_every_dimension(capsysbinary) -> None:
    exit_code = main(["--format", "html", "demo"])
    out = capsysbinary.readouterr().out.decode("utf-8")
    assert exit_code == 0
    for dim in DIMENSIONS:
        assert escape(dim.name) in out
    assert "Overall readiness" in out


def test_demo_pdf_is_a_valid_pdf(capsysbinary) -> None:
    exit_code = main(["--format", "pdf", "demo"])
    out = capsysbinary.readouterr().out
    assert exit_code == 0
    assert out.startswith(b"%PDF-1.4")
    assert b"%%EOF" in out
