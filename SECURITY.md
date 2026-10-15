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
- The CLI never calls an external service. Its optional `--narrate` summary comes from a built-in,
  deterministic provider. The Claude and OpenAI-compatible narration providers are
  **bring-your-own-key** library components: when you construct and call one, it sends the finished
  report (never the raw answers) to that provider. Review your provider's terms before you use one.
