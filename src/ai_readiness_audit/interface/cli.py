"""Command-line interface: run the demo or assess a completed questionnaire.

    ai-readiness-audit demo
    ai-readiness-audit assess --answers answers.json --format html --out report.html

Answers files are JSON objects mapping question id to a band level (1..5).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from ..adapters.html_report import HtmlReportRenderer
from ..adapters.narration import build_narration_provider
from ..adapters.pdf_report import PdfReportRenderer
from ..application.assess import assess
from ..config import Settings
from ..domain.models import Band, ReadinessReport
from .sample_org import sample_answers


def _load_answers(path: Path) -> Mapping[str, Band]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {qid: Band(int(level)) for qid, level in raw.items()}


def _text_report(report: ReadinessReport) -> str:
    lines = [
        report.advisory_notice,
        "",
        f"Overall readiness: {report.overall_band.title} ({report.overall_band.name})",
        report.verdict,
        "",
        "By dimension:",
    ]
    lines += [
        f"  - {r.dimension.name}: {r.band.title} ({r.band.name})"
        for r in report.dimension_results
    ]
    lines += ["", "Prioritized remediation:"]
    lines += [
        f"  {i}. {g.dimension_name}: {g.prompt}"
        for i, g in enumerate(report.prioritized_remediation, start=1)
    ]
    lines += ["", report.routing_cta]
    return "\n".join(lines)


def _render(report: ReadinessReport, fmt: str) -> bytes:
    if fmt == "html":
        return HtmlReportRenderer().render(report).encode("utf-8")
    if fmt == "pdf":
        return PdfReportRenderer().render(report)
    return _text_report(report).encode("utf-8")


def _emit(payload: bytes, out: str | None) -> None:
    if out is None:
        sys.stdout.buffer.write(payload)
        if not payload.endswith(b"\n"):
            sys.stdout.buffer.write(b"\n")
    else:
        Path(out).write_bytes(payload)


def _run(answers: Mapping[str, Band], args: argparse.Namespace) -> int:
    report = assess(answers)
    _emit(_render(report, args.format), args.out)
    if getattr(args, "narrate", False):
        provider = build_narration_provider(Settings(narration_enabled=True))
        if provider is not None:
            sys.stderr.write("\n" + provider.narrate(report) + "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-readiness-audit", description=__doc__)
    parser.add_argument("--format", choices=["text", "html", "pdf"], default="text")
    parser.add_argument("--out", default=None, help="write to a file instead of stdout")
    parser.add_argument(
        "--narrate", action="store_true", help="append plain-language narration (never scores)"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo", help="run the full report on the bundled sample organization")
    assess_cmd = sub.add_parser("assess", help="assess a completed questionnaire")
    assess_cmd.add_argument("--answers", required=True, help="path to a JSON answers file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return _run(sample_answers(), args)
    return _run(_load_answers(Path(args.answers)), args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
