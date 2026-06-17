"""Red/Green TDD test suite for the serp_claude pipeline.

Run with: uv run pytest tests/test_serp_claude.py
"""

from __future__ import annotations

import sys
from urllib.parse import urlparse

import pandas as pd
import pytest

from advertools.serp_claude import (
    _as_list,
    _augment_queries,
    _build_search_tool,
    _enrich_response,
    _multi_request,
    _query_map,
    _response_meta,
    _single_request,
    _validate_location,
    build_queries,
    serp_claude,
)


# ---------------------------------------------------------------------------
# Faithfulness audit: compare an enriched DataFrame against the RAW response
# (``response.model_dump()``) it was built from. The raw response is the source
# of truth; this re-derives every fact independently and reports any gap, so we
# can prove the DataFrame loses nothing. Used by the test suite AND the smoke
# notebook (``from tests import audit_response_coverage``).
# ---------------------------------------------------------------------------
def _norm(value):
    """Treat NaN/NaT the same as ``None`` so absent-vs-absent compares equal."""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


# A registry of every key we KNOWINGLY handle on the *content* side of the raw
# response — the half that a hand-written loop reshapes into rows, where an
# unrecognised key is silently dropped. (Top-level and ``usage`` keys no longer
# need a registry: production flattens them with ``json_normalize`` + a denylist,
# so any new field is auto-captured as a column rather than dropped.) The sweep
# flags anything here that isn't registered, turning silent drops / schema drift
# into a loud, reviewable gap. Keys map to a short note so it doubles as docs.
_KNOWN_BLOCK_TYPES = {
    "text": "answer text + citations",
    "server_tool_use": "search query (input.query) or executed code (input.code)",
    "web_search_tool_result": "SERP result rows (or error block)",
    "code_execution_tool_result": "code provenance (return_code/stderr)",
}
_KNOWN_SERVER_TOOL_USE_KEYS = {
    "type": "ignored: constant 'server_tool_use'",
    "id": "consumed -> links results/code via tool_use_id",
    "name": "consumed: routes web_search vs code_execution",
    "input": "consumed: search query / executed code",
    "caller": "consumed -> search_via (code-execution provenance)",
}
_KNOWN_CODE_RESULT_KEYS = {
    # outer block keys
    "type": "ignored: constant 'code_execution_tool_result'",
    "tool_use_id": "consumed -> matched to code-execution block",
    "content": "consumed: inner return_code/stderr",
    # inner content keys
    "return_code": "consumed -> code_return_code",
    "stderr": "consumed -> code_stderr",
    "encrypted_stdout": "ignored: opaque blob (agreed drop)",
}
_KNOWN_RESULT_KEYS = {
    "type": "ignored: constant 'web_search_result'",
    "url": "consumed",
    "title": "consumed",
    "page_age": "consumed",
    "encrypted_content": "ignored: opaque multi-turn blob (agreed drop)",
}
_KNOWN_CITATION_KEYS = {
    "type": "ignored: constant 'web_search_result_location'",
    "url": "consumed -> matched to SERP row",
    "cited_text": "consumed",
    "title": "ignored: redundant with the result row's title",
    "encrypted_index": "ignored: opaque multi-turn blob (agreed drop)",
}


def _sweep_unaudited_fields(raw):
    """Flag any unrecognised key on the *content* side of the raw response.

    This is the adversarial half of the audit. Response metadata is captured
    wholesale by ``json_normalize`` (new fields become columns, never dropped),
    so the only place a field can still vanish silently is the hand-written
    content loop. This walks the *actual* content and reports anything
    unregistered — unhandled block types, unexpected ``server_tool_use`` /
    result / citation / code-execution keys, and web-search error blocks.
    Returns the list of gaps (empty when the content matches our registry).
    """
    gaps = []

    for block in raw.get("content", []) or []:
        btype = block.get("type")
        if btype not in _KNOWN_BLOCK_TYPES:
            gaps.append(f"unhandled content block type: {btype!r}")
            continue
        if btype == "server_tool_use":
            for key in block:
                if key not in _KNOWN_SERVER_TOOL_USE_KEYS:
                    gaps.append(f"unaudited server_tool_use field: {key!r}")
        if btype == "code_execution_tool_result":
            inner = block.get("content")
            inner_keys = list(inner) if isinstance(inner, dict) else []
            for key in [*block, *inner_keys]:
                if key not in _KNOWN_CODE_RESULT_KEYS:
                    gaps.append(f"unaudited code_execution field: {key!r}")
        if btype == "web_search_tool_result":
            results = block.get("content")
            if not isinstance(results, list):
                # An error block: content is a dict, not a list of results.
                code = (
                    (results or {}).get("error_code")
                    if isinstance(results, dict)
                    else None
                )
                gaps.append(f"web_search error block (error_code={code!r})")
                continue
            for result in results:
                for key in result:
                    if key not in _KNOWN_RESULT_KEYS:
                        gaps.append(f"unaudited result field: {key!r}")
        for citation in block.get("citations") or []:
            for key in citation:
                if key not in _KNOWN_CITATION_KEYS:
                    gaps.append(f"unaudited citation field: {key!r}")

    return gaps


