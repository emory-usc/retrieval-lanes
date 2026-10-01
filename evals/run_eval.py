"""Standalone eval runner (does not require the package to be installed).

Each golden query declares, by job type, the lane that *should* handle it. The
eval then verifies that the declared winner actually surfaces every expected
document (recall@5 == 1.0), while reporting all three lanes' recall honestly.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from retrieval_lanes.index import Index  # noqa: E402
from retrieval_lanes.lanes import Agentic, DirectSearch, Rag  # noqa: E402


def main() -> int:
    qpath = Path(__file__).resolve().parent / "golden_queries.json"
    queries = json.loads(qpath.read_text())
    idx = Index()
    direct, rag, agentic = DirectSearch(idx), Rag(idx), Agentic(idx)

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
        print(
            f"[{status}] {q['query']!r}  (expected winner: {winner})"
        )
        print(
            f"       recall@5: direct={recalls['direct']:.2f} "
            f"rag={recalls['rag']:.2f} agentic={recalls['agentic']:.2f}"
        )

    print(f"\nwinner tally: {tally}")
    print(f"result: {'ALL PASS' if failures == 0 else f'{failures} FAILURE(S)'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
