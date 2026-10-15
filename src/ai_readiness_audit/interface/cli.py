"""Command-line interface: run the demo or assess a completed questionnaire.

    ai-readiness-audit demo
    ai-readiness-audit assess --answers answers.json --format html --out report.html

Answers files are JSON objects mapping every question id to a level from 1 to 5 (see
``examples/answers.json``). An unusable answers file is reported on stderr with exit code 2.
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
from ..application.assess import IncompleteAssessment, assess
from ..config import Settings
from ..domain.copy import TAGLINE, lineage_line
from ..domain.models import Band, ReadinessReport
from ..domain.questions import QUESTIONS
from .sample_org import sample_answers

_LEVELS = {str(int(b)) for b in Band}


class CliError(ValueError):
    """An input or output file cannot be used (reported as one line, exit code 2)."""


def _parse_level(qid: str, level: object) -> Band:
    # Accept 3 or "3"; reject booleans, floats, and anything outside 1..5.
    if isinstance(level, bool) or not isinstance(level, (int, str)) or str(level) not in _LEVELS:
        raise CliError(f"invalid level for {qid!r}: {level!r} (expected an integer 1..5)")
    return Band(int(level))


def _load_answers(path: Path) -> Mapping[str, Band]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CliError(f"answers file not found: {path}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise CliError(f"cannot read answers file {path}: {exc}") from None
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CliError(
            f"answers file is not valid JSON: {path} (line {exc.lineno}, column {exc.colno})"
        ) from None
    if not isinstance(raw, dict):
        raise CliError("answers file must be a JSON object mapping question id to a level 1..5")
    unknown = sorted(set(raw) - {q.id for q in QUESTIONS})
    if unknown:
        raise CliError(f"unknown question id(s): {', '.join(unknown)}")
    return {qid: _parse_level(qid, level) for qid, level in raw.items()}


def _text_report(report: ReadinessReport) -> str:
    lines = [
        report.advisory_notice,
        "",
        f"Overall readiness: {report.overall_band.title} ({report.overall_band.name})",
        report.verdict,
        "",
        "By dimension:",
    ]
    for r in report.dimension_results:
        lines.append(f"  - {r.dimension.name}: {r.band.title} ({r.band.name})")
        lines.append(f"    {lineage_line(r.dimension, r.score)}")
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
        try:
            Path(out).write_bytes(payload)
        except OSError as exc:
            raise CliError(f"cannot write {out}: {exc.strerror}") from None


def _run(answers: Mapping[str, Band], args: argparse.Namespace) -> int:
    report = assess(answers)
    _emit(_render(report, args.format), args.out)
    if getattr(args, "narrate", False):
        provider = build_narration_provider(Settings(narration_enabled=True))
        if provider is not None:
            sys.stderr.write("\n" + provider.narrate(report) + "\n")
    return 0


def _add_output_options(parser: argparse.ArgumentParser, *, suppress: bool) -> None:
    # The output options are accepted before or after the command. On the sub-commands the
    # defaults are suppressed so a value given before the command is not overwritten.
    def default(value: object) -> object:
        return argparse.SUPPRESS if suppress else value

    parser.add_argument("--format", choices=["text", "html", "pdf"], default=default("text"))
    parser.add_argument("--out", default=default(None), help="write to a file instead of stdout")
    parser.add_argument(
        "--narrate",
        action="store_true",
        default=default(False),
        help="append a plain-language summary to stderr (built-in, no key; never scores)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-readiness-audit", description=TAGLINE)
    _add_output_options(parser, suppress=False)
    sub = parser.add_subparsers(dest="command", required=True)
    demo_cmd = sub.add_parser("demo", help="run the full report on the bundled sample organization")
    _add_output_options(demo_cmd, suppress=True)
    assess_cmd = sub.add_parser("assess", help="assess a completed questionnaire")
    assess_cmd.add_argument("--answers", required=True, help="path to a JSON answers file")
    _add_output_options(assess_cmd, suppress=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "demo":
            return _run(sample_answers(), args)
        return _run(_load_answers(Path(args.answers)), args)
    except CliError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    except IncompleteAssessment as exc:
        sys.stderr.write(f"error: incomplete answers file: {exc}\n")
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
