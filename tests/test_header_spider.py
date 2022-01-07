import os

import pandas as pd
import pytest
from advertools.header_spider import *


def test_crawl_headers_raises_on_wrong_file_extension():
    with pytest.raises(ValueError):
        crawl_headers('https://example.com', 'myfile.wrong')

def test_crawl_headers_returns_df():
    crawl_headers(['https://example.com', 'https://www.nytimes.com'],
                  'delete.jl')
    crawl_df = pd.read_json('delete.jl', lines=True)
    print(crawl_df)
    assert isinstance(crawl_df, pd.DataFrame)
    assert all([col in crawl_df for col in ['url', 'crawl_time', 'status']])
    os.remove('delete.jl')

