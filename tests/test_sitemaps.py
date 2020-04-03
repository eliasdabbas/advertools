from advertools.sitemaps import sitemap_to_df
import pandas as pd
import pytest

tests_dir = 'https://github.com/eliasdabbas/advertools/tree/master/tests/'

sitemap_url = tests_dir + 'sitemap.xml'
sitemap_gz_url = tests_dir + 'sitemap.xml.gz'
sitemap_index_url = tests_dir + 'sitemap-index.xml'


def test_regular_sitemap():
    result = sitemap_to_df(sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_gz_sitemap():
    result = sitemap_to_df(sitemap_gz_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_sitemap_index():
    result = sitemap_to_df(sitemap_index_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 11
