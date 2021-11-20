import os

import pandas as pd
import pytest
from advertools.spider import crawl

links_columns = {
    'links_url': 14,
    'links_text': 14,
    'links_nofollow': 14,
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

crawl('file://' + links_file, 'follow_url_params.jl',
      allowed_domains=[links_file, 'example.com'],
      custom_settings={'ROBOTSTXT_OBEY': False},
      follow_links=True, skip_url_params=False)
follow_url_params_df = pd.read_json('follow_url_params.jl', lines=True)


def follow_url_params_followed():
    assert follow_url_params_df['url'].str.contains('?', regex=False).any()


crawl('file://' + links_file, 'dont_follow_url_params.jl',
      allowed_domains=[links_file, 'example.com'],
      custom_settings={'ROBOTSTXT_OBEY': False},
      follow_links=True, skip_url_params=True)
dont_follow_url_params_df = pd.read_json('dont_follow_url_params.jl',
                                         lines=True)


def dont_follow_url_params_not_followed():
    assert not dont_follow_url_params_df['url'].str.contains('?',
                                                             regex=False).all()


file_path = 'tests/data/crawl_testing/duplicate_links.html'
dup_links_file = os.path.abspath(file_path)
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


def test_image_tags_available():
    assert [col in crawl_df for col in ['img_src', 'img_alt',
                                        'img_height', 'img_width']]


def test_all_img_attrs_have_same_length():
    assert (crawl_df
            .filter(regex='img_')
            .apply(lambda s: s.str.split('@@').str.len())
            .apply(set, axis=1)[0].__len__()) == 1


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
os.remove('follow_url_params.jl')
os.remove('dont_follow_url_params.jl')
