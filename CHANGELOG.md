# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-10-15

### Fixed

- The Quickstart installs from the repository (`pip install -e .` in a clone, or
  `pip install "git+https://github.com/wmemorgan/ai-readiness-audit.git@v0.1.1"`). The package is
  not published on PyPI, so the previous `pip install ai-readiness-audit` did not work.
- A bare `pytest` now runs the full suite from a fresh clone (the tests' shared helpers were not
  importable without `python -m`).
- The CLI reports an unusable answers file (not found, not valid JSON, not an object, an unknown
  question id, a level outside 1..5, or missing answers) and an unwritable `--out` path as one
  error line with exit code 2, instead of a traceback.
- `--format`, `--out`, and `--narrate` now work before or after the command, as the CLI help text
  shows.
- The narration description now matches the code: the CLI uses the built-in deterministic
  provider; the Claude and OpenAI-compatible providers are for library use.
- The EU AI Act note gives both high-risk application dates as amended by Regulation (EU) 2026/1744.
- `contract/` records `engine_commit` as the release tag, so it names a ref that exists.

### Added

- `examples/answers.json`, a complete answers file, and a README table of every question id.
- `scripts/generate_contract.py --engine-ref REF` to record a release tag as `engine_commit`.
- `ruff format --check` in CI.

### Changed

- The acceptance gate's check functions have descriptive names (`check_determinism`, ...), and the
  check list moved to `eval/acceptance/checks.yaml`. Behaviour is unchanged.

## [0.1.0] - 2026-07-01

### Added

- The AI-Readiness Standard: a deterministic, questionnaire-driven readiness diagnostic scoring an
  organization across seven governance dimensions on a five-level scale (L1–L5).
- Deterministic scoring core (pure domain), with a locked, inspectable scoring contract and explicit
  band cut-lines.
- Banded self-assessment question set covering every dimension.
- Readiness Report with an overall band, per-dimension bands, prioritized remediation (governance and
  measurement first), an advisory notice, and a routing call to action.
- HTML and dependency-free PDF renderers, and a text renderer.
- Demo mode: the full report on a bundled sample organization with zero input.
- Optional narration that summarizes a finished report and never influences a band. The CLI
  (`--narrate`) uses a built-in deterministic provider. Claude and OpenAI-compatible providers
  (bring-your-own-key) are included for library use; the CLI does not call them.
- Command-line interface (`ai-readiness-audit`) with `demo` and `assess` commands.
- Clean Architecture (hexagonal ports and adapters) enforced by an import contract, plus lint, strict
  typing, tests, and an acceptance-criteria eval gate.

### Standards lineage

- The seven dimensions are anchored to the **ISO/IEC 42001** management-system family as the primary
  structural lineage, with **NIST AI RMF** functions (GOVERN / MAP / MEASURE / MANAGE) and the
  Generative AI Profile providing per-dimension functional alignment and risk vocabulary. The
  **FFIEC IT Examination Handbook Work Program** is retained as *method inspiration* (tiered
  objectives → procedures → evidence), cited in the report footer and README only. The L1–L5 bands
  remain this standard's own authored contribution; the referenced standards do not define them.

[0.1.1]: https://github.com/wmemorgan/ai-readiness-audit/releases/tag/v0.1.1
[0.1.0]: https://github.com/wmemorgan/ai-readiness-audit/releases/tag/v0.1.0
