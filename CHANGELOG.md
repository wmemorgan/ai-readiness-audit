# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Optional, disabled-by-default LLM narration feature (mock, Claude, and OpenAI-compatible providers,
  bring-your-own-key) that summarizes a finished report and never influences a band.
- Command-line interface (`ai-readiness-audit`) with `demo` and `assess` commands.
- Clean Architecture (hexagonal ports and adapters) enforced by an import contract, plus lint, strict
  typing, tests, an IP firewall scan, and an acceptance-criteria eval gate.

### Standards lineage

- The seven dimensions are anchored to the **ISO/IEC 42001** management-system family as the primary
  structural lineage, with **NIST AI RMF** functions (GOVERN / MAP / MEASURE / MANAGE) and the
  Generative AI Profile providing per-dimension functional alignment and risk vocabulary. The
  **FFIEC IT Examination Handbook Work Program** is retained as *method inspiration* (tiered
  objectives → procedures → evidence), cited in the report footer and README only. The L1–L5 bands
  remain this standard's own authored contribution; the referenced standards do not define them.

[0.1.0]: https://github.com/wmemorgan/ai-readiness-audit/releases/tag/v0.1.0
