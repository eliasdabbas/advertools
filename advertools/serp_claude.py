"""
.. _serp_claude:

Claude SERP Tracking at Scale
=============================

Analyze LLM / AI Search Results on a Large Scale
------------------------------------------------

``serp_claude`` tracks what Claude's web search actually surfaces for your
queries: the pages it finds, the rank they appear in, the domains it cites, and
the written ``answer`` an end user would read. Give it a query *template*, lists
of values to fill that template, and (optionally) lists of models, locations,
and tool versions; it runs every combination as its own request and returns one
tidy ``pandas.DataFrame`` — **one row per returned search result** — so you can
analyze AI search results across queries, models, and locations at scale. It is
the AI-search counterpart to advertools' :func:`serp_youtube`.

What you can do with it:

- See **which pages and domains Claude surfaces** (and cites) for a query, the
  way you would track a Google SERP — but for AI search / answer engines.
- Read the **answer** Claude gives the user, alongside the URLs it cited to
  build that answer.
- **Compare across models and locations** — does the answer or the set of cited
  sources change by model, country, or city?
- Track **search activity in your runs** (for example via
    ``usage.server_tool_use.web_search_requests``), and which sources it leans on.

How the matrix is built
-----------------------

The number of requests is the **full Cartesian product** of four axes::

    queries  ×  models  ×  locations  ×  search_tool_versions

The ``queries`` axis is itself a product: ``query_template`` is expanded over
every combination of the ``variables`` you pass. So if you give two variables
with 3 and 2 values, you get ``3 × 2 = 6`` queries, and *those* are then crossed
with the remaining axes. This grows fast — see the note on cost below.

For example, this template plus variables::

    import advertools as adv

    query_template = "best {dish} restaurants in {city}"
    variables = {"dish": ["sushi", "pizza"], "city": ["Lisbon", "Porto"]}

expands to ``2 × 2 = 4`` queries. The :func:`build_queries` helper does exactly
this and returns them as a DataFrame, with a ``query`` column plus one column
per variable (so you can see precisely which query maps to which values)::

    from advertools.serp_claude import build_queries

    build_queries(query_template, variables)

                                  query   dish    city
    0  best sushi restaurants in Lisbon  sushi  Lisbon
    1   best sushi restaurants in Porto  sushi   Porto
    2  best pizza restaurants in Lisbon  pizza  Lisbon
    3   best pizza restaurants in Porto  pizza   Porto

Cross those 4 queries with, say, 2 models and 1 location and you get
``4 × 2 × 1 = 8`` requests, each producing several result rows.

Installation & authentication
-----------------------------

The official ``anthropic`` SDK is an *optional* dependency. Install it with::

    pip install "advertools[claude]"     # or: pip install anthropic

The SDK is imported lazily — only when ``serp_claude`` actually builds a client
— so importing advertools never requires it. Authenticate by passing
``api_key=...`` or by setting the ``ANTHROPIC_API_KEY`` environment variable.

Examples
--------

The simplest case — a single, literal query (pass an empty ``variables``)::

    import advertools as adv

    df = adv.serp_claude("best running shoes 2026", {})

See which domains Claude cited most for that query::

    df[df["cited_text"].notna()]["domain"].value_counts()

Read the answer Claude gave the user (the same for every row of a request)::

    print(df["answer"].iloc[0])

A templated query expanded over one variable (3 requests)::

    df = adv.serp_claude(
        "best {sport} shoes 2026",
        {"sport": ["running", "trail", "tennis"]},
    )

Crossing multiple variables and two models (``2 dishes × 1 city × 2 models =
4`` requests)::

    df = adv.serp_claude(
        "best {dish} in {city}",
        {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},
        models=["claude-opus-4-8", "claude-sonnet-4-5"],
    )

Localizing the search with one or more ``user_location`` dicts::

    df = adv.serp_claude(
        "top wedding photographers",
        {},
        locations=[
            {"country": "PT", "city": "Lisbon", "timezone": "Europe/Lisbon"},
            {"country": "US", "city": "Seattle", "timezone": "America/Los_Angeles"},
        ],
    )

The result DataFrame
--------------------

Every row is one returned search result. The frame is wide (template variables,
result fields, citation provenance, and per-request/response metadata are all
broadcast onto each row), so here is an **abridged** view of the most useful
columns::

       query        serp_rank  title          domain         cited_text
    0  best sushi…          1  Sushi Lisboa…  sushilisboa.…  "ranked #1 for…"
    1  best sushi…          2  Confraria Su…  confraria.pt   NaN
    2  best sushi…          3  Go Juu…        gojuu.pt       "known for oma…"

Full column inventory
---------------------

.. csv-table::
   :header: "category", "column name", "description"

   "Query context", "query", "Rendered prompt sent to Claude for this request row."
   "Query context", "<template variables>", "One column per template variable (for example dish, city), copied to every result row from that request."
   "Search result identity", "serp_rank", "Position of a URL within one search result set (1 = top). Resets for each search."
   "Search result identity", "title", "Result title returned by the web search tool."
   "Search result identity", "url", "Result URL returned by the web search tool."
   "Search result identity", "domain", "Hostname parsed from url for domain-level analysis."
   "Search result identity", "page_age", "Page recency string returned by the tool, when available."
   "Search provenance", "search_index", "Which search within this request produced the row (1..N); one request can trigger multiple searches."
   "Search provenance", "search_query", "Query string Claude actually issued to the tool for that search."
   "Search provenance", "search_via", "Caller type when search was orchestrated by code execution; None for direct searches."
   "Search provenance", "search_code", "Code snippet Claude executed when search_via indicates code execution."
   "Search provenance", "code_return_code", "Return code from the related code execution block, if applicable."
   "Search provenance", "code_stderr", "Stderr from the related code execution block, if applicable."
   "Citation", "cited_text", "Snippet Claude quoted from this URL in its answer; NaN means returned but not cited."
   "Citation", "block_index", "Answer text-block index where each citation appears; repeated citations are @@-joined."
   "Citation", "rank_within_block", "Citation order inside one answer block (1..M); repeated citations are @@-joined."
   "Citation", "rank", "Global citation order across the full answer narrative (not SERP rank); repeated citations are @@-joined."
   "Request metadata", "request_id", "Internal id for one matrix row/API call."
   "Request metadata", "model", "Model requested by the plan axis."
   "Request metadata", "tool_version", "Web search tool version requested by the plan axis."
   "Request metadata", "loc_city", "Location city from the input locations axis."
   "Request metadata", "loc_region", "Location region from the input locations axis."
   "Request metadata", "loc_country", "Location country (ISO alpha-2, normalized/validated)."
   "Request metadata", "loc_timezone", "Location timezone (IANA tz id, validated)."
   "Response", "answer", "Claude's written answer text (what the end user reads), broadcast to all rows from one response."
   "Response", "retrieved_at", "UTC timestamp when the response was processed."
   "Response", "response_id", "Anthropic message id for joining with raw JSONL dumps."
   "Response", "response_model", "Model id Anthropic actually served (can differ from the requested alias in model)."
   "Response", "stop_reason", "Anthropic stop reason for the response."
   "Response", "stop_sequence", "Anthropic stop sequence value, when set."
   "Usage telemetry", "usage.cache_creation.ephemeral_1h_input_tokens", "Cache-creation tokens in the 1h bucket."
   "Usage telemetry", "usage.cache_creation.ephemeral_5m_input_tokens", "Cache-creation tokens in the 5m bucket."
   "Usage telemetry", "usage.cache_creation_input_tokens", "Total cache-creation input tokens."
   "Usage telemetry", "usage.cache_read_input_tokens", "Input tokens read from cache."
   "Usage telemetry", "usage.inference_geo", "Inference region reported by Anthropic."
   "Usage telemetry", "usage.input_tokens", "Input token count for the response."
   "Usage telemetry", "usage.output_tokens", "Output token count for the response."
   "Usage telemetry", "usage.output_tokens_details.thinking_tokens", "Thinking token count, if reported."
   "Usage telemetry", "usage.server_tool_use.web_fetch_requests", "Number of web fetch calls used by server tools."
   "Usage telemetry", "usage.server_tool_use.web_search_requests", "Number of web search calls used by server tools in the response."
   "Usage telemetry", "usage.service_tier", "Service tier reported for the response."
   "Error logging", "error", "None for successful rows; exception text for failed request rows that are logged instead of dropped."
A note on forcing searches: there is no ``tool_choice`` for the server-side
web_search tool, so a search cannot be hard-forced — the documented levers are
the system prompt (soft) and ``max_uses`` (a ceiling, not a floor).

.. note::

    **Cost / size.** The number of API calls is the full Cartesian product
    ``len(queries) × len(models) × max(len(locations), 1) × len(versions)``,
    and ``len(queries)`` is itself the product of every variable's value count.
    Each request may run up to ``max_uses`` web searches, billed by Anthropic
    (web search is roughly $10 / 1,000 searches, plus token costs). Inspect the
    plan size before launching a large matrix — there is intentionally no hard
    cap.
"""  # noqa: E501

