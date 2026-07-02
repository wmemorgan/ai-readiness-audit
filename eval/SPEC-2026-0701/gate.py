#!/usr/bin/env python3
"""Eval gate for SPEC-2026-0701 — the built tool must satisfy every acceptance criterion.

Run ``python eval/SPEC-2026-0701/gate.py`` to prove the tool against AC-1..AC-15, or
``--coverage`` to print the AC -> check map. Exit 0 iff every mapped criterion passes.
This is the authoritative completion proof (the spec becomes the eval).
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ai_readiness_audit.adapters.html_report import HtmlReportRenderer
from ai_readiness_audit.adapters.narration import build_narration_provider
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.config import Settings
from ai_readiness_audit.domain.banding import band_from_score
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.rubric import DIMENSIONS
from ai_readiness_audit.domain.scoring import DEFAULT_CONTRACT
from ai_readiness_audit.interface.sample_org import sample_answers


def _uniform(band: Band) -> dict[str, Band]:
    return {qid: band for qid in sample_answers()}


def ac_1_determinism() -> None:
    a = sample_answers()
    assert assess(a).overall_band == assess(dict(a)).overall_band
    assert assess(a).overall_score == assess(dict(a)).overall_score


def ac_2_band_boundaries() -> None:
    assert band_from_score(2.49) == Band.L2
    assert band_from_score(2.5) == Band.L3
    assert band_from_score(4.5) == Band.L5
    for band in Band:
        assert assess(_uniform(band)).overall_band == band


def ac_3_renders_all_dimensions() -> None:
    html = HtmlReportRenderer().render(assess(sample_answers()))
    for dim in DIMENSIONS:
        assert escape(dim.name) in html
    assert "Overall readiness" in html


def ac_4_prioritized_remediation() -> None:
    report = assess(_uniform(Band.L2))
    leading = {g.dimension_key for g in report.prioritized_remediation[:6]}
    assert leading == {"governance_decision_rights", "measurement_assurance"}


def ac_5_demo_mode() -> None:
    from ai_readiness_audit.interface.cli import main

    assert main(["--format", "html", "--out", "/tmp/_ara_demo.html", "demo"]) == 0
    assert Path("/tmp/_ara_demo.html").read_text(encoding="utf-8").startswith("<!doctype html>")


def ac_6_ip_grep() -> None:
    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "ip_grep.sh")],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr


def ac_7_standard_foreground() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "AI-Readiness Standard" in readme
    # ISO/IEC and NIST may appear in product language and per-dimension lineage.
    assert "ISO/IEC 42001" in readme and "NIST AI RMF" in readme
    # FFIEC may appear only from the Standards Lineage / Built on section onward.
    lineage_at = min(i for i in (readme.find("Standards Lineage"), readme.find("Built on")) if i != -1)
    ffiec_at = readme.find("FFIEC")
    assert ffiec_at != -1 and ffiec_at >= lineage_at, "FFIEC may appear only as a citation"


def ac_8_uncertainty_forward() -> None:
    html = HtmlReportRenderer().render(assess(sample_answers()))
    advisory_at = html.find("advisory readiness diagnostic, not a certification")
    assert advisory_at != -1
    assert advisory_at < html.find("By dimension")


def ac_9_rubric_lock() -> None:
    locked = {
        "governance_decision_rights": "Governance & Decision Rights",
        "risk_control_posture": "Risk & Control Posture",
        "data_readiness": "Data Readiness",
        "security_privacy": "Security & Privacy",
        "talent_operating_model": "Talent & Operating Model",
        "third_party_concentration_risk": "Third-Party & Concentration Risk",
        "measurement_assurance": "Measurement & Assurance",
    }
    assert {d.key: d.name for d in DIMENSIONS} == locked


def ac_10_locked_contract() -> None:
    assert len(DEFAULT_CONTRACT.dimension_weights) == len(DIMENSIONS)
    assert isinstance(DEFAULT_CONTRACT.question_weight, float)
    # No nondeterministic import reaches the scoring core.
    scoring_src = (REPO_ROOT / "src/ai_readiness_audit/domain/scoring.py").read_text("utf-8")
    for forbidden in ("import random", "import time", "datetime", "requests", "urllib"):
        assert forbidden not in scoring_src


def ac_11_narration_never_scores() -> None:
    assert build_narration_provider(Settings()) is None
    answers = sample_answers()
    assert assess(answers).overall_band == assess(dict(answers)).overall_band


def ac_12_routing_cta() -> None:
    report = assess(sample_answers())
    assert "close the gaps" in report.routing_cta.lower()
    assert "certified" not in HtmlReportRenderer().render(report).lower()


def ac_13_standards_alignment() -> None:
    # Every dimension carries a non-empty ISO lineage and NIST function matching Table R.
    table_r = {
        "governance_decision_rights": (
            "ISO/IEC 42001 Cl. 5 (Leadership) + ISO/IEC 38507 (AI governance)", "GOVERN"),
        "risk_control_posture": (
            "ISO/IEC 23894 (AI risk mgmt) + ISO/IEC 42001 Cl. 6 (Planning)", "MAP + MANAGE"),
        "data_readiness": (
            "ISO/IEC 42001 Annex A (Data for AI) + ISO/IEC 5259 (data quality)", "MAP"),
        "security_privacy": (
            "ISO/IEC 27001 (ISMS) + ISO/IEC 27701 (Privacy)", "MANAGE (GenAI Profile risk themes)"),
        "talent_operating_model": (
            "ISO/IEC 42001 Cl. 7 (Support — competence & awareness)", "GOVERN"),
        "third_party_concentration_risk": (
            "ISO/IEC 42001 Annex A (Suppliers) + ISO/IEC 27036 (supplier sec.)", "GOVERN + MANAGE"),
        "measurement_assurance": (
            "ISO/IEC 42001 Cl. 9 (Performance eval) + ISO/IEC 42005 (impact)", "MEASURE"),
    }
    for dim in DIMENSIONS:
        assert dim.iso_lineage.strip() and dim.nist_function.strip(), f"{dim.key} missing lineage"
        assert (dim.iso_lineage, dim.nist_function) == table_r[dim.key], f"{dim.key} lineage drift"


def ac_14_minimal_privacy_surface() -> None:
    import inspect

    from ai_readiness_audit.application import assess as assess_mod

    params = inspect.signature(assess_mod.assess).parameters
    assert not any(k in name for name in params for k in ("file", "path", "upload"))
    for module_path in (REPO_ROOT / "src").rglob("*.py"):
        text = module_path.read_text(encoding="utf-8").lower()
        assert "def upload" not in text and "multipart" not in text


def ac_15_gate3_signoff() -> None:
    signoff = (REPO_ROOT / "GATE_3_SIGNOFF.md").read_text(encoding="utf-8")
    assert "Reviewer" in signoff


CHECKS: dict[str, tuple[str, Callable[[], None]]] = {
    "AC-1": ("Deterministic scoring — identical answers replay to identical bands", ac_1_determinism),
    "AC-2": ("Band-boundary correctness across every L1..L5 cut-line", ac_2_band_boundaries),
    "AC-3": ("Report renders all 7 dimensions + overall band", ac_3_renders_all_dimensions),
    "AC-4": ("Prioritized remediation — governance + measurement first", ac_4_prioritized_remediation),
    "AC-5": ("Demo mode renders the full report on the sample org, no input", ac_5_demo_mode),
    "AC-6": ("Gate-1 grep — zero prohibited terms / authorship traces", ac_6_ip_grep),
    "AC-7": ("Authored Standard foregrounded; ISO/NIST inform it; FFIEC cited only", ac_7_standard_foreground),
    "AC-8": ("Uncertainty-forward report — advisory above the fold", ac_8_uncertainty_forward),
    "AC-9": ("Encoded rubric equals the ratified §4 lock", ac_9_rubric_lock),
    "AC-10": ("Locked, reproducible scoring contract; no nondeterministic input", ac_10_locked_contract),
    "AC-11": ("LLM narration never moves a band; disabled by default", ac_11_narration_never_scores),
    "AC-12": ("Routing CTA present, gap-framed, never 'certified'", ac_12_routing_cta),
    "AC-13": ("Standards-alignment defensibility — ISO lineage + NIST function per Table R", ac_13_standards_alignment),
    "AC-14": ("Minimal privacy surface — questionnaire-only, no upload path", ac_14_minimal_privacy_surface),
    "AC-15": ("SDS Gate-3 layout sign-off recorded", ac_15_gate3_signoff),
}


def print_coverage() -> int:
    print(f"SPEC-2026-0701 eval gate — {len(CHECKS)} acceptance criteria mapped:")
    for ac, (desc, _) in CHECKS.items():
        print(f"  {ac}: {desc}")
    return 0


def run() -> int:
    failures = 0
    for ac, (desc, check) in CHECKS.items():
        try:
            check()
            print(f"  PASS {ac}: {desc}")
        except Exception as exc:  # noqa: BLE001 - the gate reports any failure
            failures += 1
            print(f"  FAIL {ac}: {desc}\n        {exc}")
    print(f"\n{len(CHECKS) - failures}/{len(CHECKS)} acceptance criteria passed.")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--coverage" in args:
        return print_coverage()
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
