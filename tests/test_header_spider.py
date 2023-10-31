import platform

import pytest

from advertools.header_spider import crawl_headers


def test_crawl_headers_raises_on_wrong_file_extension():
    with pytest.raises(ValueError):
        crawl_headers("https://example.com", "myfile.wrong")


@pytest.mark.parametrize("column", ["url", "crawl_time", "status"])
@pytest.mark.skipif(platform.system() == "Windows", reason="Skip if on Windows")
def test_crawl_headers_returns_df(headers_crawl_df, column):
    assert column in headers_crawl_df