def audit_response_coverage(df, raw):
    """Audit that ``df`` faithfully represents one raw Anthropic response.

    ``df`` is the enriched frame for a *single* response (filter a multi-request
    frame by ``response_id`` first); ``raw`` is that response's
    ``model_dump()`` dict. Returns a report ``dict`` with an ``ok`` flag and a
    list of human-readable ``gaps`` (empty when faithful), plus a few counts.

    Checks (each re-derived straight from ``raw``):

    - **result coverage** — one row per ``web_search_result`` across every
      (non-error) search, matched on ``(search_index, serp_rank)``, with
      ``url``/``title``/``domain``/``page_age``/``search_query`` intact.
    - **search count** — distinct ``search_index`` equals the number of searches.
    - **citation coverage** — each cited url's FULL ordered citation list, both
      snippet text and provenance (``cited_text`` / ``block_index`` /
      ``rank_within_block`` / ``rank``), is reconstructed from raw and compared
      verbatim against the row's ``@@``-joined columns, so a dropped, reordered,
      or duplicated citation surfaces — not just missing text. A cited url that
      never appears as a result is flagged as an *orphan*.
    - **answer / usage** — ``answer`` text plus every broadcast metadata column
      (``response_id``/``response_model``, token counts, ``web_search_requests``,
      ``service_tier``, ...) match the raw response, by Anthropic's own names.
    - **completeness sweep** — any raw key we neither consume nor knowingly
      ignore is flagged (see :func:`_sweep_unaudited_fields`), so silently
      dropped fields and schema drift surface instead of passing unnoticed.
    """
    gaps = []
    content = raw.get("content", []) or []

    # tool_use_id -> the query Claude actually searched.
    queries = {}
    for block in content:
        if block.get("type") == "server_tool_use" and block.get("name") == "web_search":
            queries[block.get("id")] = (block.get("input") or {}).get("query")

    # Non-error search blocks, in order. Each maps to search_index = position+1.
    search_blocks = [
        block
        for block in content
        if block.get("type") == "web_search_tool_result"
        and isinstance(block.get("content"), list)
    ]

    # Every result Claude returned, with the integer keys it should land under.
    expected = []
    for search_index, block in enumerate(search_blocks, start=1):
        query = queries.get(block.get("tool_use_id"))
        for serp_rank, result in enumerate(block["content"], start=1):
            url = result.get("url")
            expected.append(
                {
                    "search_index": search_index,
                    "serp_rank": serp_rank,
                    "url": url,
                    "title": result.get("title"),
                    "domain": urlparse(url).netloc if url else None,
                    "page_age": result.get("page_age"),
                    "search_query": query,
                }
            )

    if len(df) != len(expected):
        gaps.append(f"row count {len(df)} != {len(expected)} search results in raw")

    distinct_searches = (
        df["search_index"].nunique() if "search_index" in df and len(df) else 0
    )
    if distinct_searches != len(search_blocks):
        gaps.append(
            f"distinct search_index {distinct_searches} != "
            f"{len(search_blocks)} searches in raw"
        )

    # Per-result field coverage, matched on the integer (search_index, serp_rank).
    if len(df) == len(expected) and expected:
        actual = df.set_index(["search_index", "serp_rank"])
        for exp in expected:
            key = (exp["search_index"], exp["serp_rank"])
            if key not in actual.index:
                gaps.append(f"missing result row {key}")
                continue
            row = actual.loc[key]
            for field in ("url", "title", "domain", "page_age", "search_query"):
                if _norm(row[field]) != _norm(exp[field]):
                    gaps.append(
                        f"{field} mismatch at {key}: {row[field]!r} != {exp[field]!r}"
                    )

    # Citations: reconstruct each cited url's FULL ordered citation list —
    # snippet AND provenance — from raw (mirroring the enrich traversal:
    # content order, global rank, per-block rank), then prove the row's four
    # ``@@``-joined columns reproduce it EXACTLY. Substring-checking the text
    # alone would miss dropped/duplicated citations and any provenance loss, so
    # we compare the joined strings verbatim. A url cited but never returned as
    # a result is an orphan.
    raw_citations = {}  # url -> list of (cited_text, block_index, rwb, rank)
    global_rank = 0
    for block_index, block in enumerate(content):
        for rwb, citation in enumerate(block.get("citations") or [], start=1):
            global_rank += 1
            raw_citations.setdefault(citation.get("url"), []).append(
                (
                    citation.get("cited_text") or "",
                    str(block_index),
                    str(rwb),
                    str(global_rank),
                )
            )
    result_urls = {exp["url"] for exp in expected}
    prov_cols = ("cited_text", "block_index", "rank_within_block", "rank")
    for url, cites in raw_citations.items():
        if url not in result_urls:
            gaps.append(f"orphan citation: cited url {url} has no SERP result row")
            continue
        missing = [c for c in prov_cols if c not in df.columns]
        if missing:
            gaps.append(f"citation columns {missing} missing though {url} was cited")
            continue
        # enrich joins ALL of a url's citations onto EVERY result row for that
        # url, so each matching row must reproduce the same four joined strings.
        expected_joined = {
            "cited_text": "@@".join(c[0] for c in cites),
            "block_index": "@@".join(c[1] for c in cites),
            "rank_within_block": "@@".join(c[2] for c in cites),
            "rank": "@@".join(c[3] for c in cites),
        }
        for _, row in df.loc[df["url"] == url].iterrows():
            for col in prov_cols:
                if _norm(row[col]) != expected_joined[col]:
                    gaps.append(
                        f"citation {col} mismatch for {url}: "
                        f"{row[col]!r} != {expected_joined[col]!r}"
                    )

    # Answer text and response-level metadata. We derive the expected metadata
    # the SAME way production does (json_normalize + denylist + renames), so the
    # audit can never drift from the enrichment: every flattened column must be
    # present and equal in the frame.
    if len(df):
        expected_answer = "".join(
            block.get("text", "") for block in content if block.get("type") == "text"
        )
        if "answer" in df.columns and _norm(df["answer"].iloc[0]) != expected_answer:
            gaps.append("answer text mismatch")
        expected_meta = _response_meta(raw).iloc[0].to_dict()
        for col, exp in expected_meta.items():
            if col not in df.columns:
                gaps.append(f"{col} column missing")
            elif _norm(df[col].iloc[0]) != _norm(exp):
                gaps.append(f"{col} mismatch: {df[col].iloc[0]!r} != {exp!r}")

    gaps.extend(_sweep_unaudited_fields(raw))

    return {
        "ok": not gaps,
        "gaps": gaps,
        "n_rows": len(df),
        "n_results_raw": len(expected),
        "n_searches_raw": len(search_blocks),
        "n_cited_urls_raw": len(raw_citations),
    }


# ---------------------------------------------------------------------------
# Phase 1: _as_list
# ---------------------------------------------------------------------------
def test_as_list():
    assert _as_list("opus-4-8") == ["opus-4-8"]
    assert _as_list(5) == [5]

    # Lists pass through unchanged (and as a new list, not the same object).
    src = ["a", "b"]
    out = _as_list(src)
    assert out == ["a", "b"]

    # Tuples are treated as sequences too.
    assert _as_list(("a", "b")) == ["a", "b"]

    # Any non-string collection is materialized into a list.
    import pandas as pd

    assert _as_list(pd.Series(["a", "b"])) == ["a", "b"]
    assert sorted(_as_list({"a", "b"})) == ["a", "b"]

    # None means "absent" -> empty list, so callers can iterate safely.
    assert _as_list(None) == []

    # Dicts are scalar units (a single location), NOT iterated into keys.
    loc = {"city": "Lisbon", "country": "PT"}
    assert _as_list(loc) == [loc]


# ---------------------------------------------------------------------------
# Phase 2: _validate_location
# ---------------------------------------------------------------------------
def test_validate_location_forces_approximate_type():
    # type is mandatory and always "approximate"; inject it when missing.
    out = _validate_location(
        {"city": "Lisbon", "country": "PT", "timezone": "Europe/Lisbon"}
    )
    assert out["type"] == "approximate"

    # An explicit wrong type is corrected, not trusted.
    out = _validate_location({"type": "precise", "country": "FR"})
    assert out["type"] == "approximate"


def test_validate_location_returns_new_dict():
    src = {"country": "DE"}
    out = _validate_location(src)
    assert out is not src  # never mutate the caller's dict
    assert src == {"country": "DE"}


def test_validate_location_normalizes_country_case():
    out = _validate_location({"country": "fr"})
    assert out["country"] == "FR"


def test_validate_location_accepts_valid_country_codes():
    for code in ["US", "RU", "FR", "DE", "PT", "JP"]:
        out = _validate_location({"country": code})
        assert out["country"] == code