from __future__ import annotations

import itertools
import json
import os
import threading
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from string import Formatter
from urllib.parse import urlparse

import pandas as pd
import zoneinfo

# ISO 3166-1 alpha-2 country codes (all 249), embedded to avoid a runtime
# dependency. Source: en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
_ISO_3166_1_ALPHA2 = frozenset(
    """
    AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ
    BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR
    CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR
    GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU
    ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ
    LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ
    MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF
    PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI
    SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR
    TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW
    """.split()
)


def _validate_location(location):
    """Validate and normalize a single ``user_location`` dict.

    Returns a NEW dict (never mutates the caller's) with:

    - ``type`` forced to ``"approximate"`` (the only value the API accepts).
    - ``country`` (optional) upper-cased and checked against ISO 3166-1
      alpha-2 codes -> ``ValueError`` if unknown.
    - ``timezone`` (optional) checked against the IANA tz database via
      ``zoneinfo`` -> ``ValueError`` if unknown.

    Other keys (``city``, ``region``) pass through untouched.
    """
    if not isinstance(location, dict):
        raise TypeError(f"location must be a dict, got {type(location).__name__}")

    out = dict(location)
    out["type"] = "approximate"

    country = out.get("country")
    if country is not None:
        normalized = str(country).upper()
        if normalized not in _ISO_3166_1_ALPHA2:
            raise ValueError(
                f"Invalid country {country!r}: expected an ISO 3166-1 alpha-2 "
                f"code (e.g. 'US', 'FR', 'DE')."
            )
        out["country"] = normalized

    timezone = out.get("timezone")
    if timezone is not None and timezone not in zoneinfo.available_timezones():
        raise ValueError(
            f"Invalid timezone {timezone!r}: expected an IANA tz id "
            f"(e.g. 'Europe/Lisbon', 'America/Los_Angeles')."
        )

    return out


