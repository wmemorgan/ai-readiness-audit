"""The CLI reports an unusable answers file as one line on stderr with exit code 2.

A user who writes their own answers file must get a clear message, never a traceback. The
bundled example answers file must stay complete and valid.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_readiness_audit.domain.questions import QUESTIONS
from ai_readiness_audit.interface.cli import main

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "answers.json"


def _complete(level: object = 3) -> dict[str, object]:
    return {q.id: level for q in QUESTIONS}


def _run_with(tmp_path: Path, content: str) -> int:
    path = tmp_path / "answers.json"
    path.write_text(content, encoding="utf-8")
    return main(["assess", "--answers", str(path)])


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (json.dumps({**_complete(), "gov-1": 9}), "invalid level for 'gov-1': 9"),
        (json.dumps({**_complete(), "gov-1": 2.5}), "invalid level for 'gov-1': 2.5"),
        (json.dumps({**_complete(), "gov-1": True}), "invalid level for 'gov-1': True"),
        (json.dumps({**_complete(), "gov1": 3}), "unknown question id(s): gov1"),
        (json.dumps({"gov-1": 3}), "incomplete answers file: missing answers for"),
        ("{not json", "answers file is not valid JSON"),
        ("[1, 2, 3]", "must be a JSON object"),
    ],
)
def test_bad_answers_file_is_one_clear_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], content: str, message: str
) -> None:
    assert _run_with(tmp_path, content) == 2
    err = capsys.readouterr().err
    assert err.startswith("error: ") and message in err
    assert "Traceback" not in err and err.count("\n") == 1


def test_missing_answers_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["assess", "--answers", str(tmp_path / "absent.json")]) == 2
    assert "answers file not found" in capsys.readouterr().err


def test_unwritable_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--out", str(tmp_path / "no" / "such" / "dir.html"), "demo"]) == 2
    assert "cannot write" in capsys.readouterr().err


def test_levels_as_strings_are_accepted(tmp_path: Path, capsysbinary) -> None:
    assert _run_with(tmp_path, json.dumps(_complete("3"))) == 0


def test_output_options_work_before_or_after_the_command(tmp_path: Path) -> None:
    before, after = tmp_path / "before.html", tmp_path / "after.html"
    assert main(["--format", "html", "--out", str(before), "demo"]) == 0
    assert main(["demo", "--format", "html", "--out", str(after)]) == 0
    assert before.read_bytes() == after.read_bytes()
    assert before.read_text(encoding="utf-8").startswith("<!doctype html>")


def test_example_answers_file_is_complete_and_valid(capsysbinary) -> None:
    answers = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    assert list(answers) == [q.id for q in QUESTIONS]
    assert main(["assess", "--answers", str(EXAMPLE)]) == 0
