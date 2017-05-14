from urllib.parse import urlparse, urljoin


def utm_builder(url, source, medium=None, campaign_name=None,
                content=None, term=None):
    url = (url + '?') if '?' not in url else (url + '&')
    source = 'utm_source=' + source
    url += source
    if medium:
        medium = '&utm_medium=' + medium
        url += medium
    if campaign_name:
        campaign_name = '&utm_campaign=' + campaign_name
        url += campaign_name
    if content:
        content = '&utm_content=' + content
        url += content
    if term:
        term = '&utm_term=' + term
        url += term
    return url
