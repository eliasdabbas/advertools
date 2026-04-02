from pathlib import Path

import pandas as pd
import pytest

from advertools.sitemaps import _build_request_headers, sitemap_to_df
from advertools.sitemaps import headers as DEFAULT_HEADERS

gh_test_data_folder = "https://raw.githubusercontent.com/eliasdabbas/advertools/master/tests/data/sitemap_testing/"
offline_test_data_folder = "tests/data/sitemap_testing/"


def full_path(file):
    return gh_test_data_folder + file


def offline_path(filename):
    path = Path(offline_test_data_folder + filename)
    return path.absolute().as_uri()


regular_sitemap_url = full_path("regular_sitemap.xml")
zipped_sitemap_url = full_path("zipped_sitemap.xml.gz")
zipped_butnot_sitemap_url = offline_path("regular_sitemap.xml.gz")
sitemap_index_url = full_path("sitemap_index.xml")
error_sitemap_url = full_path("error_sitemap.xml")
image_sitemap_url = full_path("image_sitemap.xml")
video_sitemap_url = full_path("video_sitemap.xml")
news_sitemap_url = full_path("news_sitemap.xml")
robotstxt_url = full_path("robots.txt")


def test_build_request_headers():
    user_headers = {"If-None-Match": "ETAG_STRING"}
    final_headers = _build_request_headers(user_headers)
    assert isinstance(final_headers, dict)
    assert final_headers == {
        "user-agent": DEFAULT_HEADERS["User-Agent"],
        "if-none-match": "ETAG_STRING",
    }


def test_build_request_headers_default():
    user_headers = None
    final_headers = _build_request_headers(user_headers)
    assert final_headers == {"user-agent": DEFAULT_HEADERS["User-Agent"]}


def test_build_request_headers_override_default():
    user_headers = {"User-agent": "example/agent", "If-None-Match": "ETAG_STRING"}
    final_headers = _build_request_headers(user_headers)
    assert final_headers == {
        "user-agent": "example/agent",
        "if-none-match": "ETAG_STRING",
    }


def test_regular_sitemap():
    result = sitemap_to_df(regular_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_gz_sitemap():
    result = sitemap_to_df(zipped_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_gz_declared_but_regular_sitemap():
    result = sitemap_to_df(zipped_butnot_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_sitemap_index():
    result = sitemap_to_df(sitemap_index_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert "errors" in result
    errors = {"WARNING: Sitemap contains a link to itself", "HTTP Error 404: Not Found"}
    assert errors.issubset(result["errors"])
    assert all([col in result for col in ["loc", "download_date", "sitemap"]])


def test_error_sitemap():
    with pytest.raises(Exception):
        sitemap_to_df(error_sitemap_url)


def test_image_sitemap():
    result = sitemap_to_df(image_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert "image" in result


def test_video_sitemap():
    result = sitemap_to_df(video_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert "video_content_loc" in result


def test_news_sitemap():
    result = sitemap_to_df(news_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert "news" in result


def test_get_sitemaps_from_robotstxt():
    result = sitemap_to_df(robotstxt_url)
    assert isinstance(result, pd.core.frame.DataFrame)


def test_sitemaps_offline():
    sitemap_path = offline_path("regular_sitemap.xml")
    result = sitemap_to_df(sitemap_path)
    assert isinstance(result, pd.DataFrame)


def test_zipped_sitemaps_offline():
    sitemap_path = offline_path("zipped_sitemap.xml.gz")
    result = sitemap_to_df(sitemap_path)
    assert isinstance(result, pd.DataFrame)


def test_request_headers_propagate_in_robots_recursion(monkeypatch):
    import advertools.sitemaps as sitemaps_module

    original_sitemap_to_df = sitemaps_module.sitemap_to_df
    root_url = "https://example.com/robots.txt"
    child_url = "https://example.com/child-sitemap.xml"
    user_headers = {"X-Test": "header"}
    calls = []

    def wrapped_sitemap_to_df(
        sitemap_url, max_workers=8, recursive=True, request_headers=None
    ):
        calls.append(
            {
                "sitemap_url": sitemap_url,
                "max_workers": max_workers,
                "recursive": recursive,
                "request_headers": request_headers,
            }
        )
        if sitemap_url == root_url:
            return original_sitemap_to_df(
                sitemap_url,
                max_workers=max_workers,
                recursive=recursive,
                request_headers=request_headers,
            )
        return pd.DataFrame({"loc": ["https://example.com/page"], "sitemap": [sitemap_url]})

    monkeypatch.setattr(
        sitemaps_module,
        "_sitemaps_from_robotstxt",
        lambda robots_url, request_headers: [child_url],
    )
    monkeypatch.setattr(sitemaps_module, "sitemap_to_df", wrapped_sitemap_to_df)

    result = wrapped_sitemap_to_df(
        root_url, max_workers=3, recursive=True, request_headers=user_headers
    )

    assert isinstance(result, pd.DataFrame)
    child_calls = [call for call in calls if call["sitemap_url"] == child_url]
    assert child_calls
    assert child_calls[0]["request_headers"] == user_headers
    assert child_calls[0]["max_workers"] == 3
    assert child_calls[0]["recursive"] is True


def test_request_headers_propagate_in_sitemapindex_recursion(monkeypatch):
    import advertools.sitemaps as sitemaps_module

    original_sitemap_to_df = sitemaps_module.sitemap_to_df
    root_url = "https://example.com/sitemap-index.xml"
    child_url = "https://example.com/child-sitemap.xml"
    user_headers = {"X-Test": "header"}
    calls = []

    class _FakeResponse:
        def __init__(self, payload: bytes):
            self._payload = payload

        def read(self):
            return self._payload

        def getheaders(self):
            return []

    sitemapindex_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{child_url}</loc></sitemap>
</sitemapindex>
""".encode("utf-8")

    def fake_urlopen(request):
        request_url = request.full_url if hasattr(request, "full_url") else str(request)
        if request_url == root_url:
            return _FakeResponse(sitemapindex_xml)
        raise AssertionError(f"Unexpected network request: {request_url}")

    def wrapped_sitemap_to_df(
        sitemap_url, max_workers=8, recursive=True, request_headers=None
    ):
        calls.append(
            {
                "sitemap_url": sitemap_url,
                "max_workers": max_workers,
                "recursive": recursive,
                "request_headers": request_headers,
            }
        )
        if sitemap_url == root_url:
            return original_sitemap_to_df(
                sitemap_url,
                max_workers=max_workers,
                recursive=recursive,
                request_headers=request_headers,
            )
        return pd.DataFrame({"loc": ["https://example.com/page"], "sitemap": [sitemap_url]})

    monkeypatch.setattr(sitemaps_module, "urlopen", fake_urlopen)
    monkeypatch.setattr(sitemaps_module, "sitemap_to_df", wrapped_sitemap_to_df)

    result = wrapped_sitemap_to_df(
        root_url, max_workers=5, recursive=True, request_headers=user_headers
    )

    assert isinstance(result, pd.DataFrame)
    child_calls = [call for call in calls if call["sitemap_url"] == child_url]
    assert child_calls
    assert child_calls[0]["request_headers"] == user_headers
    assert child_calls[0]["max_workers"] == 5
    assert child_calls[0]["recursive"] is True