def test_validate_location_rejects_bad_country_code():
    with pytest.raises(ValueError):
        _validate_location({"country": "XX"})  # not an ISO 3166-1 alpha-2
    with pytest.raises(ValueError):
        _validate_location({"country": "USA"})  # alpha-3, not alpha-2


def test_validate_location_validates_timezone():
    out = _validate_location({"timezone": "America/Los_Angeles"})
    assert out["timezone"] == "America/Los_Angeles"
    with pytest.raises(ValueError):
        _validate_location({"timezone": "Mars/Phobos"})


def test_validate_location_country_and_timezone_optional():
    # All fields optional except the forced type.
    out = _validate_location({"city": "Lisbon"})
    assert out == {"type": "approximate", "city": "Lisbon"}


def test_validate_location_requires_dict():
    with pytest.raises(TypeError):
        _validate_location("Lisbon")


# ---------------------------------------------------------------------------
# Phase 3: _build_search_tool
# ---------------------------------------------------------------------------
def test_build_search_tool_basic_schema():
    tool = _build_search_tool("web_search_20250305", location=None, max_uses=5)
    assert tool["type"] == "web_search_20250305"
    assert tool["name"] == "web_search"
    assert tool["max_uses"] == 5


def test_build_search_tool_omits_location_when_none():
    tool = _build_search_tool("web_search_20250305", location=None, max_uses=5)
    assert "user_location" not in tool


def test_build_search_tool_embeds_location():
    loc = {
        "type": "approximate",
        "city": "Lisbon",
        "country": "PT",
        "timezone": "Europe/Lisbon",
    }
    tool = _build_search_tool("web_search_20250305", location=loc, max_uses=3)
    assert tool["user_location"] == loc
    assert tool["max_uses"] == 3


def test_build_search_tool_honors_version():
    tool = _build_search_tool("web_search_20260209", location=None, max_uses=5)
    assert tool["type"] == "web_search_20260209"


def test_build_search_tool_does_not_mutate_location():
    loc = {"type": "approximate", "city": "Lisbon"}
    tool = _build_search_tool("web_search_20250305", location=loc, max_uses=5)
    # embedding a copy keeps the tool independent of the caller's dict
    tool["user_location"]["city"] = "Porto"
    assert loc["city"] == "Lisbon"


# ---------------------------------------------------------------------------
# Phase 4: _augment_queries
# ---------------------------------------------------------------------------
def _queries():
    # 2 base queries with one content variable.
    return build_queries("Best {x} in town", {"x": ["sushi", "pizza"]})


def test_build_queries_raises_when_placeholders_dont_match_keys():
    # Extra variable key with no placeholder -> ValueError.
    with pytest.raises(ValueError, match="must match"):
        build_queries("Best {dish} in town", {"dish": ["sushi"], "city": ["Lisbon"]})
    # Missing variable for a placeholder -> ValueError.
    with pytest.raises(ValueError, match="must match"):
        build_queries("Best {dish} in {city}", {"dish": ["sushi"]})


def test_augment_queries_full_cross_product_count():
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8", "sonnet-4-6"],
        locations=[{"country": "PT"}, {"country": "US"}],
        search_tool_versions=["web_search_20250305"],
    )
    # 2 queries x 2 models x 2 locations x 1 version = 8 rows
    assert len(plan) == 8


def test_augment_queries_preserves_content_columns():
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8"],
        locations=[],
        search_tool_versions=["web_search_20250305"],
    )
    # query + content variable survive the cross
    assert {"query", "x"} <= set(plan.columns)
    assert set(plan["x"]) == {"sushi", "pizza"}


def test_augment_queries_adds_execution_columns():
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8"],
        locations=[{"country": "PT", "city": "Lisbon", "timezone": "Europe/Lisbon"}],
        search_tool_versions=["web_search_20250305"],
    )
    for col in [
        "request_id",
        "model",
        "tool_version",
        "loc_country",
        "loc_city",
        "loc_timezone",
    ]:
        assert col in plan.columns
    assert set(plan["model"]) == {"opus-4-8"}
    assert set(plan["tool_version"]) == {"web_search_20250305"}
    assert set(plan["loc_country"]) == {"PT"}


def test_augment_queries_unique_request_ids():
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8", "sonnet-4-6"],
        locations=[{"country": "PT"}],
        search_tool_versions=["web_search_20250305"],
    )
    assert plan["request_id"].is_unique
    assert len(plan["request_id"]) == len(plan)


def test_augment_queries_no_locations_means_one_per_query():
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8"],
        locations=[],
        search_tool_versions=["web_search_20250305"],
    )
    # 2 queries x 1 model x (no location) x 1 version = 2 rows
    assert len(plan) == 2


def test_augment_queries_keeps_location_components_together():
    # Each row's loc_* fields must come from ONE location dict, never mixed.
    plan = _augment_queries(
        _queries(),
        models=["opus-4-8"],
        locations=[
            {"country": "PT", "city": "Lisbon", "timezone": "Europe/Lisbon"},
            {"country": "US", "city": "Seattle", "timezone": "America/Los_Angeles"},
        ],
        search_tool_versions=["web_search_20250305"],
    )
    pairs = set(zip(plan["loc_city"], plan["loc_timezone"]))
    assert pairs == {
        ("Lisbon", "Europe/Lisbon"),
        ("Seattle", "America/Los_Angeles"),
    }


# ---------------------------------------------------------------------------
# Phase 5: _enrich_response
# ---------------------------------------------------------------------------
class _FakeResponse:
    """Minimal stand-in exposing ``model_dump()`` like an Anthropic Message."""

    def __init__(self, dump):
        self._dump = dump

    def model_dump(self):
        return self._dump


def _citation(url, title, text):
    return {
        "type": "web_search_result_location",
        "url": url,
        "title": title,
        "cited_text": text,
    }


def _response_with_citations():
    # Realistic shape: a search returns three results (a, b, c), then Claude
    # quotes a and b in one answer block and c in a later block.
    content = [
        {"type": "text", "text": "Intro with no citations."},
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "q"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [
                _result("https://a.com/x", "A", "April 30, 2025"),
                _result("https://b.org/y", "B", "May 1, 2025"),
                _result("https://c.net/z", "C", "May 2, 2025"),
            ],
        },
        {
            "type": "text",
            "text": "First finding.",
            "citations": [
                _citation("https://a.com/x", "A", "snippet a"),
                _citation("https://b.org/y", "B", "snippet b"),
            ],
        },
        {
            "type": "text",
            "text": "Second finding.",
            "citations": [_citation("https://c.net/z", "C", "snippet c")],
        },
    ]
    return _FakeResponse(
        {
            "id": "msg_123",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 100, "output_tokens": 50},
            "content": content,
        }
    )


def _plan_row():
    return {
        "request_id": 7,
        "query": "Best sushi in town",
        "x": "sushi",
        "model": "claude-opus-4-8",
        "tool_version": "web_search_20250305",
        "location": None,
        "loc_country": None,
        "loc_city": None,
    }


