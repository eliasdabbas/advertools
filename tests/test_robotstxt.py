import os
from advertools.robotstxt import robotstxt_to_df, robotstxt_test
import pandas as pd
import pytest
from .test_sitemaps import full_path

robots_file = full_path('robots.txt')


def test_robotstxt_to_df():
    result = robotstxt_to_df('https://www.media-supermarket.com/robots.txt')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result
               for col in ['directive', 'content', 'download_date'])


def test_robtostxt_to_df_handles_list():
    result = robotstxt_to_df([
        'https://www.media-supermarket.com/robots.txt',
        robots_file
    ])
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result
               for col in ['directive', 'content', 'download_date'])


def test_robotstxt_to_df_saves_single_file():
    robotstxt_to_df('https://www.media-supermarket.com/robots.txt',
                    output_file='robots_output.jl')
    result = pd.read_json('robots_output.jl', lines=True)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result
               for col in ['directive', 'content', 'download_date'])
    os.remove('robots_output.jl')


def test_robotstxt_to_df_saves_file_list():
    robotstxt_to_df(['https://www.media-supermarket.com/robots.txt',
                     robots_file],
                    output_file='robots_output.jl')
    result = pd.read_json('robots_output.jl', lines=True)
    assert isinstance(result, pd.core.frame.DataFrame)
    assert all(col in result
               for col in ['directive', 'content', 'download_date'])
    os.remove('robots_output.jl')


def test_robotstxt_to_df_raises_on_wrong_file():
    with pytest.raises(ValueError):
        robotstxt_to_df(robots_file, output_file='wrong_extension.pdf')


def test_robotstxt_to_df_contains_errors():
    result = robotstxt_to_df('wrong_url.html')
    assert 'errors' in result


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