def _build_search_tool(version, location=None, max_uses=5):
    """Assemble the ``web_search`` tool schema for one request.

    A dumb assembler: it trusts ``location`` to be already validated (the
    request plan is validated upfront by ``serp_claude``). When ``location``
    is ``None`` the ``user_location`` key is omitted entirely.

    - ``version``: the tool version string, e.g. ``"web_search_20250305"`` or
      ``"web_search_20260209"``; becomes the tool ``type``.
    - ``location``: an optional validated ``user_location`` dict (embedded as a
      copy so the tool is independent of the caller's dict).
    - ``max_uses``: cap on searches per request.
    """
    tool = {
        "type": version,
        "name": "web_search",
        "max_uses": max_uses,
    }
    if location is not None:
        tool["user_location"] = dict(location)
    return tool


def _as_list(value):
    """Normalize a scalar-or-list parameter into a list.

    - ``None`` -> ``[]`` so callers can iterate over "absent" safely.
    - ``str``/``bytes`` -> ``[value]``: iterable, but a single scalar value.
    - ``dict`` -> ``[value]``: a dict is a single unit (e.g. one location),
      never iterated into its keys.
    - any other iterable (``list``, ``tuple``, ``set``, ``pandas.Series``,
      ``numpy.ndarray``, generators, ...) -> a new ``list`` of its items.
    - any remaining scalar -> ``[value]``.
    """
    if value is None:
        return []
    if isinstance(value, (str, bytes, dict)):
        return [value]
    if isinstance(value, Iterable):
        return list(value)
    return [value]


def build_queries(query_template: str, variables: dict[str, list]) -> pd.DataFrame:
    """Expand a template into the Cartesian product of its variables.

    ``query_template`` placeholders must match ``variables`` keys exactly (in
    both directions) or a ``ValueError`` is raised. Returns a DataFrame with a
    ``query`` column plus one column per variable.
    """
    placeholders = {name for _, name, _, _ in Formatter().parse(query_template) if name}
    keys = set(variables)
    if placeholders != keys:
        raise ValueError(
            f"Template placeholders {placeholders} must match "
            f"variables keys {keys}. "
            f"Missing: {placeholders - keys}. Extra: {keys - placeholders}."
        )

    names = list(variables.keys())
    queries = []
    for combo in itertools.product(*(variables[n] for n in names)):
        combo_dict = dict(zip(names, combo))
        queries.append({"query": query_template.format(**combo_dict), **combo_dict})

    return pd.json_normalize(queries)


# Location dict fields that get flattened onto the request plan as ``loc_*``.
_LOCATION_FIELDS = ("city", "region", "country", "timezone")


