import os
import random
import re
from collections import Counter

import pytest
from scrapy.http import HtmlResponse, Request

from advertools.spider import (
    _extract_images,
    _filter_crawl_dict,
    _json_to_dict,
    _numbered_duplicates,
    _split_long_urllist,
    crawl,
)

jsonobj = {
    "@context": "http://schema.org",
    "@type": "NewsMediaOrganization",
    "name": "The New York Times",
    "logo": {
        "@context": "http://schema.org",
        "@type": "ImageObject",
        "url": "https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png",
        "height": 40,
        "width": 250,
    },
    "url": "https://www.nytimes.com/",
    "@id": "https://www.nytimes.com/#publisher",
    "diversityPolicy": "https://www.nytco.com/diversity-and-inclusion-at-the-new-york-times/",
    "ethicsPolicy": "https://www.nytco.com/who-we-are/culture/standards-and-ethics/",
    "masthead": "https://www.nytimes.com/interactive/2019/admin/the-new-york-times-masthead.html",
    "foundingDate": "1851-09-18",
    "sameAs": "https://en.wikipedia.org/wiki/The_New_York_Times",
}


def response_from_file(filename, url="https://example.com"):
    request = Request(url=url)
    filepath = os.path.abspath(filename)
    with open(filepath) as file:
        file_content = file.read()
        response = HtmlResponse(
            url=url, request=request, body=file_content, encoding="utf-8"
        )
    return response


def test_numbered_duplicates_returns_same_num_of_items():
    l1 = ["jan", "feb", "jan", "jan", "feb", "mar", "apr"]
    l2 = ["one", "one", "one"]
    l3 = ["one", "two", "three", "three", "three", "two"]
    for lst in [l1, l2, l3]:
        result = _numbered_duplicates(lst)
        assert len(result) == len(lst)


def test_numbered_duplicates_returns_correct_items():
    numbers = ["one", "two", "three", "four"]
    for i in range(1000):
        sample = random.choices(numbers, k=7)
        result = _numbered_duplicates(sample)
        result_split = [num.rsplit("_", 1)[0] for num in result]
        assert Counter(sample) == Counter(result_split)


def test_json_to_dict_returns_dict():
    result = _json_to_dict(jsonobj)
    assert isinstance(result, dict)
    assert all("jsonld_" in key for key in result)


def test_json_to_dict_contains_number():
    for i in range(1, 6):
        result = _json_to_dict(jsonobj, i)
        to_test = "jsonld_" + str(i) + "_"
        assert isinstance(result, dict)
        assert all(to_test in key for key in result)


def test_crawl_raises_on_wrong_file_extension():
    with pytest.raises(ValueError):
        crawl("https://example.com", "myfile.wrong", allowed_domains="example.com")


def test_split_long_urllist_correct_lengths():
    testlist = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
    result = _split_long_urllist(testlist, max_len=15)
    assert sum(len(x) for x in result) == len(testlist)
    assert all(len(x) < 15 for x in result)


def test_extract_images(html_file="tests/data/crawl_testing/test_images.html"):
    response = response_from_file(html_file)
    imgs_dict = _extract_images(response)
    for k, v in imgs_dict.items():
        assert len(v.split("@@")) == 3
    assert imgs_dict["img_src"] == "@@https://example.com/image.png@@"

    def test_numbered_duplicates_empty_list():
        result = _numbered_duplicates([])
        assert result == []


    def test_json_to_dict_empty_input():
        result = _json_to_dict({})
        assert result == {}


@pytest.fixture
def sample_dict():
    """Canonical crawl dict used by most examples."""
    return {
        "url": "https://example.com/",
        "errors": [],
        "jsonld_errors": [],
        "title": "Example Domain",
        "h1": "Example Domain",
        "h2": "Sub‑heading",
        "meta_description": "Just an example",
        "custom_key": "value",
    }


def test_filterdict_returns_original_when_no_filters(sample_dict):
    """If both keep/discard are None or empty, the function must be a no‑op."""
    original = sample_dict.copy()
    # No filters (None)
    result = _filter_crawl_dict(sample_dict, None, None)
    assert result is sample_dict
    # Explicit empty lists should behave identically
    result2 = _filter_crawl_dict(sample_dict, [], [])
    assert result2 is sample_dict
    assert sample_dict == original


@pytest.mark.parametrize(
    "patterns, expected_keys",
    [
        (["^title$"], {"title", "url", "errors", "jsonld_errors"}),
        (["^h\\d$"], {"h1", "h2", "url", "errors", "jsonld_errors"}),
        (
            ["(title|meta_description)"],
            {"title", "meta_description", "url", "errors", "jsonld_errors"},
        ),
    ],
)
def test_filterdict_keep_only(sample_dict, patterns, expected_keys):
    result = _filter_crawl_dict(sample_dict, keep_columns=patterns)
    assert set(result) == expected_keys


@pytest.mark.parametrize(
    "patterns, forbidden_keys",
    [
        (["^h\\d$"], {"h1", "h2"}),
        (["title", "meta"], {"title", "meta_description"}),
        (["custom_.*"], {"custom_key"}),
    ],
)
def test_filterdict_discard_only(sample_dict, patterns, forbidden_keys):
    result = _filter_crawl_dict(sample_dict, discard_columns=patterns)
    assert not (set(result) & set(forbidden_keys))
    for k in {"url", "errors", "jsonld_errors"}:
        assert k in result


def test_filterdict_discard_overrides_keep(sample_dict):
    keep = [r"^h\d$"]
    discard = [r"h2"]
    result = _filter_crawl_dict(sample_dict, keep, discard)
    assert "h1" in result
    assert "h2" not in result
    for k in {"url", "errors", "jsonld_errors"}:
        assert k in result


@pytest.mark.parametrize("pattern", [r"url", r"errors", r"jsonld"])
def test_filterdict_always_include_never_dropped(sample_dict, pattern):
    result = _filter_crawl_dict(sample_dict, discard_columns=[pattern])
    for k in {"url", "errors", "jsonld_errors"}:
        assert k in result


def test_filterdict_empty_input_dict_returns_empty():
    assert _filter_crawl_dict({}, keep_columns=[".*"]) == {}


def test_filterdict_invalid_regex_raises(sample_dict):
    with pytest.raises(re.error):
        _filter_crawl_dict(sample_dict, keep_columns=["["])  # invalid pattern
