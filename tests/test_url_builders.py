from urllib.parse import urlparse, parse_qs

from advertools.url_builders import url_utm_ga
import pytest

def test_correct_url_returned():
    url = 'www.mysite.com?utm_source=source&utm_medium=medium&utm_campaign=campaign&utm_content=content&utm_term=term'
    composed_url = url_utm_ga('www.mysite.com', 'source', 'medium', 'campaign', 
                     'content', 'term')
    
    parsed = urlparse(url)
    assert parse_qs(parsed.query) == parse_qs(urlparse(url).query)
