import os

import pytest
from advertools.spider import crawl
import pandas as pd

links_columns = {
    'links_url': 12,
    'links_text': 12,
    'links_nofollow': 12,
    'nav_links_url': 3,
    'nav_links_text': 3,
    'header_links_url': 3,
    'header_links_text': 3,
    'footer_links_url': 3,
    'footer_links_text': 3,
}

links_file = os.path.abspath('tests/data/crawl_testing/test_content.html')
crawl('file://' + links_file, 'links_crawl.jl',
      custom_settings={'ROBOTSTXT_OBEY': False})
crawl_df = pd.read_json('links_crawl.jl', lines=True)


def test_link_columns_all_exist():
    assert set(links_columns).difference(crawl_df.columns.tolist()) == set()


@pytest.mark.parametrize("colname,count", links_columns.items())
def test_links_extracted_at_correct_number(colname, count):
    assert crawl_df[colname].str.split('@@').str.len().values[0] == count


def test_extract_h_tags():
    assert crawl_df['h2'].str.split('@@').str.len().values[0] == 3
    assert crawl_df['h2'].str.split('@@').explode().iloc[1] == ''


def test_all_links_have_nofollow():
    assert (crawl_df
            .filter(regex='nofollow')
            .apply(lambda s: s.str.contains("True"))
            .all().all())


os.remove('links_crawl.jl')
