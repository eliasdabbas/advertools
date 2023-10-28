from tempfile import TemporaryDirectory

import pytest
from pandas import read_json

from advertools import crawl_headers


@pytest.fixture(scope="session")
def crawl_dir():
    with TemporaryDirectory() as temp_dir:
        return temp_dir


@pytest.fixture(scope="session")
def headers_crawl_df(crawl_dir):
    crawl_headers(
        ["https://adver.tools", "does not exist dot com"],
        f"{crawl_dir}/headers_output.jl",
        custom_settings={
            "ROBOTSTXT_OBEY": False,
            # "LOG_ENABLED": False,
            "DEFAULT_REQUEST_HEADERS": {"Accept-Language": "en"},
        },
    )

    df = read_json(f"{crawl_dir}/headers_output.jl", lines=True)
    return df
