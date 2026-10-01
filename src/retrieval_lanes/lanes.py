"""Three retrieval lanes over a shared index.

Each lane returns a plain dict so the CLI can render them side-by-side. All
three are deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass

from .corpus import Document
from .index import Index


@dataclass
class LaneResult:
    lane: str
    query: str
    hits: list[str]  # document ids, ranked
    citations: list[str]  # titles used in synthesis
    summary: str


class DirectSearch:
    """Ranked keyword search with an optional category filter. No synthesis."""

    name = "direct"

    def __init__(self, index: Index):
        self.index = index

    def run(self, query: str, category: str | None = None) -> LaneResult:
        results = self.index.search(query, filter_category=category)
        hits = [d.id for d, _ in results]
        summary = f"{len(results)} documents match; no synthesis performed."
        return LaneResult(self.name, query, hits, [], summary)


class Rag:
    """Single-pass top-k retrieval + templated synthesis with citations."""

    name = "rag"

    def __init__(self, index: Index, top_k: int = 5):
        self.index = index
        self.top_k = top_k

    def run(self, query: str, category: str | None = None) -> LaneResult:
        results = self.index.search(query, filter_category=category, top_k=self.top_k)
        hits = [d.id for d, _ in results]
        citations = [d.title for d, _ in results]
        if not results:
            summary = "No relevant documents found within the requested scope."
        else:
            joined = "; ".join(citations)
            summary = (
                f"Synthesis grounded in {len(results)} document(s): {joined}. "
                f"(Scope: {'category=' + category if category else 'whole corpus'}.)"
            )
        return LaneResult(self.name, query, hits, citations, summary)


class Agentic:
    """Query decomposition + iterative retrieval, merged across sub-queries."""

    name = "agentic"

    def __init__(self, index: Index, top_k: int = 3):
        self.index = index
        self.top_k = top_k

    def _decompose(self, query: str) -> list[str]:
        # Deterministic, crude decomposition: split on conjunction cues so a
        # multi-hop question fans out across clauses.
        parts = [p.strip() for p in re_split_clauses(query)]
        return [p for p in parts if p]

    def run(self, query: str) -> LaneResult:
        sub_queries = self._decompose(query) or [query]
        seen: list[str] = []
        titles: list[str] = []
        for sub in sub_queries:
            for doc, _ in self.index.search(sub, top_k=self.top_k):
                if doc.id not in seen:
                    seen.append(doc.id)
                    titles.append(doc.title)
        summary = (
            f"Iterative retrieval over {len(sub_queries)} sub-question(s) "
            f"surfaced {len(seen)} document(s): {'; '.join(titles)}."
        )
        return LaneResult(self.name, query, seen, titles, summary)


def re_split_clauses(query: str) -> list[str]:
    import re

    # Split on conjunction cues so a multi-hop question fans out across clauses.
    # Deliberately does NOT split on "how" (often the query opener).
    return [s for s in re.split(r"\b(?:and|versus|vs|compared to)\b", query, flags=re.I)]
