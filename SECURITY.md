# Security Policy

## Reporting a vulnerability

Report security issues privately rather than opening a public issue. Include a
description, reproduction steps, and any proposed fix. Do not include real data
or credentials in any report.

## Security posture

- **No external services, no credentials.** The project is standard-library
  Python. There is nothing to configure and no secret to store.
- **Deterministic by construction.** Retrieval and synthesis are pure
  functions; the same query always produces the same result, so outputs are
  reproducible and auditable.
- **Synthetic corpus only.** The knowledge base is hand-written synthetic
  content. No real source material is involved.
- **No prompt or input is executed.** Queries are tokenized and scored; nothing
  in a query is interpreted as code.
- **Eval-first.** The golden-query harness verifies the retrieval contract on
  every CI run, so regressions in recall are caught mechanically.

## Supported versions

Only the latest `main` branch is supported for security fixes.
