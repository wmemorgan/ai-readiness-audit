# The AI-Readiness Standard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/wmemorgan/ai-readiness-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/wmemorgan/ai-readiness-audit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Typed: mypy](https://img.shields.io/badge/typed-mypy-blue.svg)](https://mypy-lang.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Release](https://img.shields.io/badge/release-v0.1.0-informational.svg)](CHANGELOG.md)

**Seven dimensions. Five levels. One honest picture of where your organization stands
before you build with AI.**

The **AI-Readiness Standard** is an authored, regulator-grade diagnostic. You answer a
structured self-assessment; the engine scores it **deterministically** and returns a banded
**Readiness Report** — a level per dimension, an overall level, and a prioritized list of the
gaps to close first. It ingests **answers, not artifacts**: no documents, no data, no upload.

> It is an **advisory** diagnostic — a picture of *structural* readiness. It is **not** a
> certification and **not** a guarantee that any given AI deployment will succeed.

## The seven dimensions

| # | Dimension | Examination lineage | Core question |
|---|-----------|---------------------|---------------|
| 1 | Governance & Decision Rights | Management + Audit oversight | Accountable executive, written policy, approval gates? |
| 2 | Risk & Control Posture | Risk Management + Information Security | AI-specific risks named and mapped to controls by severity? |
| 3 | Data Readiness | Operations | Data accessible, governed, quality-assured, rights-cleared? |
| 4 | Security & Privacy | Information Security | Access control, PII handling, isolation, third-party posture? |
| 5 | Talent & Operating Model | Development & Acquisition + Management | Skills, roles (build/operate/govern), run-state ownership? |
| 6 | Third-Party & Concentration Risk | Outsourcing | Concentration understood, controlled, portable? |
| 7 | Measurement & Assurance | Audit | Can you evaluate outputs, severity, and the evaluation itself? |

## The five levels

**L1 Ad hoc → L2 Emerging → L3 Defined → L4 Governed → L5 Optimized.** The same level
vocabulary applies to each dimension and to your overall readiness.

## Quickstart

```bash
pip install ai-readiness-audit

# Run the full report on a bundled sample organization — zero input:
ai-readiness-audit --format html --out report.html demo

# Assess your own answers (JSON: question id -> level 1..5):
ai-readiness-audit --format text assess --answers answers.json
```

## How it scores

Scoring is a **pure, deterministic** function: the same answers always produce the same
levels. There is no model in the scoring path — an optional plain-language **narration**
feature (bring-your-own-key) can summarize a finished report, but it *never* changes a level.

## Architecture

The engine follows a hexagonal, ports-and-adapters design (Clean Architecture):

```
interface  ──▶ application ──▶ domain (pure: rubric, scoring, banding, remediation)
adapters   ──▶ application ──▶ domain
```

The **domain core** performs no I/O and imports no outer layer — which is exactly what makes
scoring reproducible. Report rendering, PDF output, narration, and delivery are **adapters**
behind ports; the core never depends on them. The dependency rule is enforced in CI.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Built on / Cites

The AI-Readiness Standard is an original work. It rests on, and cites, these public frameworks:

- **FFIEC IT Examination Handbook — Work Program** (the tiered objectives → procedures →
  evidence examination structure, transposed to AI adoption).
- **NIST AI Risk Management Framework (AI RMF 1.0)** (AI risk vocabulary).

These are the foundations the standard cites; they are not the standard itself.

## License

[MIT](LICENSE) © 2026 Wilfred Morgan