def test_query_map_maps_tool_use_id_to_query():
    content = [
        {"type": "text", "text": "thinking"},
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "first query"},
        },
        {
            "type": "server_tool_use",
            "id": "srvtoolu_2",
            "name": "web_search",
            "input": {"query": "second query"},
        },
    ]
    assert _query_map(content) == {
        "srvtoolu_1": "first query",
        "srvtoolu_2": "second query",
    }


def test_query_map_empty_when_no_searches():
    content = [{"type": "text", "text": "no searches here"}]
    assert _query_map(content) == {}


def _result(url, title, page_age):
    return {
        "type": "web_search_result",
        "url": url,
        "title": title,
        "page_age": page_age,
    }


def _response_with_uncited_results():
    # One search returning two results, none of which Claude cited.
    content = [
        {"type": "text", "text": "Let me search."},
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "rent harringay"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [
                _result("https://a.com/x", "A", "April 30, 2025"),
                _result("https://b.org/y", "B", "May 1, 2025"),
            ],
        },
        {"type": "text", "text": "I could not find anything useful."},
    ]
    return _FakeResponse(
        {
            "id": "msg_r",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_enrich_response_emits_uncited_result_rows():
    df = _enrich_response(_response_with_uncited_results(), _plan_row())
    assert len(df) == 2
    assert list(df["url"]) == ["https://a.com/x", "https://b.org/y"]
    assert list(df["title"]) == ["A", "B"]
    assert list(df["domain"]) == ["a.com", "b.org"]
    assert list(df["page_age"]) == ["April 30, 2025", "May 1, 2025"]
    assert list(df["search_query"]) == ["rent harringay", "rent harringay"]
    assert list(df["serp_rank"]) == [1, 2]
    assert list(df["search_index"]) == [1, 1]
    # Uncited results carry no cited_text (the column only appears once some
    # citation exists; absent here, and that's fine — NaN-where-absent).
    assert "cited_text" not in df.columns


def _response_with_cited_and_uncited():
    # One search returns three results (a, b, c); Claude cites a and c only.
    content = [
        {"type": "text", "text": "Let me search."},
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "best sushi"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [
                _result("https://a.com/x", "A", "April 30, 2025"),
                _result("https://b.org/y", "B", "May 1, 2025"),
                _result("https://c.net/z", "C", "May 2, 2025"),
            ],
        },
        {
            "type": "text",
            "text": "Findings.",
            "citations": [
                _citation("https://a.com/x", "A", "snippet a"),
                _citation("https://c.net/z", "C", "snippet c"),
            ],
        },
    ]
    return _FakeResponse(
        {
            "id": "msg_mix",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_enrich_response_joins_search_metadata_onto_citations():
    df = _enrich_response(_response_with_cited_and_uncited(), _plan_row())
    # SERP backbone: one row per result, in SERP order (a, b, c). b is uncited.
    assert len(df) == 3
    assert list(df["url"]) == [
        "https://a.com/x",
        "https://b.org/y",
        "https://c.net/z",
    ]
    # Cited results carry their snippet; the uncited result (b) has none.
    assert list(df["cited_text"][[0, 2]]) == ["snippet a", "snippet c"]
    assert pd.isna(df["cited_text"].iloc[1])
    # search_query / serp_rank / page_age come straight off the SERP row.
    assert list(df["search_query"]) == ["best sushi", "best sushi", "best sushi"]
    assert list(df["serp_rank"]) == [1, 2, 3]
    assert list(df["page_age"]) == [
        "April 30, 2025",
        "May 1, 2025",
        "May 2, 2025",
    ]
    # cited_text.isna() cleanly flags the uncited result (b is in the middle).
    assert list(df["cited_text"].isna()) == [False, True, False]


def _response_with_two_searches():
    # One request, TWO searches: serp_rank must reset to 1 at the second search.
    content = [
        {
            "type": "server_tool_use",
            "id": "s1",
            "name": "web_search",
            "input": {"query": "first query"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "s1",
            "content": [
                _result("https://a.com", "A", None),
                _result("https://b.com", "B", None),
            ],
        },
        {
            "type": "server_tool_use",
            "id": "s2",
            "name": "web_search",
            "input": {"query": "second query"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "s2",
            "content": [
                _result("https://c.com", "C", None),
                _result("https://d.com", "D", None),
            ],
        },
    ]
    return _FakeResponse(
        {
            "id": "msg_two",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_enrich_response_serp_rank_resets_per_search():
    df = _enrich_response(_response_with_two_searches(), _plan_row())
    # search_index identifies the SERP (1, then 2); serp_rank is position within
    # each search and RESETS to 1 at the second search.
    assert list(df["search_index"]) == [1, 1, 2, 2]
    assert list(df["serp_rank"]) == [1, 2, 1, 2]
    assert list(df["search_query"]) == [
        "first query",
        "first query",
        "second query",
        "second query",
    ]


def test_enrich_response_ranks_are_integers():
    # A rank is a number, always — never NaN, never a string.
    df = _enrich_response(_response_with_two_searches(), _plan_row())
    assert df["serp_rank"].dtype.kind == "i"
    assert df["search_index"].dtype.kind == "i"


def test_enrich_response_flattens_citations():
    df = _enrich_response(_response_with_citations(), _plan_row())
    assert len(df) == 3  # 2 + 1 citations; narrative-only block excluded
    assert list(df["url"]) == ["https://a.com/x", "https://b.org/y", "https://c.net/z"]
    assert list(df["title"]) == ["A", "B", "C"]


def test_enrich_response_rank_columns():
    df = _enrich_response(_response_with_citations(), _plan_row())
    # Rows are in SERP order (a, b, c). Provenance comes from the matching
    # citation, ``@@``-joined per row (here each URL is cited once, so a single
    # value). These are citation-level, hence strings — unlike serp_rank.
    # global rank: 1..N in answer order
    assert list(df["rank"]) == ["1", "2", "3"]
    # rank_within_block resets per block (a=1, b=2 in block 3; c=1 in block 4)
    assert list(df["rank_within_block"]) == ["1", "2", "1"]
    # block_index is the content-block position of the citation (3 and 4 here)
    assert list(df["block_index"]) == ["3", "3", "4"]


def _response_with_url_cited_multiple_times():
    # One result URL that Claude quotes THREE times, in two different answer
    # blocks, with three different snippets — the realistic case that the old
    # ``citations[0]`` provenance silently dropped.
    content = [
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "q"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [_result("https://a.com/x", "A", "May 1, 2025")],
        },
        {
            "type": "text",
            "text": "First mention.",
            "citations": [
                _citation("https://a.com/x", "A", "snippet one"),
                _citation("https://a.com/x", "A", "snippet two"),
            ],
        },
        {
            "type": "text",
            "text": "Later mention.",
            "citations": [_citation("https://a.com/x", "A", "snippet three")],
        },
    ]
    return _FakeResponse(
        {
            "id": "msg_multi_cite",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_enrich_keeps_every_citation_for_a_repeated_url():
    # The fix for the "lossless" promise: all three snippets AND all three
    # provenance tuples are kept, ``@@``-joined in parallel (one row, since the
    # URL is a single result). Nothing is collapsed to citations[0].
    df = _enrich_response(_response_with_url_cited_multiple_times(), _plan_row())
    assert len(df) == 1
    row = df.iloc[0]
    assert row["cited_text"] == "snippet one@@snippet two@@snippet three"
    # block_index: blocks 2 and 2 (first text block) then 3 (second text block)
    assert row["block_index"] == "2@@2@@3"
    assert row["rank_within_block"] == "1@@2@@1"  # resets per block
    assert row["rank"] == "1@@2@@3"  # global answer order


def test_citation_columns_round_trip_via_split_explode():
    # The four citation-level columns stay positionally aligned, so a single
    # split+explode across all of them recovers the original citation-level
    # frame (3 rows here) with text and provenance still matched up.
    df = _enrich_response(_response_with_url_cited_multiple_times(), _plan_row())
    cols = ["cited_text", "block_index", "rank_within_block", "rank"]
    exploded = df.assign(**{c: df[c].str.split("@@") for c in cols}).explode(cols)
    assert list(exploded["cited_text"]) == [
        "snippet one",
        "snippet two",
        "snippet three",
    ]
    assert list(exploded["block_index"]) == ["2", "2", "3"]
    assert list(exploded["rank"]) == ["1", "2", "3"]


def test_enrich_response_derives_domain():
    df = _enrich_response(_response_with_citations(), _plan_row())
    assert list(df["domain"]) == ["a.com", "b.org", "c.net"]


def test_enrich_response_leads_with_query_then_variables():
    df = _enrich_response(_response_with_citations(), _plan_row())
    # Readers should see context first: the query, then the template variables.
    assert list(df.columns[:2]) == ["query", "x"]


def test_enrich_response_adds_joined_answer():
    df = _enrich_response(_response_with_citations(), _plan_row())
    # Narrative = all text blocks joined; broadcast onto every row.
    expected = "Intro with no citations.First finding.Second finding."
    assert set(df["answer"]) == {expected}


def test_enrich_response_broadcasts_plan_metadata():
    df = _enrich_response(_response_with_citations(), _plan_row())
    assert set(df["request_id"]) == {7}
    assert set(df["query"]) == {"Best sushi in town"}
    assert set(df["x"]) == {"sushi"}
    assert set(df["tool_version"]) == {"web_search_20250305"}


def test_enrich_response_includes_usage_metadata():
    df = _enrich_response(_response_with_citations(), _plan_row())
    for col in [
        "response_id",
        "usage.input_tokens",
        "usage.output_tokens",
        "stop_reason",
        "retrieved_at",
    ]:
        assert col in df.columns
    assert set(df["usage.input_tokens"]) == {100}
    assert set(df["usage.output_tokens"]) == {50}
    assert set(df["response_id"]) == {"msg_123"}


def test_enrich_response_no_citations_returns_empty():
    resp = _FakeResponse(
        {
            "id": "msg_x",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 5, "output_tokens": 5},
            "content": [{"type": "text", "text": "No citations here."}],
        }
    )
    df = _enrich_response(resp, _plan_row())
    assert len(df) == 0


def test_enrich_response_soft_handles_search_error():
    # web_search_tool_result_error must not raise; just yields no citations.
    resp = _FakeResponse(
        {
            "id": "msg_e",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 5, "output_tokens": 5},
            "content": [
                {
                    "type": "web_search_tool_result",
                    "tool_use_id": "srvtoolu_a",
                    "content": {
                        "type": "web_search_tool_result_error",
                        "error_code": "max_uses_exceeded",
                    },
                }
            ],
        }
    )
    df = _enrich_response(resp, _plan_row())
    assert len(df) == 0


# ---------------------------------------------------------------------------
# Phase 6: _single_request
# ---------------------------------------------------------------------------
class _MockMessages:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._response


class _MockClient:
    def __init__(self, response):
        self.messages = _MockMessages(response)


def _located_plan_row():
    row = _plan_row()
    row["model"] = "claude-opus-4-8"
    row["tool_version"] = "web_search_20250305"
    row["location"] = {"type": "approximate", "city": "Lisbon", "country": "PT"}
    return row


def test_single_request_calls_api_with_model_and_query():
    client = _MockClient(_response_with_citations())
    _single_request(_plan_row(), client, max_uses=5)
    assert len(client.messages.calls) == 1
    call = client.messages.calls[0]
    assert call["model"] == "claude-opus-4-8"
    # The query is sent as the user message content.
    assert call["messages"][0]["role"] == "user"
    assert call["messages"][0]["content"] == "Best sushi in town"


def test_single_request_passes_versioned_tool_and_location():
    client = _MockClient(_response_with_citations())
    _single_request(_located_plan_row(), client, max_uses=3)
    tool = client.messages.calls[0]["tools"][0]
    assert tool["type"] == "web_search_20250305"
    assert tool["name"] == "web_search"
    assert tool["max_uses"] == 3
    assert tool["user_location"]["city"] == "Lisbon"


def test_single_request_omits_location_when_none():
    client = _MockClient(_response_with_citations())
    _single_request(_plan_row(), client, max_uses=5)  # plan_row location=None
    tool = client.messages.calls[0]["tools"][0]
    assert "user_location" not in tool


def test_single_request_omits_temperature_by_default():
    client = _MockClient(_response_with_citations())
    _single_request(_plan_row(), client, max_uses=5)
    # Newer models reject temperature; omit the kwarg entirely unless asked.
    assert "temperature" not in client.messages.calls[0]


def test_single_request_passes_temperature_when_set():
    client = _MockClient(_response_with_citations())
    _single_request(_plan_row(), client, max_uses=5, temperature=0)
    assert client.messages.calls[0]["temperature"] == 0


def test_single_request_returns_enriched_dataframe():
    client = _MockClient(_response_with_citations())
    df = _single_request(_plan_row(), client, max_uses=5)
    # Same shape as _enrich_response output: 3 citations, ranks + metadata.
    assert len(df) == 3
    assert list(df["rank"]) == ["1", "2", "3"]
    assert set(df["request_id"]) == {7}
    assert "answer" in df.columns


def test_single_request_sorts_by_search_then_rank_with_fresh_index():
    client = _MockClient(_response_with_two_searches())
    df = _single_request(_plan_row(), client, max_uses=5)
    # Rows in SERP order (search_index, serp_rank) and a clean 0..n-1 index.
    assert list(df["search_index"]) == [1, 1, 2, 2]
    assert list(df["serp_rank"]) == [1, 2, 1, 2]
    assert list(df.index) == [0, 1, 2, 3]


# ---------------------------------------------------------------------------
# Phase 7: _multi_request
# ---------------------------------------------------------------------------
import threading


class _CountingMessages:
    """Thread-safe mock that records every call and returns a fixed response."""

    def __init__(self, response):
        self._response = response
        self.calls = []
        self._lock = threading.Lock()

    def create(self, **kwargs):
        with self._lock:
            self.calls.append(kwargs)
        return self._response


class _CountingClient:
    def __init__(self, response):
        self.messages = _CountingMessages(response)


class _RaisingMessages:
    """Mock that raises for one specific query, succeeds otherwise."""

    def __init__(self, response, fail_query):
        self._response = response
        self._fail_query = fail_query
        self.calls = []
        self._lock = threading.Lock()

    def create(self, **kwargs):
        with self._lock:
            self.calls.append(kwargs)
        if kwargs["messages"][0]["content"] == self._fail_query:
            raise RuntimeError("boom")
        return self._response


class _RaisingClient:
    def __init__(self, response, fail_query):
        self.messages = _RaisingMessages(response, fail_query)


def _two_row_plan():
    queries = build_queries(
        "Best {dish} in {city}", {"dish": ["sushi", "pizza"], "city": ["town"]}
    )
    return _augment_queries(
        queries,
        models=["claude-opus-4-8"],
        locations=[],
        search_tool_versions=["web_search_20250305"],
    )


def test_multi_request_calls_api_once_per_plan_row():
    plan = _two_row_plan()
    client = _CountingClient(_response_with_citations())
    _multi_request(plan, client, max_workers=4, max_uses=5)
    assert len(client.messages.calls) == len(plan)


def test_multi_request_concatenates_results():
    plan = _two_row_plan()
    client = _CountingClient(_response_with_citations())
    df = _multi_request(plan, client, max_workers=4, max_uses=5)
    # 2 plan rows x 3 citations each = 6 rows.
    assert len(df) == 6
    assert set(df["request_id"]) == set(plan["request_id"])


def test_multi_request_isolates_per_row_failures():
    plan = _two_row_plan()
    fail_query = plan["query"].iloc[0]
    client = _RaisingClient(_response_with_citations(), fail_query)
    df = _multi_request(plan, client, max_workers=4, max_uses=5)
    # The surviving row still yields its 3 citations; the failing row is not
    # dropped silently — it survives as a single logged error row (4 total).
    assert len(df) == 4
    survivors = df[df["error"].isna()]
    assert len(survivors) == 3
    assert fail_query not in set(survivors["query"])


def test_multi_request_logs_errors_in_error_column():
    plan = _two_row_plan()
    fail_query = plan["query"].iloc[0]
    client = _RaisingClient(_response_with_citations(), fail_query)
    df = _multi_request(plan, client, max_workers=4, max_uses=5)
    # An "error" column exists; successful rows are null, the failed row holds
    # the exception message and still carries its plan metadata.
    assert "error" in df.columns
    errored = df[df["error"].notna()]
    assert len(errored) == 1
    assert errored["query"].iloc[0] == fail_query
    assert "boom" in errored["error"].iloc[0]
    # Successful citation rows have no error logged.
    assert df["error"].isna().sum() == 3


def test_multi_request_empty_plan_returns_empty_frame():
    plan = _two_row_plan().iloc[0:0]
    client = _CountingClient(_response_with_citations())
    df = _multi_request(plan, client, max_workers=4, max_uses=5)
    assert len(df) == 0
    assert len(client.messages.calls) == 0


# ---------------------------------------------------------------------------
# Phase 8: serp_claude (public orchestrator)
# ---------------------------------------------------------------------------
def test_serp_claude_runs_full_pipeline():
    client = _CountingClient(_response_with_citations())
    df = serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},
        client=client,
    )
    # 2 queries x 1 model x 1 version = 2 requests, each -> 3 citations.
    assert len(client.messages.calls) == 2
    assert len(df) == 6
    # Context columns lead the frame.
    assert list(df.columns[:3]) == ["query", "dish", "city"]


def test_serp_claude_normalizes_scalar_axes():
    client = _CountingClient(_response_with_citations())
    # models / search_tool_versions passed as bare scalars, not lists.
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},
        client=client,
        models="claude-opus-4-8",
        search_tool_versions="web_search_20250305",
    )
    assert len(client.messages.calls) == 1
    assert client.messages.calls[0]["model"] == "claude-opus-4-8"


def test_serp_claude_crosses_all_axes():
    client = _CountingClient(_response_with_citations())
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},
        client=client,
        models=["claude-opus-4-8", "claude-sonnet-4-5"],
        locations=[{"country": "PT"}, {"country": "US"}],
        search_tool_versions=["web_search_20250305"],
    )
    # 2 queries x 2 models x 2 locations x 1 version = 8 requests.
    assert len(client.messages.calls) == 8


