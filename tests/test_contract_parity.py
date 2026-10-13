"""The published contract is a faithful, non-drifting mirror of the engine.

This test is the drift guard: if the rubric, questions, cut-lines, gap logic, or shared copy
change without the contract being regenerated, CI fails. It also proves the parity fixtures are
real engine output — a conformant re-implementation can trust them.
"""

from __future__ import annotations

import json
from pathlib import Path

from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.banding import BAND_CUT_LINES
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.questions import questions_for
from ai_readiness_audit.domain.remediation import REMEDIATION_FIRST
from ai_readiness_audit.domain.rubric import DIMENSIONS

CONTRACT_DIR = Path(__file__).resolve().parents[1] / "contract"
CONTRACT = json.loads((CONTRACT_DIR / "readiness-contract.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((CONTRACT_DIR / "parity-fixtures.json").read_text(encoding="utf-8"))


def test_contract_dimensions_match_the_engine_verbatim() -> None:
    by_id = {d["id"]: d for d in CONTRACT["dimensions"]}
    assert list(by_id) == [d.key for d in DIMENSIONS]
    for dim in DIMENSIONS:
        entry = by_id[dim.key]
        assert entry["name"] == dim.name
        assert entry["iso_lineage"] == dim.iso_lineage
        assert entry["nist_function"] == dim.nist_function
        assert entry["core_question"] == dim.core_question


def test_contract_questions_and_anchors_match_the_engine_verbatim() -> None:
    by_id = {d["id"]: d for d in CONTRACT["dimensions"]}
    for dim in DIMENSIONS:
        engine_questions = questions_for(dim.key)
        contract_questions = by_id[dim.key]["questions"]
        assert [q["id"] for q in contract_questions] == [q.id for q in engine_questions]
        for cq, eq in zip(contract_questions, engine_questions, strict=True):
            assert cq["prompt"] == eq.prompt
            for option in eq.options:
                assert cq["level_anchors"][str(int(option.band))] == option.label


def test_contract_scoring_matches_the_engine() -> None:
    scoring = CONTRACT["scoring"]
    assert scoring["band_cut_lines"] == [
        {"min_score": lo, "level": int(b)} for lo, b in BAND_CUT_LINES
    ]
    assert scoring["gap_rule"]["priority_dimensions_first"] == list(REMEDIATION_FIRST)
    assert scoring["gap_rule"]["dimension_order"] == [d.key for d in DIMENSIONS]


def test_parity_fixtures_reproduce_engine_output_exactly() -> None:
    assert len(FIXTURES["cases"]) >= 12
    for case in FIXTURES["cases"]:
        answers = {qid: Band(level) for qid, level in case["answers"].items()}
        report = assess(answers)
        expected = case["expected"]
        got_dims = {r.dimension.key: int(r.band) for r in report.dimension_results}
        got_gaps = [g.question_id for g in report.prioritized_remediation]
        assert got_dims == expected["per_dimension_levels"], case["name"]
        assert int(report.overall_band) == expected["overall_level"], case["name"]
        assert got_gaps == expected["ordered_gaps"], case["name"]


def test_fixtures_span_the_full_band_range() -> None:
    overall = {c["expected"]["overall_level"] for c in FIXTURES["cases"]}
    assert overall == {1, 2, 3, 4, 5}
