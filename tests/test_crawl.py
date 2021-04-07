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

dup_links_file = os.path.abspath('tests/data/crawl_testing/duplicate_links.html')
crawl('file://' + dup_links_file, 'dup_links_crawl.jl',
      custom_settings={'ROBOTSTXT_OBEY': False})
dup_crawl_df = pd.read_json('dup_links_crawl.jl', lines=True)


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


dup_links_test = (['https://example_a.com' for i in range(5)] +
                  ['https://example.com'])

dup_text_test = ['Link Text A',
                 'Link Text A',
                 'Link Text A',
                 'Link Text B',
                 'Link Text C',
                 'Link Other']

dup_nf_test = ['True'] + ['False' for i in range(5)]


def test_duplicate_links_counted_propery():
    assert dup_crawl_df['links_url'].str.split('@@')[0] == dup_links_test
    assert dup_crawl_df['links_text'].str.split('@@')[0] == dup_text_test
    assert dup_crawl_df['links_nofollow'].str.split('@@')[0] == dup_nf_test


def test_non_existent_links_are_NA():
    assert 'nav_links_url' not in dup_crawl_df
    assert 'nav_links_text' not in dup_crawl_df
    assert 'header_links_url' not in dup_crawl_df
    assert 'footer_links_url' not in dup_crawl_df


os.remove('links_crawl.jl')
os.remove('dup_links_crawl.jl')
