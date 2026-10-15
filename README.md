# The AI-Readiness Standard

**AI Readiness Audit** (`ai-readiness-audit`) is the open-source reference implementation of the
AI-Readiness Standard.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/wmemorgan/ai-readiness-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/wmemorgan/ai-readiness-audit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Typed: mypy](https://img.shields.io/badge/typed-mypy-blue.svg)](https://mypy-lang.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Release](https://img.shields.io/badge/release-v0.1.1-informational.svg)](CHANGELOG.md)

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
git clone https://github.com/wmemorgan/ai-readiness-audit.git
cd ai-readiness-audit
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Run the full report on a bundled sample organization — zero input:
ai-readiness-audit --format html --out report.html demo

# Assess a completed questionnaire (see "Writing an answers file" below):
ai-readiness-audit --format text assess --answers examples/answers.json
```

To install without a clone:

```bash
pip install "git+https://github.com/wmemorgan/ai-readiness-audit.git@v0.1.1"
```

The package has no runtime dependencies. `--format` is `text` (default), `html`, or `pdf`;
`--out` writes to a file instead of stdout.

## Writing an answers file

An answers file is a JSON object that maps **every** question id to a level from 1 to 5.
[`examples/answers.json`](examples/answers.json) is a complete example (the bundled sample
organization) — copy it and change the levels. The five options for each question, from L1 to
L5, are the `level_anchors` in [`contract/readiness-contract.json`](contract/readiness-contract.json).

| Question id | Dimension | Question |
|---|---|---|
| `gov-1` | Governance & Decision Rights | Who is accountable for AI outcomes in your organization? |
| `gov-2` | Governance & Decision Rights | Is there a written AI policy governing acceptable use and approval? |
| `gov-3` | Governance & Decision Rights | How are AI initiatives approved before they ship? |
| `risk-1` | Risk & Control Posture | Are AI-specific risks named (hallucination, leakage, injection, drift)? |
| `risk-2` | Risk & Control Posture | Is there a human-in-the-loop gate calibrated to severity? |
| `risk-3` | Risk & Control Posture | How is model/output drift detected and contained? |
| `data-1` | Data Readiness | Is the data intended for AI accessible and inventoried? |
| `data-2` | Data Readiness | Is data quality assured for the data AI will consume? |
| `data-3` | Data Readiness | Are usage rights and licensing cleared for AI use of this data? |
| `sec-1` | Security & Privacy | How is access to AI systems and their data controlled? |
| `sec-2` | Security & Privacy | How is PII handled in AI workflows? |
| `sec-3` | Security & Privacy | Is third-party model/data processing understood and disclosed? |
| `talent-1` | Talent & Operating Model | Are the skills to build and run AI present or sourced? |
| `talent-2` | Talent & Operating Model | Are build, operate, and govern responsibilities defined? |
| `talent-3` | Talent & Operating Model | Who owns an AI system once it is in production? |
| `tp-1` | Third-Party & Concentration Risk | Is your model/vendor concentration understood? |
| `tp-2` | Third-Party & Concentration Risk | Are third-party AI dependencies contractually controlled? |
| `tp-3` | Third-Party & Concentration Risk | How portable are you off a given model or vendor? |
| `meas-1` | Measurement & Assurance | Can you evaluate the quality of AI outputs? |
| `meas-2` | Measurement & Assurance | Do you measure the severity of failures, not just their rate? |
| `meas-3` | Measurement & Assurance | Do you evaluate the evaluation itself for blind spots? |

A missing id, an unknown id, or a level outside 1..5 is reported as one error line, with exit
code 2.

## How it scores

Scoring is a **pure, deterministic** function: the same answers always produce the same
levels. There is no model in the scoring path.

**Narration** is an optional plain-language summary of a finished report, and it *never*
changes a level. The CLI's `--narrate` flag writes a summary from the built-in deterministic
provider to stderr — no key, no network. The package also includes Claude and
OpenAI-compatible providers for library use, with your own key. The CLI does not call an
external provider.

```python
# pip install "ai-readiness-audit[claude] @ git+https://github.com/wmemorgan/ai-readiness-audit.git@v0.1.1"
import json

from ai_readiness_audit.adapters.narration.claude import ClaudeNarrationProvider
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.domain.models import Band

with open("examples/answers.json", encoding="utf-8") as fh:
    answers = {qid: Band(level) for qid, level in json.load(fh).items()}
report = assess(answers)
print(ClaudeNarrationProvider(api_key="YOUR_ANTHROPIC_API_KEY").narrate(report))
```

For an OpenAI-compatible endpoint, use the `openai` extra and
`ai_readiness_audit.adapters.narration.openai_compatible.OpenAICompatibleNarrationProvider(api_key=..., model=..., base_url=...)`.

## Architecture

The engine follows a hexagonal, ports-and-adapters design (Clean Architecture):

```
interface  ──▶ application ──▶ domain (pure: rubric, scoring, banding, remediation)
adapters   ──▶ application ──▶ domain
```

The **domain core** performs no I/O and imports no outer layer — which is exactly what makes
scoring reproducible. Report rendering, PDF output, narration, and delivery are **adapters**
behind ports; the core never depends on them. The dependency rule is enforced in CI.

## Integration

`contract/` is the canonical, language-neutral integration surface for re-implementing the
scorer in another language or runtime:

- **`contract/readiness-contract.json`** — the rubric, the seven dimensions with their ISO/NIST
  lineage, the exact question prompts and level anchors, the deterministic scoring and gap-priority
  rules, and the report's shared copy.
- **`contract/parity-fixtures.json`** — golden input/output cases generated by running the engine;
  a conformant scorer must reproduce `per_dimension_levels`, `overall_level`, and `ordered_gaps`
  exactly.

Both are generated from the engine by `scripts/generate_contract.py` and kept in lock-step with it
by `tests/test_contract_parity.py` in CI, so the contract can never silently drift.

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
management-system approaches referenced by the EU AI Act. As amended by Regulation (EU)
2026/1744, its high-risk obligations apply from 2 December 2027 for stand-alone (Annex III)
systems and from 2 August 2028 for systems in products covered by Annex I.

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
