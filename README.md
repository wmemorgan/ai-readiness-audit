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

The **AI-Readiness Standard** is an audit-grade readiness standard aligned to ISO/IEC 42001
domains and NIST AI RMF functions. You answer a structured self-assessment; the engine scores it
**deterministically** and returns a banded **Readiness Report** — a level per dimension, an overall
level, and a prioritized list of the gaps to close first. It ingests **answers, not artifacts**:
no documents, no data, no upload.

> It is an **advisory** diagnostic — a picture of *structural* readiness. It is **not** a
> certification and **not** a guarantee that any given AI deployment will succeed.

## The seven dimensions

| Dimension | ISO/IEC 42001 lineage | NIST AI RMF | Core question |
|-----------|-----------------------|-------------|---------------|
| Governance & Decision Rights | Cl. 5 (Leadership) + ISO/IEC 38507 | GOVERN | Accountable executive, written policy, approval gates? |
| Risk & Control Posture | ISO/IEC 23894 + Cl. 6 (Planning) | MAP + MANAGE | AI-specific risks named and mapped to controls by severity? |
| Data Readiness | Annex A (Data for AI) + ISO/IEC 5259 | MAP | Data accessible, governed, quality-assured, rights-cleared? |
| Security & Privacy | ISO/IEC 27001 + ISO/IEC 27701 | MANAGE | Access control, PII handling, isolation, third-party posture? |
| Talent & Operating Model | Cl. 7 (Support — competence) | GOVERN | Skills, roles (build/operate/govern), run-state ownership? |
| Third-Party & Concentration Risk | Annex A (Suppliers) + ISO/IEC 27036 | GOVERN + MANAGE | Concentration understood, controlled, portable? |
| Measurement & Assurance | Cl. 9 (Performance eval) + ISO/IEC 42005 | MEASURE | Can you evaluate outputs, severity, and the evaluation itself? |

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

## Standards Lineage

The AI-Readiness Standard is an original work built on a three-layer synthesis of public standards:

- **ISO/IEC 42001 family** supplies the management-system **domain structure** — the shape of the
  seven dimensions (leadership, planning, support, operation, performance evaluation, and the
  Annex A controls for data and suppliers), extended by ISO/IEC 38507, 23894, 5259, 27001, 27701,
  27036, and 42005.
- **NIST AI RMF** supplies the **risk functions** (GOVERN, MAP, MEASURE, MANAGE) and the Generative
  AI Profile's risk vocabulary, tagged per dimension.
- **FFIEC examination discipline** supplies the **method** — the tiered *objectives → procedures →
  evidence* structure that turns a framework into an auditable diagnostic.

None of the three publishes a scored maturity band. **The L1–L5 bands and their cut-lines are this
standard's own authored contribution.** These standards inform the diagnostic; they do not define
the bands.

These standards also support organizations preparing for emerging AI regulation, including
management-system approaches referenced by the EU AI Act (high-risk obligations effective
December 2, 2027).

## Built on / Cites

- **ISO/IEC 42001:2023** — AI management systems (iso.org/standard/42001)
- **ISO/IEC 23894, 38507, 42005, 27001, 27701, 5259 series, 27036**
- **NIST AI RMF 1.0 (AI 100-1)** + **Generative AI Profile (AI 600-1)**
- **FFIEC IT Examination Handbook Work Program** — method inspiration
  (tiered objectives → procedures → evidence, by domain)

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE) © 2026 Wilfred Morgan