def test_serp_claude_validates_locations_before_any_api_call():
    client = _CountingClient(_response_with_citations())
    with pytest.raises(ValueError):
        serp_claude(
            "Best {dish} in {city}",
            {"dish": ["sushi"], "city": ["Lisbon"]},
            client=client,
            locations=[{"country": "PT"}, {"country": "ZZ"}],  # ZZ is invalid
        )
    # Fail-fast at $0: not a single request should have been dispatched.
    assert len(client.messages.calls) == 0


def test_serp_claude_normalizes_single_location_dict():
    client = _CountingClient(_response_with_citations())
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},
        client=client,
        locations={"country": "pt"},  # a bare dict, lower-case country
    )
    assert len(client.messages.calls) == 1
    tool = client.messages.calls[0]["tools"][0]
    # Location is validated (country upper-cased) and attached to the tool.
    assert tool["user_location"]["country"] == "PT"


def test_serp_claude_builds_client_from_api_key(monkeypatch):
    # The anthropic SDK is an optional dependency, imported lazily inside
    # serp_claude. Patch the SDK's own ``Anthropic`` (the source the lazy
    # ``from anthropic import Anthropic`` resolves) so no real client is built.
    pytest.importorskip("anthropic")

    captured = {}

    def _fake_anthropic(api_key=None):
        captured["api_key"] = api_key
        return _CountingClient(_response_with_citations())

    monkeypatch.setattr("anthropic.Anthropic", _fake_anthropic)
    df = serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},
        api_key="sk-test-123",
    )
    # api_key flows straight into the SDK constructor; pipeline still runs.
    assert captured["api_key"] == "sk-test-123"
    assert len(df) == 3


