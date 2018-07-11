from urllib.parse import urlparse, parse_qs

import pytest
from advertools.url_builders import url_utm_ga


def test_correct_url_returned():
    url = 'www.mysite.com?utm_source=source&utm_medium=medium&utm_campaign=campaign&utm_content=content&utm_term=term'
    composed_url = url_utm_ga('www.mysite.com', 'source', 'medium', 'campaign',
                              'content', 'term')

    parsed = urlparse(url)
    assert parse_qs(parsed.query) == parse_qs(urlparse(composed_url).query)


def test_raises_error_missing_source():
    with pytest.raises(TypeError):
        url_utm_ga('www.mysite.com')


def test_raises_error_missing_url():
    with pytest.raises(TypeError):
        url_utm_ga(source='source')


def test_space_converted_to_plut():
    result = url_utm_ga('www.mysite.com', 'one two')
    assert result == 'www.mysite.com?utm_source=one+two'


def test_symbols_are_url_encoded():
    result = url_utm_ga('www.mysite.com', 'one !@#$%^&*() two')
    assert result == 'www.mysite.com?utm_source=one+%21%40%23%24%25%5E%26%2A%28%29+two'
