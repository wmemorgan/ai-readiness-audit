"""AC-14: the engine ingests answers, not artifacts — no upload / document-parse path exists."""

from __future__ import annotations

from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "ai_readiness_audit"

# Libraries or verbs that would indicate document ingestion rather than a questionnaire.
FORBIDDEN_TOKENS = (
    "def upload",
    "multipart",
    "werkzeug",
    "pypdf",
    "pdfminer",
    "python-docx",
    "import docx",
    "extract_text",
)


def test_no_document_ingestion_tokens_in_source() -> None:
    for module_path in SRC.rglob("*.py"):
        text = module_path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_TOKENS:
            assert token not in text, f"{module_path.name} contains upload/parse token {token!r}"


def test_answers_are_the_only_input_surface() -> None:
    # The assessment use-case accepts a mapping of answers; there is no file parameter.
    import inspect

    from ai_readiness_audit.application.assess import assess

    params = inspect.signature(assess).parameters
    assert "answers" in params
    assert not any("file" in name or "path" in name or "upload" in name for name in params)
