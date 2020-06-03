import os
from advertools.robotstxt import robotstxt_to_df, robotstxt_test
import pandas as pd
import pytest
from .test_sitemaps import full_path

# robots_file = 'file://' + os.path.abspath('tests/sitemap_testing/robots.txt')
robots_file = full_path('robots.txt')

def test_robotstxt_to_df():
    result = robotstxt_to_df('https://www.media-supermarket.com/robots.txt')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result
               for col in ['directive', 'content', 'file_downloaded'])


def test_robotstxt_test():
    user_agents = ['Googlebot', 'Baiduspider', '*']
    urls_to_check = ['/', '/help', 'something.html']
    result = robotstxt_test(robots_file, user_agents, urls_to_check)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result for col in
               ['robotstxt_url', 'user_agent', 'url_path', 'can_fetch'])


def test_robotstxt_raises():
    with pytest.raises(ValueError):
        robotstxt_test('http://www.wrong-url.com', '*', '/')


def test_robots_converts_str_to_list():
    result = robotstxt_test('https://www.apple.com/robots.txt', '*', 'hello')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result for col in
               ['robotstxt_url', 'user_agent', 'url_path', 'can_fetch'])

