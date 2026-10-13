# Security Policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately using GitHub's
[private vulnerability reporting](https://github.com/wmemorgan/ai-readiness-audit/security/advisories/new)
rather than opening a public issue. You will receive an acknowledgement, and we will work with
you on a coordinated disclosure.

## Scope notes

- The engine ingests **questionnaire answers only** — it does not accept file uploads or parse
  documents, which keeps its input surface small.
- The engine is **policy-neutral**: it makes no data-retention or processing promises and pins no
  provider. Any such policy lives in a deployment, not in this library.
- The optional narration feature is **bring-your-own-key** and disabled by default; when enabled it
  sends a finished report summary to the configured provider. Review your provider's terms before
  enabling it.
