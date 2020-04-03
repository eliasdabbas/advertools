"""
Download, Parse, and Analyze XML Sitemaps in Python
===================================================



"""
from gzip import GzipFile
import logging
from xml.etree import ElementTree
from urllib.request import urlopen, Request

import pandas as pd

logging.basicConfig(level=logging.INFO)


def sitemap_to_df(sitemap_url):
    """
    Retrieve all URLs and other available tags of a sitemap and put them in a
    DataFrame.

    You can also pass the URL of a sitemap index file.

    :param url sitemap_url: The URL of a sitemap, either a regular sitemap or a
                            sitemap index. In the case of a sitemap index, the
                            function will go through all the sub sitemaps and
                            retrieve all the included URLs in one Dataframe.
    :return sitemap_df: A pandas DataFrame containing all URLs, as well as
                        other tags if available (``lastmod``, ``changefreq``,
                        ``priority``, ``alternate``).
    """
    if sitemap_url.endswith('xml.gz'):
        xml_text = urlopen(Request(sitemap_url,
                                   headers={'Accept-Encoding': 'gzip'}))
        xml_text = GzipFile(fileobj=xml_text)
    else:
        xml_text = urlopen(sitemap_url)
    tree = ElementTree.parse(xml_text)
    root = tree.getroot()

    sitemap_df = pd.DataFrame()

    if root.tag.split('}')[-1] == 'sitemapindex':
        for elem in root:
            for el in elem:
                if el.text.split('.')[-1] in ['xml', 'gz']:
                    try:
                        logging.info(msg='Getting ' + el.text)
                        sitemap_df = sitemap_df.append(sitemap_to_df(el.text),
                                                       ignore_index=True)
                    except Exception as e:
                        logging.warning(msg=str(e) + el.text)
                        error_df = pd.DataFrame(dict(sitemap=el.text),
                                                index=range(1))
                        sitemap_df = sitemap_df.append(error_df,
                                                       ignore_index=True)

    else:
        logging.info(msg='Getting ' + sitemap_url)
        for elem in root:
            d = {}
            for el in elem:
                tag = el.tag
                name = tag.split('}', 1)[1] if '}' in tag else tag

                if name == 'link':
                    if 'href' in el.attrib:
                        d.setdefault('alternate', []).append(el.get('href'))
                else:
                    d[name] = el.text.strip() if el.text else ''
            if 'alternate' in d:
                d['alternate'] = ', '.join(d['alternate'])
            elem_df = pd.DataFrame(d, index=range(1))
            sitemap_df = sitemap_df.append(elem_df, ignore_index=True)
    sitemap_df['sitemap'] = [sitemap_url] if sitemap_df.empty else sitemap_url
    if 'lastmod' in sitemap_df:
        sitemap_df['lastmod'] = pd.to_datetime(sitemap_df['lastmod'], utc=True)
    if 'priority' in sitemap_df:
        sitemap_df['priority'] = sitemap_df['priority'].astype(float)
    return sitemap_df