def _augment_queries(queries, models, locations, search_tool_versions) -> pd.DataFrame:
    """Cross a queries frame with the execution axes into a request plan.

    Produces one row per ``(query x model x location x tool_version)``
    combination — i.e. one row per API call. Pure combinatorics over plain
    values; no API objects are constructed here.

    - ``models`` / ``search_tool_versions``: lists of scalars, each an
      independent axis.
    - ``locations``: a list of (already validated) location dicts, each treated
      as a single unit so its components never get mixed across rows. Flattened
      onto ``loc_city``, ``loc_region``, ``loc_country``, ``loc_timezone``. An
      empty list means "no location" -> one row per query, with ``None`` in the
      ``loc_*`` columns. The full dict is also kept in ``location`` for
      downstream request construction.

    Adds a unique ``request_id`` per row.
    """
    # An empty location axis still yields one combination (the "no location").
    location_axis = list(locations) if locations else [None]

    rows = []
    for query_row in queries.to_dict("records"):
        for model, location, version in itertools.product(
            models, location_axis, search_tool_versions
        ):
            row = dict(query_row)
            row["model"] = model
            row["tool_version"] = version
            row["location"] = location
            for field in _LOCATION_FIELDS:
                row[f"loc_{field}"] = location.get(field) if location else None
            rows.append(row)

    plan = pd.DataFrame(rows)
    plan.insert(0, "request_id", range(len(plan)))
    return plan


# Plan-row keys that are request-construction details, not result metadata.
_PLAN_INTERNAL_KEYS = ("location",)

# Top-level response keys we deliberately do NOT broadcast as metadata columns:
# - role: constant "assistant"     - container: container/code-exec API only (null)
# - type: constant "message"       - stop_details: redundant with stop_reason
# - content: routed to the custom SERP-row loop, never flattened here
_RESPONSE_DENYLIST = frozenset({"role", "type", "container", "stop_details", "content"})

# Response keys that collide with existing user-facing columns -> disambiguate
# (our ``model`` is the requested axis; ``query``/``request_id`` are ours too).
_RESPONSE_RENAMES = {"id": "response_id", "model": "response_model"}


def _response_meta(dump):
    """Flatten a response's top-level metadata into one tidy row of columns.

    Rather than hand-pick fields (brittle, and silently drops whatever Anthropic
    adds next), this lets :func:`pandas.json_normalize` flatten everything except
    ``content`` into dotted leaf columns (``usage.input_tokens``,
    ``usage.server_tool_use.web_search_requests``, ...), drops a small denylist
    of constant/empty/redundant keys, and renames the two that collide with our
    own columns (``id`` -> ``response_id``, ``model`` -> ``response_model``).

    Returns a single-row DataFrame; the caller broadcasts it onto the SERP rows.
    """
    top_level = {k: v for k, v in dump.items() if k not in _RESPONSE_DENYLIST}
    meta = pd.json_normalize(top_level)
    meta = meta.drop(columns=[c for c in _RESPONSE_DENYLIST if c in meta.columns])
    return meta.rename(columns=_RESPONSE_RENAMES)


# Plan-row keys that are pipeline structure, not user-supplied template
# variables. Everything else in a plan row came from the query template.
_STRUCTURAL_PLAN_KEYS = frozenset(
    {
        "request_id",
        "query",
        "model",
        "tool_version",
        "location",
        "loc_city",
        "loc_region",
        "loc_country",
        "loc_timezone",
    }
)


def _lead_with_query_and_variables(df, plan_row) -> pd.DataFrame:
    """Reorder columns so ``query`` and the template variables come first.

    Readers see the context (what was asked and which variable values it
    covers) before the citation/result columns. Remaining columns keep their
    existing order.
    """
    variables = [key for key in plan_row if key not in _STRUCTURAL_PLAN_KEYS]
    lead = [col for col in ["query", *variables] if col in df.columns]
    rest = [col for col in df.columns if col not in lead]
    return df[lead + rest]


def _query_map(content) -> dict:
    """Map each ``server_tool_use`` block's id to the query Claude issued.

    The web-search response interleaves ``server_tool_use`` blocks (each
    carrying the actual search string in ``input.query`` and a unique ``id``)
    with ``web_search_tool_result`` blocks that reference that id via
    ``tool_use_id``. This map lets every result row be tied back to the exact
    query that produced it. Returns ``{}`` when no searches were performed.
    """
    return {
        block["id"]: block.get("input", {}).get("query")
        for block in content
        if block.get("type") == "server_tool_use" and block.get("id")
    }


def _caller_map(content) -> dict:
    """Map each ``web_search`` block's id to its ``caller`` (or ``None``).

    Newer tool versions let Claude issue searches from *inside* code execution.
    When it does, the ``web_search`` ``server_tool_use`` block carries a
    ``caller`` — ``{"tool_id": <code-execution id>, "type": <code-exec
    version>}`` — pointing back to the code block that spawned it. A search
    Claude issued directly has ``caller`` set to ``None``. This map lets every
    result row record *how* its search was issued.
    """
    return {
        block["id"]: block.get("caller")
        for block in content
        if block.get("type") == "server_tool_use"
        and block.get("name") == "web_search"
        and block.get("id")
    }


