import os
from advertools.sitemaps import sitemap_to_df
import pandas as pd
import pytest


def full_path(file):
    tests_dir = 'tests/sitemap_testing/'
    return 'file://' + os.path.abspath(tests_dir + file)

regular_sitemap_url = full_path('regular_sitemap.xml')
zipped_sitemap_url = full_path('zipped_sitemap.xml.gz')
sitemap_index_url = full_path('sitemap_index.xml')
error_sitemap_url = full_path('error_sitemap.xml')
image_sitemap_url = full_path('image_sitemap.xml')
video_sitemap_url = full_path('video_sitemap.xml')
news_sitemap_url = full_path('news_sitemap.xml')
robotstxt_url = full_path('robots.txt')


def test_regular_sitemap():
    result = sitemap_to_df(regular_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_gz_sitemap():
    result = sitemap_to_df(zipped_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 5


def test_sitemap_index():
    result = sitemap_to_df(sitemap_index_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all([col in result
               for col in ['loc', 'sitemap_downloaded', 'sitemap']])


def test_error_sitemap():
    with pytest.raises(Exception):
        result = sitemap_to_df(error_sitemap_url)


def test_image_sitemap():
    result = sitemap_to_df(image_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'image' in result


def test_video_sitemap():
    result = sitemap_to_df(video_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'video_content_loc' in result


def test_news_sitemap():
    result = sitemap_to_df(news_sitemap_url)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'news' in result


def test_get_sitemaps_from_robotstxt():
    result = sitemap_to_df(robotstxt_url)