def test_serp_claude_raises_friendly_error_when_sdk_missing(monkeypatch):
    # When no client is injected and the optional ``anthropic`` package is not
    # installed, the lazy import must fail with a helpful ImportError pointing
    # at the extra — not a bare ModuleNotFoundError. Simulate "not installed"
    # by masking the module in sys.modules so the import inside serp_claude
    # raises ImportError.
    monkeypatch.setitem(sys.modules, "anthropic", None)
    with pytest.raises(ImportError, match=r"advertools\[claude\]"):
        serp_claude(
            "Best {dish} in {city}",
            {"dish": ["sushi"], "city": ["Lisbon"]},
            api_key="sk-test-123",
        )


def test_serp_claude_threads_temperature_through():
    client = _CountingClient(_response_with_citations())
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},
        client=client,
        temperature=0,
    )
    assert client.messages.calls[0]["temperature"] == 0


def test_serp_claude_omits_temperature_by_default():
    client = _CountingClient(_response_with_citations())
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},
        client=client,
    )
    assert "temperature" not in client.messages.calls[0]


# ---------------------------------------------------------------------------
# Phase 9: raw-response capture (save_raw_path) + faithfulness audit
# ---------------------------------------------------------------------------
def _response_with_orphan_citation():
    # One search returns a single result (a); Claude cites a DIFFERENT url that
    # never appeared in any SERP. Under the SERP-backbone model that citation
    # cannot get integer keys, so it is dropped — exactly the gap the audit
    # must catch.
    content = [
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "q"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [_result("https://a.com/x", "A", "May 1, 2025")],
        },
        {
            "type": "text",
            "text": "Findings.",
            "citations": [_citation("https://orphan.com/z", "Z", "ghost snippet")],
        },
    ]
    return _FakeResponse(
        {
            "id": "msg_orphan",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_save_raw_path_writes_jsonl_joinable_to_dataframe(tmp_path):
    import json

    raw_path = tmp_path / "run.jsonl"
    client = _CountingClient(_response_with_citations())
    df = serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},  # 2 requests
        client=client,
        save_raw_path=str(raw_path),
    )
    lines = raw_path.read_text().splitlines()
    # One raw JSON line per request, each valid JSON joinable to the frame by id.
    assert len(lines) == len(client.messages.calls) == 2
    raw_dumps = [json.loads(line) for line in lines]
    raw_ids = {dump["id"] for dump in raw_dumps}
    assert raw_ids == set(df["response_id"])
    # The saved object is the UNMODIFIED response dump (model_dump()).
    assert raw_dumps[0] == _response_with_citations().model_dump()


