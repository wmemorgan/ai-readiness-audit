"""Generate the language-neutral engine contract + parity fixtures FROM the engine.

Every string (dimension names, ISO/NIST lineage, question prompts, level anchors, bands,
shared copy) is pulled directly from the engine's own data — never paraphrased. The parity
fixtures are produced by running the engine, so a re-implementation can verify exact parity.

Usage:  python scripts/generate_contract.py contract/
The committed contract is verified against the live engine by tests/test_contract_parity.py.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ai_readiness_audit import __version__ as ENGINE_VERSION
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain import copy as engine_copy
from ai_readiness_audit.domain.banding import BAND_CUT_LINES
from ai_readiness_audit.domain.models import Band
from ai_readiness_audit.domain.questions import QUESTIONS, questions_for
from ai_readiness_audit.domain.remediation import GAP_THRESHOLD, MAX_GAPS_PER_DIMENSION
from ai_readiness_audit.domain.rubric import DIMENSIONS, REMEDIATION_FIRST
from ai_readiness_audit.domain.scoring import DEFAULT_CONTRACT

DIMENSION_ORDER = [d.key for d in DIMENSIONS]


def _engine_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:  # pragma: no cover - git may be unavailable
        return "unknown"


def _uniform(level: int) -> dict[str, Band]:
    return {q.id: Band(level) for q in QUESTIONS}


def _shared_copy() -> dict:
    # Read report-shared strings off a real report so they can never drift from the engine.
    sample = assess(_uniform(3))
    verdicts = {str(int(b)): assess(_uniform(int(b))).verdict for b in Band}
    return {
        "headline": engine_copy.STANDARD_HEADLINE,
        "subtitle": engine_copy.STANDARD_SUBTITLE,
        "tagline": engine_copy.TAGLINE,
        "descriptor": engine_copy.STANDARD_DESCRIPTOR,
        "thesis": engine_copy.THESIS,
        "advisory_disclaimer": sample.advisory_notice,
        "routing_cta": sample.routing_cta,
        "verdicts_by_overall_level": verdicts,
    }


def build_contract(commit: str, generated_at: str) -> dict:
    dimensions = [
        {
            "id": d.key,
            "name": d.name,
            "iso_lineage": d.iso_lineage,
            "nist_function": d.nist_function,
            "core_question": d.core_question,
            "weight": DEFAULT_CONTRACT.weight_for(d.key),
            "questions": [
                {
                    "id": q.id,
                    "prompt": q.prompt,
                    "level_anchors": {str(int(o.band)): o.label for o in q.options},
                }
                for q in questions_for(d.key)
            ],
        }
        for d in DIMENSIONS
    ]

    scoring = {
        "question_weight": DEFAULT_CONTRACT.question_weight,
        "dimension_weights": {d.key: DEFAULT_CONTRACT.weight_for(d.key) for d in DIMENSIONS},
        "dimension_score_rule": (
            "Arithmetic mean of the answered question levels within the dimension "
            "(each weighted by question_weight; uniform)."
        ),
        "overall_score_rule": (
            "Weighted mean of the seven dimension scores (each weighted by its dimension weight; "
            "uniform)."
        ),
        "band_cut_lines": [{"min_score": lo, "level": int(b)} for lo, b in BAND_CUT_LINES],
        "band_rule": "Assign the highest level whose min_score <= score. Scores range 1.0..5.0.",
        "gap_rule": {
            "is_gap_when_level_at_or_below": int(GAP_THRESHOLD),
            "severity": "5 - level",
            "max_gaps_per_dimension": MAX_GAPS_PER_DIMENSION,
            "per_dimension_sort": "severity desc, then question_id asc; take the top N per dimension",
            "priority_dimensions_first": list(REMEDIATION_FIRST),
            "overall_sort": (
                "priority_rank asc (priority dimensions = 0, others = 1), then severity desc, "
                "then dimension_order asc, then question_id asc"
            ),
            "dimension_order": DIMENSION_ORDER,
        },
    }

    return {
        "version": "1.0",
        "engine_version": ENGINE_VERSION,
        "engine_commit": commit,
        "generated_at": generated_at,
        "generated_from": "the ai-readiness-audit Python engine (exact strings; do not paraphrase)",
        "levels": [
            {"level": int(b), "code": b.name, "name": b.title, "summary": b.summary} for b in Band
        ],
        "dimensions": dimensions,
        "scoring": scoring,
        "copy": _shared_copy(),
    }


def _expected(answers: Mapping[str, Band]) -> dict:
    report = assess(answers)
    return {
        "per_dimension_levels": {r.dimension.key: int(r.band) for r in report.dimension_results},
        "overall_level": int(report.overall_band),
        "ordered_gaps": [g.question_id for g in report.prioritized_remediation],
    }


def build_fixtures(commit: str, generated_at: str) -> dict:
    cases: list[tuple[str, dict[str, Band]]] = []
    for lvl in range(1, 6):
        cases.append((f"uniform-L{lvl}", _uniform(lvl)))
    for d in DIMENSIONS:
        cases.append(
            (
                f"only-{d.key}-strong",
                {q.id: Band(5) if q.dimension_key == d.key else Band(1) for q in QUESTIONS},
            )
        )
    for offset in range(3):
        cases.append(
            (f"gradient-{offset}", {q.id: Band(((i + offset) % 5) + 1) for i, q in enumerate(QUESTIONS)})
        )

    return {
        "version": "1.0",
        "engine_commit": commit,
        "generated_at": generated_at,
        "generated_from": "assess() over the engine — expected values are engine output, not hand-authored",
        "note": "A conformant scorer MUST reproduce per_dimension_levels, overall_level, and ordered_gaps exactly.",
        "cases": [
            {
                "name": name,
                "answers": {qid: int(b) for qid, b in answers.items()},
                "expected": _expected(answers),
            }
            for name, answers in cases
        ],
    }


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "contract")
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = _engine_commit()
    generated_at = date.today().isoformat()
    _write(out_dir / "readiness-contract.json", build_contract(commit, generated_at))
    _write(out_dir / "parity-fixtures.json", build_fixtures(commit, generated_at))
    print(f"wrote contract + fixtures to {out_dir}/ (engine {commit})")


if __name__ == "__main__":
    main()
