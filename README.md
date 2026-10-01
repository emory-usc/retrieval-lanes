# Retrieval Lanes

[![CI](https://github.com/emory-usc/retrieval-lanes/actions/workflows/ci.yml/badge.svg)](https://github.com/emory-usc/retrieval-lanes/actions/workflows/ci.yml)

A deterministic, dependency-free comparison of three retrieval strategies over
the same synthetic corpus. It answers one question with runnable evidence:
**which retrieval tool fits which job?**

Three lanes, same index, same corpus:

| Lane | What it is | Synthesis | Deterministic |
|---|---|---|---|
| **direct** | Ranked keyword search with a metadata filter | None — raw hits | Yes |
| **rag** | Single-pass top-k retrieval + templated synthesis with citations | Yes | Yes |
| **agentic** | Query decomposition + iterative retrieval + merge | Yes | Yes |

The punchline is *not* "agents good, search bad". It is "pick the right tool
for the retrieval job":

```
direct ──────────────► rag ──────────────► agentic
(you get hits)         (you add synthesis)  (you add iteration)
no synthesis           single-pass scope    multi-hop scope
```

## Why deterministic

There is no LLM and no external service. Retrieval is TF-IDF over a synthetic
corpus; synthesis is templated. Every run is reproducible — the same query
always returns the same result — which is exactly the property you lose the
moment you bolt an LLM onto the pipeline. The comparison is honest because the
only variable is the retrieval strategy, not the model.

## Quick start

```bash
pip install -e ".[dev]"
retrieval-lanes compare "reusable rockets versus the shuttle and Mars"
retrieval-lanes eval
```

## The eval harness

`evals/golden_queries.json` holds queries with the document ids each *should*
surface and the lane the job type calls for. The eval verifies the declared
winner actually achieves recall@5 = 1.0 on every query, and reports all three
lanes' recall honestly — the "which tool wins" story is backed by measurement,
not assertion.

The shape is the same as LLM-eval scoring (e.g. LangSmith dataset
experiments): golden inputs, expected references, a metric per run, and a
declared winner per scenario. If you swap the TF-IDF index for a vector store
and the templated synthesis for a model call, the eval harness carries over
unchanged.

## Structure

```
src/retrieval_lanes/
├── corpus.py    # synthetic documents
├── index.py     # TF-IDF index + metadata filter
├── lanes.py     # direct / rag / agentic
└── cli.py       # compare + eval commands
evals/
├── golden_queries.json
└── run_eval.py
tests/
└── test_lanes.py
```

## Security posture

See `SECURITY.md`. The short version: no external services, no credentials,
synthetic corpus, queries are never executed as code, and the eval enforces
the retrieval contract on every CI run.
