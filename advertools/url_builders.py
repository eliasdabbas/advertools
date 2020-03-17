"""
.. _url_builders:

URL Builders
============
"""

import urllib


def url_utm_ga(url, utm_source, utm_medium=None, utm_campaign=None,
               utm_content=None, utm_term=None):
    """Generate a URL with UTM codes for your campaigns.

    :param str url: a valid URL, required
    :param str utm_source: the referrer of the traffic (e.g. facebook, twitter)
    :param str utm_medium: marketing medium (e.g. banner, email)
    :param str utm_campaign: the name of the campaign
        (e.g. summer_promo, 20pct_off)
    :param str utm_content: ad name / differentiator
        (e.g. 728x90, mpu, square_banner)
    :param str utm_term: search terms bid on (only relevant for search campaigns)
    :return: URL-encoded string for the campaign

    >>> url_utm_ga('mysite.com', utm_source='the source')
    'mysite.com?utm_source=the+source'

    >>> url_utm_ga('mysite.com', utm_source='the source',
    ...            utm_medium='THE MEDIUM!!',
    ...            utm_campaign='campaign*name&^%',utm_content='728x90')
    'mysite.com?utm_content=728x90&utm_campaign=campaign%2Aname%26%5E%25&utm_medium=THE+MEDIUM%21%21&utm_source=the+source'
    """
    url += '?'
    params = {k: v for k, v in locals().items() if k != 'url'}
    return url + urllib.parse.urlencode({k: v for k, v in params.items() if v})