def test_save_raw_path_truncates_between_runs(tmp_path):
    raw_path = tmp_path / "run.jsonl"
    client = _CountingClient(_response_with_citations())
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},  # 2 requests
        client=client,
        save_raw_path=str(raw_path),
    )
    serp_claude(
        "Best {dish} in {city}",
        {"dish": ["sushi"], "city": ["Lisbon"]},  # 1 request
        client=_CountingClient(_response_with_citations()),
        save_raw_path=str(raw_path),
    )
    # The file mirrors the LATEST run only — no leftover lines from the first.
    assert len(raw_path.read_text().splitlines()) == 1


@pytest.mark.parametrize(
    "fixture",
    [
        _response_with_citations,
        _response_with_two_searches,
        _response_with_cited_and_uncited,
        _response_with_uncited_results,
    ],
)
def test_audit_passes_on_faithful_dataframe(fixture):
    response = fixture()
    df = _enrich_response(response, _plan_row())
    report = audit_response_coverage(df, response.model_dump())
    assert report["ok"], report["gaps"]
    # Sanity: the audit actually saw the searches/results it was checking.
    assert report["n_rows"] == report["n_results_raw"]


def test_audit_flags_orphan_citation():
    # A cited url that never appears as a search result gets dropped by the
    # enrich step; the audit must report it rather than silently bless the gap.
    response = _response_with_orphan_citation()
    df = _enrich_response(response, _plan_row())
    report = audit_response_coverage(df, response.model_dump())
    assert not report["ok"]
    assert any("orphan citation" in gap for gap in report["gaps"])


def test_audit_flags_dropped_result_row():
    # Simulate losing a result row: the audit must catch the row-count gap.
    response = _response_with_cited_and_uncited()
    df = _enrich_response(response, _plan_row()).iloc[1:]  # drop the first result
    report = audit_response_coverage(df, response.model_dump())
    assert not report["ok"]
    assert any("row count" in gap for gap in report["gaps"])


def test_audit_flags_lost_citation_provenance():
    # Regression guard: the OLD audit only substring-checked cited_text, so
    # wiping block_index/rank/rank_within_block passed silently — exactly the
    # provenance loss the @@-parallel-join fixed. The hardened audit must now
    # flag it instead of blessing the gap.
    response = _response_with_url_cited_multiple_times()
    df = _enrich_response(response, _plan_row())
    assert audit_response_coverage(df, response.model_dump())["ok"]  # faithful first
    df_lossy = df.copy()
    df_lossy["block_index"] = None
    df_lossy["rank"] = None
    df_lossy["rank_within_block"] = None
    report = audit_response_coverage(df_lossy, response.model_dump())
    assert not report["ok"]
    assert any("citation block_index mismatch" in gap for gap in report["gaps"])


def test_audit_flags_dropped_duplicate_citation():
    # A url cited 3x but reduced to one snippet (a count loss) must surface,
    # which substring containment could never catch.
    response = _response_with_url_cited_multiple_times()
    df = _enrich_response(response, _plan_row())
    df_lossy = df.copy()
    df_lossy["cited_text"] = "snippet one"  # collapsed 3 citations to 1
    report = audit_response_coverage(df_lossy, response.model_dump())
    assert not report["ok"]
    assert any("citation cited_text mismatch" in gap for gap in report["gaps"])


def _response_with_full_usage():
    # A response carrying the full real ``usage`` shape (as Anthropic returns
    # it) plus the actual served model, so we can verify every broadcast column.
    content = [
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "input": {"query": "q"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [_result("https://a.com/x", "A", "May 1, 2025")],
        },
        {"type": "text", "text": "Done."},
    ]
    return _FakeResponse(
        {
            "id": "msg_full",
            "model": "claude-opus-4-8-20260115",
            "role": "assistant",
            "type": "message",
            "container": None,
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "stop_details": None,
            "usage": {
                "input_tokens": 129702,
                "output_tokens": 3305,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "cache_creation": {
                    "ephemeral_1h_input_tokens": 0,
                    "ephemeral_5m_input_tokens": 0,
                },
                "output_tokens_details": {"thinking_tokens": 0},
                "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 4},
                "service_tier": "standard",
                "inference_geo": "global",
            },
            "content": content,
        }
    )


def test_enrich_captures_usage_and_response_meta_by_anthropic_names():
    df = _enrich_response(_response_with_full_usage(), _plan_row())
    row = df.iloc[0]
    # Response's served model is kept distinct from the requested ``model`` axis.
    assert row["model"] == "claude-opus-4-8"  # requested (from plan_row)
    assert row["response_model"] == "claude-opus-4-8-20260115"  # actually served
    # Token + billable-tool counts land under Anthropic's own dotted names,
    # flattened straight from ``usage`` by json_normalize.
    assert row["usage.input_tokens"] == 129702
    assert row["usage.output_tokens"] == 3305
    assert row["usage.cache_creation_input_tokens"] == 0
    assert row["usage.cache_read_input_tokens"] == 0
    assert row["usage.output_tokens_details.thinking_tokens"] == 0
    assert row["usage.server_tool_use.web_search_requests"] == 4
    assert row["usage.server_tool_use.web_fetch_requests"] == 0
    assert row["usage.service_tier"] == "standard"
    assert row["usage.inference_geo"] == "global"
    assert row["stop_sequence"] is None


