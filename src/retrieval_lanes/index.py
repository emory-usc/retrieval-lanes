"""A small deterministic TF-IDF index with a metadata filter.

No external dependencies: tokenization and scoring are pure Python, so results
are reproducible run to run.
"""

from __future__ import annotations

import math
import re

from .corpus import DOCS, Document

_WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _WORD.findall(text.lower())


class Index:
    def __init__(self, docs: list[Document] | None = None):
        self.docs = docs or DOCS
        self._df: dict[str, int] = {}
        self._tfs: list[dict[str, int]] = []
        self._build()

    def _build(self) -> None:
        for doc in self.docs:
            tf: dict[str, int] = {}
            for tok in tokenize(doc.title + " " + doc.body):
                tf[tok] = tf.get(tok, 0) + 1
            self._tfs.append(tf)
            for tok in tf:
                self._df[tok] = self._df.get(tok, 0) + 1
        self._n = len(self.docs)

    def _idf(self, term: str) -> float:
        return math.log((self._n + 1) / (self._df.get(term, 0) + 1)) + 1.0

    def search(
        self,
        query: str,
        filter_category: str | None = None,
        top_k: int | None = None,
    ) -> list[tuple[Document, float]]:
        qterms = tokenize(query)
        scored: list[tuple[Document, float]] = []
        for i, doc in enumerate(self.docs):
            if filter_category and doc.category != filter_category:
                continue
            score = sum(self._tfs[i].get(t, 0) * self._idf(t) for t in qterms)
            if score > 0:
                scored.append((doc, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        if top_k is not None:
            scored = scored[:top_k]
        return scored