def _code_execution_map(content):
    """Map code-execution ids to the code Claude ran and that run's outcome.

    Returns ``(code_by_id, result_by_id)``:

    - ``code_by_id``: a ``code_execution`` ``server_tool_use`` id -> the Python
      ``input.code`` Claude wrote and ran.
    - ``result_by_id``: a ``code_execution_tool_result``'s ``tool_use_id`` ->
      ``(return_code, stderr)`` from its inner content (the opaque
      ``encrypted_stdout`` is deliberately dropped, like the other
      ``encrypted_*`` blobs).

    Together with :func:`_caller_map` these let a search result be traced back
    to the code that orchestrated it and whether that code succeeded.
    """
    code_by_id = {
        block["id"]: block.get("input", {}).get("code")
        for block in content
        if block.get("type") == "server_tool_use"
        and block.get("name") == "code_execution"
        and block.get("id")
    }
    result_by_id = {}
    for block in content:
        if block.get("type") != "code_execution_tool_result":
            continue
        inner = block.get("content") or {}
        result_by_id[block.get("tool_use_id")] = (
            inner.get("return_code"),
            inner.get("stderr"),
        )
    return code_by_id, result_by_id


def _enrich_response(response, plan_row) -> pd.DataFrame:
    """Turn one API response into a tidy SERP DataFrame.

    The frame's backbone is the search results themselves: **one row per
    returned result**, located by two integers that together pin it down:

    - ``search_index`` — *which* search within this request (1..N). One request
      can trigger several searches; this identifies the SERP.
    - ``serp_rank`` — the result's position *within that one search* (1..M,
      1 = top hit). It RESETS to 1 at the start of every search.

    Each row also carries ``title``, ``url``, ``domain``, ``page_age`` and the
    ``search_query`` Claude actually issued. When Claude orchestrated the search
    from *inside* code execution (newer tool versions), the row also records the
    provenance: ``search_via`` (the code-execution version, else ``None`` for a
    direct search), ``search_code`` (the Python Claude ran), and that run's
    ``code_return_code`` / ``code_stderr``. Results Claude quoted in its
    written answer are enriched with the snippet (``cited_text``) and its
    provenance in the answer (``block_index``, ``rank_within_block``, global
    ``rank``); uncited results leave those as NaN, so ``cited_text.notna()``
    flags "was this quoted?".

    A URL returned by more than one search becomes one row per search (each with
    its own integer ``serp_rank``/``search_index``). A URL quoted with several
    snippets keeps EVERY citation: ``cited_text`` and its three provenance
    fields (``block_index``, ``rank_within_block``, ``rank``) are each
    ``@@``-joined in parallel, so the snippet and its location stay aligned and
    a single ``.str.split("@@").explode()`` (across all four) round-trips the
    full citation-level frame losslessly. (Those four are therefore strings when
    cited; ``serp_rank``/``search_index`` stay integers — they are genuinely
    one value per row.) Plan-row metadata and response usage are broadcast onto
    every row.

    Response-level metadata is broadcast onto every row by flattening the raw
    response (everything except ``content``) with :func:`pandas.json_normalize`,
    so fields arrive under Anthropic's own dotted names and new ones are captured
    automatically (see :func:`_response_meta`):

    - ``response_id`` / ``response_model`` — the response's ``id`` and the model
      Anthropic actually served (renamed to avoid colliding with the requested
      ``model`` axis, which an alias may resolve to a dated id).
    - ``usage.input_tokens`` / ``usage.output_tokens``, the prompt-cache split
      ``usage.cache_creation_input_tokens`` / ``usage.cache_read_input_tokens``,
      and ``usage.output_tokens_details.thinking_tokens``.
    - ``usage.server_tool_use.web_search_requests`` /
      ``usage.server_tool_use.web_fetch_requests`` — billable tool counts.
    - ``usage.service_tier`` / ``usage.inference_geo`` / ``stop_reason`` /
      ``stop_sequence``.

    Plus two computed columns: ``answer`` (the concatenated text blocks) and
    ``retrieved_at`` (our fetch timestamp).

    Web-search errors (``web_search_tool_result_error``) are soft-handled: they
    contribute no rows rather than raising. A response with no search results
    yields an empty DataFrame.
    """
    dump = response.model_dump()
    content = dump.get("content", [])
    queries = _query_map(content)
    callers = _caller_map(content)
    code_by_id, code_results = _code_execution_map(content)

    # Citation lookup: url -> list of citations (in answer order), each with the
    # quoted snippet and where it sat in the answer. Used to enrich the matching
    # SERP row(s) below.
    cited = {}
    global_rank = 0
    for block_index, block in enumerate(content):
        for rank_within_block, citation in enumerate(
            block.get("citations") or [], start=1
        ):
            global_rank += 1
            cited.setdefault(citation.get("url"), []).append(
                {
                    "cited_text": citation.get("cited_text"),
                    "block_index": block_index,
                    "rank_within_block": rank_within_block,
                    "rank": global_rank,
                }
            )
    has_citations = bool(cited)

    # SERP rows: the backbone. One row per returned result, with integer
    # search_index (which search) and serp_rank (position within that search).
    rows = []
    search_index = 0
    for block in content:
        if block.get("type") != "web_search_tool_result":
            continue
        results = block.get("content")
        if not isinstance(results, list):
            continue  # error blocks carry a dict, not a list of results
        search_index += 1
        search_query = queries.get(block.get("tool_use_id"))
        # Provenance: was this search issued directly, or orchestrated by code
        # Claude wrote? ``caller`` is None for a direct search; otherwise it
        # points back to the code-execution block that spawned it.
        caller = callers.get(block.get("tool_use_id"))
        search_via = caller.get("type") if caller else None
        code_id = caller.get("tool_id") if caller else None
        search_code = code_by_id.get(code_id)
        code_return_code, code_stderr = code_results.get(code_id, (None, None))
        for serp_rank, result in enumerate(results, start=1):
            url = result.get("url")
            row = {
                "serp_rank": serp_rank,
                "title": result.get("title"),
                "url": url,
                "domain": urlparse(url).netloc if url else None,
            }
            # Keep cited_text adjacent to the result identity, but only
            # introduce the column when the response cited anything at all.
            if has_citations:
                row["cited_text"] = None
            row["page_age"] = result.get("page_age")
            row["search_query"] = search_query
            row["search_via"] = search_via
            row["search_code"] = search_code
            row["code_return_code"] = code_return_code
            row["code_stderr"] = code_stderr
            row["search_index"] = search_index
            citations = cited.get(url)
            if citations:
                # A URL can be cited many times (different snippets, different
                # places in the answer). Keep EVERY citation losslessly by
                # ``@@``-joining all four citation-level fields IN PARALLEL, so
                # one ``.str.split("@@").explode()`` round-trips the full
                # citation-level frame with text and provenance still aligned.
                # All four iterate the SAME ``citations`` with no filtering, so
                # the columns stay positionally aligned (a missing snippet
                # becomes "" rather than shifting the others). ``serp_rank`` /
                # ``search_index`` stay integers — genuinely one-per-row.
                row["cited_text"] = "@@".join(
                    (c["cited_text"] or "") for c in citations
                )
                row["block_index"] = "@@".join(str(c["block_index"]) for c in citations)
                row["rank_within_block"] = "@@".join(
                    str(c["rank_within_block"]) for c in citations
                )
                row["rank"] = "@@".join(str(c["rank"]) for c in citations)
            rows.append(row)

    df = pd.DataFrame(rows)

    # Broadcast plan-row metadata (skip request-construction-only keys).
    for key, value in plan_row.items():
        if key in _PLAN_INTERNAL_KEYS:
            continue
        df[key] = [value] * len(df) if len(df) else pd.Series(dtype="object")

    # Response metadata: flatten everything (minus denylist) straight from the
    # dump, so new API fields are captured automatically instead of hand-picked.
    answer = "".join(
        block.get("text", "") for block in content if block.get("type") == "text"
    )
    computed = {
        "answer": answer,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    meta = _response_meta(dump)
    for key, value in {**computed, **meta.iloc[0].to_dict()}.items():
        df[key] = [value] * len(df) if len(df) else pd.Series(dtype="object")

    return _lead_with_query_and_variables(df, plan_row)


def _single_request(
    plan_row,
    client,
    max_uses=5,
    max_tokens=10000,
    temperature=None,
    save_raw_path=None,
    write_lock=None,
) -> pd.DataFrame:
    """Execute one request-plan row against the API and enrich the result.

    Builds the user message from ``plan_row["query"]`` and the versioned
    ``web_search`` tool (with ``user_location`` when the row has a location),
    calls ``client.messages.create(...)`` and runs the response through
    :func:`_enrich_response`. The result is sorted into SERP order
    (``search_index`` then ``serp_rank``) with a fresh index, so each
    per-request frame is clean and self-contained.

    ``temperature`` is omitted from the request unless explicitly set: newer
    models manage their own sampling and reject the parameter, while older
    models still honor it (e.g. ``temperature=0`` for deterministic results).

    When ``save_raw_path`` is set, the raw ``response.model_dump()`` is appended
    as one JSON line *before* enrichment — so the source of truth is captured
    even if parsing has a bug. ``write_lock`` (an internal
    :class:`threading.Lock`, supplied by :func:`_multi_request`) serializes the
    append so concurrent workers never interleave lines; callers other than
    ``_multi_request`` leave it ``None``.
    """
    tool = _build_search_tool(
        plan_row["tool_version"],
        location=plan_row.get("location"),
        max_uses=max_uses,
    )
    kwargs = {
        "model": plan_row["model"],
        "messages": [{"role": "user", "content": plan_row["query"]}],
        "tools": [tool],
        "max_tokens": max_tokens,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    response = client.messages.create(**kwargs)
    if save_raw_path is not None:
        _save_raw_response(response, save_raw_path, write_lock)
    df = _enrich_response(response, plan_row)
    # Present each request's results in SERP order — by search, then rank within
    # it — and renumber the index so every per-request frame is self-contained.
    if {"search_index", "serp_rank"}.issubset(df.columns):
        df = df.sort_values(["search_index", "serp_rank"]).reset_index(drop=True)
    return df


def _multi_request(
    plan,
    client,
    max_workers=8,
    max_uses=5,
    max_tokens=10000,
    temperature=None,
    save_raw_path=None,
) -> pd.DataFrame:
    """Run every plan row through :func:`_single_request` concurrently.

    Each row is dispatched to a thread pool. Per-row failures are isolated and
    *logged, not dropped*: a request that raises becomes a single row carrying
    the plan metadata plus the exception message in an ``error`` column, so the
    caller sees both successful and failed requests in one honest frame.
    Successful citation rows have ``error`` set to ``None``. An empty plan
    yields an empty frame.

    When ``save_raw_path`` is set, the file is truncated once up front, then
    each worker appends its raw response as one JSON line under a shared lock
    (so concurrent writes never interleave). The resulting ``.jsonl`` fully
    represents this run.
    """
    rows = plan.to_dict("records")
    if not rows:
        return pd.DataFrame()

    write_lock = None
    if save_raw_path is not None:
        # Truncate once so the file mirrors exactly this run, then let workers
        # append their own line under the lock.
        open(save_raw_path, "w").close()
        write_lock = threading.Lock()

    def _run(plan_row):
        try:
            df = _single_request(
                plan_row,
                client,
                max_uses,
                max_tokens,
                temperature,
                save_raw_path=save_raw_path,
                write_lock=write_lock,
            )
            df["error"] = None
            return df
        except Exception as exc:  # noqa: BLE001 — log any failure, don't crash the batch
            return _error_frame(plan_row, exc)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        frames = list(executor.map(_run, rows))

    return pd.concat(frames, ignore_index=True)


def _save_raw_response(response, path, write_lock=None):
    """Append one raw response (``model_dump()``) to ``path`` as a JSON line.

    ``default=str`` keeps the dump faithful even if it carries non-JSON-native
    values (e.g. datetimes). The optional ``write_lock`` serializes concurrent
    appends from the thread pool so lines never interleave; a fresh open/close
    per line means a crash mid-run still leaves valid JSONL of all completed
    requests.
    """
    line = json.dumps(response.model_dump(), default=str) + "\n"
    lock = write_lock or threading.Lock()
    with lock:
        with open(path, "a") as handle:
            handle.write(line)


def _error_frame(plan_row, exc) -> pd.DataFrame:
    """Build a one-row frame logging a failed request.

    Broadcasts the plan-row metadata (skipping request-construction-only keys)
    and records the exception message in the ``error`` column.
    """
    meta = {
        key: value for key, value in plan_row.items() if key not in _PLAN_INTERNAL_KEYS
    }
    meta["error"] = f"{type(exc).__name__}: {exc}"
    meta["retrieved_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return _lead_with_query_and_variables(pd.DataFrame([meta]), plan_row)


def serp_claude(
    query_template: str,
    variables: dict[str, list],
    *,
    api_key=None,
    client=None,
    models="claude-opus-4-8",
    locations=None,
    search_tool_versions="web_search_20250305",
    max_uses=5,
    max_tokens=10000,
    max_workers=8,
    temperature=None,
    save_raw_path=None,
) -> pd.DataFrame:
    """Get SERP-style results from Claude's web search across an input matrix.

    Expands ``query_template`` over ``variables`` and crosses the resulting
    queries with every ``model × location × search_tool_version`` combination,
    running each combination as one concurrent request. Returns a tidy
    DataFrame with one row per returned search result; failed requests are
    logged in an ``error`` column rather than dropped. See the module
    documentation for the full description, the result-column reference, and
    more examples.

    Parameters
    ----------
    query_template : str
        The query to send, with optional ``{placeholder}`` fields that must
        match the keys of ``variables`` exactly. Use a plain string with no
        placeholders (and ``variables={}``) for a single literal query.
    variables : dict
        Mapping of placeholder name to a list of values. The template is
        expanded over the Cartesian product of these values (e.g.
        ``{"dish": ["sushi", "ramen"], "city": ["Lisbon"]}`` yields two
        queries). Pass an empty dict ``{}`` when the template has no
        placeholders.
    api_key : str, optional
        Anthropic API key. If omitted, it is read from the
        ``ANTHROPIC_API_KEY`` environment variable. A ``ValueError`` is raised
        if neither is provided and no ``client`` is given.
    client : anthropic.Anthropic, optional
        A pre-configured Anthropic client (custom timeout, base_url, retries,
        ...). Takes precedence over ``api_key``. Most users can leave this
        ``None`` and let the function build one.
    models : str or list of str, default "claude-opus-4-8"
        One or more model ids to run every query against (an axis of the
        matrix).
    locations : dict or list of dict, optional
        One or more ``user_location`` dicts to localize the search, or ``None``
        for no location. Each dict may contain ``city``, ``region``,
        ``country`` (ISO 3166-1 alpha-2), and ``timezone`` (IANA tz id); all
        are validated upfront. Each dict is treated as a single unit, never
        mixed across rows.
    search_tool_versions : str or list of str, default "web_search_20250305"
        One or more ``web_search`` tool version strings (an axis of the matrix).
    max_uses : int, default 5
        Maximum number of web searches Claude may run per request (a ceiling,
        not a floor).
    max_tokens : int, default 10000
        Maximum tokens for each response.
    max_workers : int, default 8
        Number of concurrent requests.
    temperature : float, optional
        Sampling temperature. Omitted from the request unless set; newer models
        reject it, while older models honor it (e.g. ``0`` for deterministic
        output).
    save_raw_path : str, optional
        Path to a ``.jsonl`` file. When set, each successful request's raw,
        unmodified response (``response.model_dump()``) is appended as one JSON
        line, joinable back to the DataFrame by ``id`` (the ``response_id``
        column). The file is truncated once at the start of the call.

    Returns
    -------
    pandas.DataFrame
        One row per returned search result, with the template variables, result
        fields (``serp_rank``, ``title``, ``url``, ``domain``, ``page_age``),
        the ``search_query`` Claude issued, any quoted ``cited_text``, Claude's
        ``answer``, per-request/response metadata (``model``, location columns,
        ``usage.*`` token counts, ``response_id``), and an ``error`` column
        (``None`` on success). See the module documentation for the full column
        reference.

    Raises
    ------
    ValueError
        If a location is invalid, if template placeholders do not match
        ``variables`` keys, or if no API key is found and no ``client`` given.
    ImportError
        If the optional ``anthropic`` package is not installed and no ``client``
        is provided. Install it with ``pip install "advertools[claude]"``.

    Examples
    --------
    A single, literal query::

        import advertools as adv

        df = adv.serp_claude("best running shoes 2026", {})

    A templated query expanded over one variable (3 requests)::

        df = adv.serp_claude(
            "best {sport} shoes 2026",
            {"sport": ["running", "trail", "tennis"]},
        )

    Crossing two variables and two models (``2 × 1 × 2 = 4`` requests)::

        df = adv.serp_claude(
            "best {dish} in {city}",
            {"dish": ["sushi", "ramen"], "city": ["Lisbon"]},
            models=["claude-opus-4-8", "claude-sonnet-4-5"],
        )

    .. note::

        The number of API calls is the full Cartesian product
        ``len(queries) × len(models) × max(len(locations), 1) × len(versions)``
        and each request may run up to ``max_uses`` billed web searches. Inspect
        the matrix size before launching a large run.
    """
    if client is None:
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "No API key found. Pass api_key=... or set the "
                "ANTHROPIC_API_KEY environment variable."
            )
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ImportError(
                "serp_claude requires the 'anthropic' package. Install it with: "
                'pip install "advertools[claude]"  (or: pip install anthropic)'
            ) from exc
        client = Anthropic(api_key=key)

    models = _as_list(models)
    versions = _as_list(search_tool_versions)
    # Validate every location upfront (the single fail-fast-at-$0 gate).
    locations = [_validate_location(loc) for loc in _as_list(locations)]

    queries = build_queries(query_template, variables)
    plan = _augment_queries(queries, models, locations, versions)
    return _multi_request(
        plan,
        client,
        max_workers=max_workers,
        max_uses=max_uses,
        max_tokens=max_tokens,
        temperature=temperature,
        save_raw_path=save_raw_path,
    )