def test_audit_passes_on_full_usage_response():
    response = _response_with_full_usage()
    df = _enrich_response(response, _plan_row())
    report = audit_response_coverage(df, response.model_dump())
    # Every broadcast column verified against the raw usage; sweep finds nothing
    # unregistered in a realistic full-usage response.
    assert report["ok"], report["gaps"]


def test_new_top_level_field_is_auto_captured():
    # The point of json_normalize: a top-level field we never anticipated is
    # flattened into its own column automatically, not silently dropped.
    raw = _response_with_full_usage().model_dump()
    raw["brand_new_field"] = "surprise"
    response = _FakeResponse(raw)
    df = _enrich_response(response, _plan_row())
    assert "brand_new_field" in df.columns
    assert set(df["brand_new_field"]) == {"surprise"}
    report = audit_response_coverage(df, response.model_dump())
    assert report["ok"], report["gaps"]


def test_new_usage_field_is_auto_captured():
    # Likewise for a brand-new nested ``usage`` leaf: it arrives as a dotted
    # column rather than vanishing.
    raw = _response_with_full_usage().model_dump()
    raw["usage"]["new_token_bucket"] = 7
    response = _FakeResponse(raw)
    df = _enrich_response(response, _plan_row())
    assert "usage.new_token_bucket" in df.columns
    assert set(df["usage.new_token_bucket"]) == {7}
    report = audit_response_coverage(df, response.model_dump())
    assert report["ok"], report["gaps"]


def test_audit_sweep_flags_unhandled_block_type():
    response = _response_with_full_usage()
    df = _enrich_response(response, _plan_row())
    raw = response.model_dump()
    raw["content"].append({"type": "thinking", "thinking": "hmm"})
    report = audit_response_coverage(df, raw)
    assert not report["ok"]
    assert any("unhandled content block type" in gap for gap in report["gaps"])


def test_audit_sweep_flags_web_search_error_block():
    response = _response_with_full_usage()
    df = _enrich_response(response, _plan_row())
    raw = response.model_dump()
    raw["content"].append(
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_err",
            "content": {
                "type": "web_search_tool_result_error",
                "error_code": "max_uses_exceeded",
            },
        }
    )
    report = audit_response_coverage(df, raw)
    assert not report["ok"]
    assert any("web_search error block" in gap for gap in report["gaps"])


def test_audit_sweep_flags_unaudited_result_field():
    response = _response_with_full_usage()
    df = _enrich_response(response, _plan_row())
    raw = response.model_dump()
    # Inject an unexpected key on a search result.
    raw["content"][1]["content"][0]["favicon"] = "http://x/icon.png"
    report = audit_response_coverage(df, raw)
    assert not report["ok"]
    assert any("unaudited result field" in gap for gap in report["gaps"])


def _response_with_code_execution():
    # Newer tool versions let Claude orchestrate searches from inside code
    # execution: a ``code_execution`` block (the Python it ran) spawns a
    # ``web_search`` whose ``caller`` points back to it, and a
    # ``code_execution_tool_result`` reports how that code finished. The
    # underlying search still returns real results.
    content = [
        {"type": "text", "text": "Let me run some code."},
        {
            "type": "server_tool_use",
            "id": "code_1",
            "name": "code_execution",
            "caller": None,
            "input": {"code": "results = await web_search({'query': 'q'})"},
        },
        {
            "type": "server_tool_use",
            "id": "srvtoolu_1",
            "name": "web_search",
            "caller": {"tool_id": "code_1", "type": "code_execution_20260120"},
            "input": {"query": "q"},
        },
        {
            "type": "web_search_tool_result",
            "tool_use_id": "srvtoolu_1",
            "content": [
                _result("https://a.com/x", "A", "May 1, 2025"),
                _result("https://b.org/y", "B", "May 2, 2025"),
            ],
        },
        {
            "type": "code_execution_tool_result",
            "tool_use_id": "code_1",
            "content": {
                "type": "encrypted_code_execution_result",
                "content": [],
                "encrypted_stdout": "OPAQUE==",
                "return_code": 1,
                "stderr": "Server tool use limit exceeded during code execution.",
            },
        },
        {"type": "text", "text": "Here is what I found."},
    ]
    return _FakeResponse(
        {
            "id": "msg_code",
            "model": "claude-opus-4-8",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 10, "output_tokens": 20},
            "content": content,
        }
    )


def test_enrich_captures_code_execution_provenance():
    df = _enrich_response(_response_with_code_execution(), _plan_row())
    assert len(df) == 2  # two results, both via the same code execution
    row = df.iloc[0]
    assert row["search_via"] == "code_execution_20260120"
    assert "await web_search" in row["search_code"]
    assert row["code_return_code"] == 1
    assert "Server tool use limit exceeded" in row["code_stderr"]


def test_enrich_direct_search_has_no_code_provenance():
    # A search Claude issued directly (caller=None) leaves the provenance
    # columns empty rather than fabricating a code execution.
    df = _enrich_response(_response_with_citations(), _plan_row())
    assert df["search_via"].isna().all()
    assert df["search_code"].isna().all()
    assert df["code_return_code"].isna().all()
    assert df["code_stderr"].isna().all()


def test_audit_passes_on_code_execution_response():
    response = _response_with_code_execution()
    df = _enrich_response(response, _plan_row())
    report = audit_response_coverage(df, response.model_dump())
    # code_execution_tool_result is now a known block type and the provenance
    # fields are registered, so a faithful frame sweeps clean.
    assert report["ok"], report["gaps"]


def test_audit_sweep_flags_unaudited_server_tool_use_field():
    # ``caller`` slipped past the old sweep because server_tool_use keys were
    # never checked; now a brand-new key on such a block is caught.
    response = _response_with_code_execution()
    df = _enrich_response(response, _plan_row())
    raw = response.model_dump()
    raw["content"][1]["surprise_field"] = "x"  # the code_execution block
    report = audit_response_coverage(df, raw)
    assert not report["ok"]
    assert any("unaudited server_tool_use field" in gap for gap in report["gaps"])


def test_audit_sweep_flags_unaudited_code_execution_field():
    response = _response_with_code_execution()
    df = _enrich_response(response, _plan_row())
    raw = response.model_dump()
    raw["content"][4]["content"]["wall_clock_ms"] = 1234  # new inner field
    report = audit_response_coverage(df, raw)
    assert not report["ok"]
    assert any("unaudited code_execution field" in gap for gap in report["gaps"])
