# Contributing

Thanks for your interest in improving the AI-Readiness Standard.

## Development setup

```bash
python -m pip install -e ".[dev]"
```

## Before opening a pull request

Run the full local quality bar — CI runs the same checks:

```bash
ruff check .                      # lint
mypy                              # types (strict)
lint-imports                      # Clean Architecture dependency contract
bash scripts/ip_grep.sh           # IP firewall
pytest                            # tests
python eval/SPEC-2026-0701/gate.py  # acceptance gate (AC-1..AC-15)
```

## Design rules

- **The domain core is pure.** Anything in `domain/` must not perform I/O or import an outer
  layer. Scoring is deterministic; keep it that way — the import contract enforces this.
- **Scoring is deterministic; narration never scores.** The optional LLM narration feature may
  summarize a finished report but must never influence a band.
- **The rubric is a locked contract.** Changing the seven dimensions, their standards lineage
  (ISO/IEC 42001 domains and NIST AI RMF functions), or the five bands is a deliberate versioned
  change, not a casual edit.
- **Answers, not artifacts.** This tool ingests questionnaire answers only. Do not add document
  upload or parsing.

## Commit style

Small, focused commits with clear messages. New behavior comes with tests.
