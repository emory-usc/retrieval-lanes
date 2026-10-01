"""CLI: compare three lanes side-by-side, and run the golden-query eval."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .index import Index
from .lanes import Agentic, DirectSearch, Rag


def build_lanes():
    idx = Index()
    return DirectSearch(idx), Rag(idx), Agentic(idx)


def run_compare(query: str, category: str | None = None) -> None:
    direct, rag, agentic = build_lanes()
    rows = [direct.run(query, category), rag.run(query, category), agentic.run(query)]
    for r in rows:
        print(f"\n[{r.lane.upper()}]")
        print(f"  hits:      {', '.join(r.hits) if r.hits else '(none)'}")
        if r.citations:
            print(f"  citations: {', '.join(r.citations)}")
        print(f"  summary:   {r.summary}")


def run_eval(queries_path: Path) -> int:
    if not queries_path.exists():
        print(f"missing golden queries file: {queries_path}")
        return 1

    queries = json.loads(queries_path.read_text())
    direct, rag, agentic = build_lanes()

    failures = 0
    tally: dict[str, int] = {}
    for q in queries:
        expected = set(q["expected_docs"])
        winner = q["expected_winner"]
        results = {
            "direct": direct.run(q["query"], q.get("category")),
            "rag": rag.run(q["query"], q.get("category")),
            "agentic": agentic.run(q["query"]),
        }
        recalls = {
            lane: len(set(r.hits[:5]) & expected) / len(expected)
            for lane, r in results.items()
        }
        ok = recalls[winner] >= 1.0
        tally[winner] = tally.get(winner, 0) + 1
        if not ok:
            failures += 1
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {q['query']!r}  (expected winner: {winner})")
        print(
            f"       recall@5: direct={recalls['direct']:.2f} "
            f"rag={recalls['rag']:.2f} agentic={recalls['agentic']:.2f}"
        )

    print(f"\nwinner tally: {tally}")
    print(f"result: {'ALL PASS' if failures == 0 else f'{failures} FAILURE(S)'}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="retrieval-lanes")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compare")
    c.add_argument("query")
    c.add_argument("--category", default=None)

    e = sub.add_parser("eval")
    e.add_argument("--queries", default=None)

    args = p.parse_args(argv)
    if args.cmd == "compare":
        run_compare(args.query, args.category)
        return 0
    if args.cmd == "eval":
        default = Path(__file__).resolve().parents[2] / "evals" / "golden_queries.json"
        path = Path(args.queries) if args.queries else default
        return run_eval(path)
    return 2


if __name__ == "__main__":
    sys.exit(main())
