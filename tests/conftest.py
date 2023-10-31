from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pandas import read_json

from advertools import crawl_headers


@pytest.fixture(scope="session")
def crawl_dir():
    with TemporaryDirectory() as temp_dir:
        return Path(temp_dir).absolute()


@pytest.fixture(scope="session")
def headers_crawl_df(crawl_dir):
    crawl_headers(
        ["https://adver.tools", "does not exist dot com"],
        str(crawl_dir.joinpath("headers_output.jl")),
        custom_settings={
            "ROBOTSTXT_OBEY": False,
            "DEFAULT_REQUEST_HEADERS": {"Accept-Language": "en"},
        },
    )

    df = read_json(crawl_dir.joinpath("headers_output.jl"), lines=True)
    return df
