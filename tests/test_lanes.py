"""Tests for retrieval-lanes."""

from retrieval_lanes.index import Index
from retrieval_lanes.lanes import Agentic, DirectSearch, Rag


def build():
    idx = Index()
    return DirectSearch(idx), Rag(idx), Agentic(idx)


def test_index_ranks_relevant_docs_first():
    idx = Index()
    results = idx.search("reusable rocket")
    assert results, "expected at least one hit"
    assert results[0][0].id in {"doc-001", "doc-006"}


def test_category_filter_narrows_results():
    idx = Index()
    results = idx.search("moon", filter_category="mission")
    assert results, "expected mission-category hits for 'moon'"
    assert all(d.category == "mission" for d, _ in results)


def test_direct_search_has_no_synthesis():
    direct, _, _ = build()
    r = direct.run("moon", category="mission")
    assert r.hits, "expected hits for 'moon' within mission category"
    assert not r.citations, "direct search must not synthesize"


def test_rag_cites_sources():
    _, rag, _ = build()
    r = rag.run("summarize the Moon landing and the samples")
    assert r.citations, "rag should cite sources"
    assert "doc-003" in r.hits


def test_agentic_decomposes_multi_hop():
    _, _, agentic = build()
    r = agentic.run("reusable rockets versus the space shuttle and crewed Mars")
    assert len(r.hits) >= 2, "multi-hop should fan out across sub-clauses"
    assert "doc-001" in r.hits


def test_all_lanes_deterministic():
    _, _, agentic = build()
    r1 = agentic.run("orbits gravity assists")
    r2 = agentic.run("orbits gravity assists")
    assert r1.hits == r2.hits
