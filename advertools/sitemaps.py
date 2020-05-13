"""
Download, Parse, and Analyze XML Sitemaps
=========================================

One of the fastest and easiest ways to get insights on a website's content is
to simply download its XML sitemap(s).

It basically contains a log of their publishing activity, and if they have rich
URLs then you can do some good analysis on their content across time as well.

The :func:`sitemap_to_df` is very simple to use, and only requires the URL of a
sitemap, or a sitemap index. It goes through the sitemap(s) and returns a
DataFrame containing the tags and their information.

Let's go through a quick example of what can be done with sitemaps. We can
start by getting one of the BBC's sitemaps.

>>> bbc_sitemap = sitemap_to_df('https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml')
>>> bbc_sitemap
                                                     loc                    lastmod                                            sitemap
0      https://www.bbc.com/arabic/middleeast/2009/06/...  2009-06-20 14:10:48+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
1      https://www.bbc.com/arabic/middleeast/2009/06/...  2009-06-20 21:07:43+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
2      https://www.bbc.com/arabic/business/2009/06/09...  2009-06-22 12:41:48+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
3      https://www.bbc.com/arabic/multimedia/2009/06/...  2009-06-24 15:27:24+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
4      https://www.bbc.com/arabic/business/2009/06/09...  2009-06-18 15:32:54+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
                                                  ...                        ...                                                ...
49994  https://www.bbc.com/vietnamese/world/2009/09/0...  2009-09-02 11:46:23+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
49995  https://www.bbc.com/vietnamese/world/2009/09/0...  2009-09-04 11:20:42+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
49996  https://www.bbc.com/vietnamese/world/2009/09/0...  2009-09-02 02:40:41+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
49997  https://www.bbc.com/vietnamese/football/2009/0...  2009-09-02 03:09:06+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
49998  https://www.bbc.com/vietnamese/world/2009/09/0...  2009-09-05 04:38:11+00:00  https://www.bbc.com/sitemaps/https-sitemap-com...
[49999 rows x 3 columns]

>>> bbc_sitemap.dtypes
loc                     object
lastmod    datetime64[ns, UTC]
sitemap                 object
dtype: object

Since ``lastmod`` is a ``datetime`` object, we can easily use it for various
time-related operations.
Here we look at how many articles have been published (last modified) per year.

>>> bbc_sitemap.set_index('lastmod').resample('A')['loc'].count()
lastmod
2008-12-31 00:00:00+00:00     2261
2009-12-31 00:00:00+00:00    47223
2010-12-31 00:00:00+00:00        0
2011-12-31 00:00:00+00:00        0
2012-12-31 00:00:00+00:00        0
2013-12-31 00:00:00+00:00        0
2014-12-31 00:00:00+00:00        0
2015-12-31 00:00:00+00:00        0
2016-12-31 00:00:00+00:00        0
2017-12-31 00:00:00+00:00        0
2018-12-31 00:00:00+00:00        0
2019-12-31 00:00:00+00:00      483
2020-12-31 00:00:00+00:00       32
Freq: A-DEC, Name: loc, dtype: int64

As the majority are in 2009 with a few in other years, it seems these were
later updated, but we would have to check to verify (in this special case BBC's
URLs contain date information, which can be compared to ``lastmod`` to check if
there is a difference between them).

We can take a look at a sample of the URLs to get the URL template that they
use.

>>> bbc_sitemap['loc'].sample(10).tolist()
['https://www.bbc.com/russian/rolling_news/2009/06/090628_rn_pakistani_soldiries_ambush',
 'https://www.bbc.com/urdu/pakistan/2009/04/090421_mqm_speaks_rza',
 'https://www.bbc.com/arabic/middleeast/2009/07/090723_ae_silwan_tc2',
 'https://www.bbc.com/portuguese/noticias/2009/07/090729_iraquerefenbritsfn',
 'https://www.bbc.com/portuguese/noticias/2009/06/090623_egitomilitaresfn',
 'https://www.bbc.com/portuguese/noticias/2009/03/090302_gazaconferenciaml',
 'https://www.bbc.com/portuguese/noticias/2009/07/090715_hillary_iran_cq',
 'https://www.bbc.com/vietnamese/culture/2009/04/090409_machienhuu_revisiting',
 'https://www.bbc.com/portuguese/noticias/2009/05/090524_paquistaoupdateg',
 'https://www.bbc.com/arabic/worldnews/2009/06/090629_om_pakistan_report_tc2']

It seems the pattern is

    **https://www.bbc.com/{language}/{topic}/{YYYY}/{MM}/{YYMMDD_article_title}**

This is quite a rich structure, full of useful information. We can easily count
how many articles they have by language, by splitting by "/" and getting the
elements at index three, and counting them.

>>> bbc_sitemap['loc'].str.split('/').str[3].value_counts()
russian       14022
persian       10968
portuguese     5403
urdu           5068
mundo          5065
vietnamese     3561
arabic         2984
hindi          1677
turkce          706
ukchina         545
Name: loc, dtype: int64

We can also get a subset of articles written in a certain language, and see how
many articles they publish per month, week, year, etc.

>>> (bbc_sitemap[bbc_sitemap['loc']
...  .str.contains('/russian/')]
...  .set_index('lastmod')
...  .resample('M')['loc'].count())
lastmod
2009-04-30 00:00:00+00:00    1506
2009-05-31 00:00:00+00:00    2910
2009-06-30 00:00:00+00:00    3021
2009-07-31 00:00:00+00:00    3250
2009-08-31 00:00:00+00:00    2769
                             ...
2019-09-30 00:00:00+00:00       8
2019-10-31 00:00:00+00:00      17
2019-11-30 00:00:00+00:00      11
2019-12-31 00:00:00+00:00      24
2020-01-31 00:00:00+00:00       6
Freq: M, Name: loc, Length: 130, dtype: int64

The fifth element after splitting URLs is the topic or category of the article.
We can do the same and count the values.

>>> bbc_sitemap['loc'].str.split('/').str[4].value_counts()[:30]
rolling_news          9044
world                 5050
noticias              4224
iran                  3682
pakistan              2103
afghanistan           1959
multimedia            1657
internacional         1555
sport                 1350
international         1293
india                 1285
america_latina        1274
business              1204
cultura_sociedad       913
middleeast             874
worldnews              872
russia                 841
radio                  769
science                755
football               674
arts                   664
ciencia_tecnologia     627
entertainment          621
simp                   545
vietnam                539
economia               484
haberler               424
interactivity          411
help                   354
ciencia                308
Name: loc, dtype: int64

Finally, we can take the last element after splitting, which contains the slugs
of the articles, replace underscores with spaces, split, concatenate all, put
in a ``pd.Series`` and count the values. This way we see how many times each
word occurred in an article.

>>> (pd.Series(
...     bbc_sitemap['loc']
...     .str.split('/')
...     .str[-1]
...     .str.replace('_', ' ')
...     .str.cat(sep=' ')
...     .split()
...    )
...     .value_counts()[:15])
rn        8808
tc2       3153
iran      1534
video      973
obama      882
us         862
china      815
ir88       727
russia     683
si         640
np         638
afghan     632
ka         565
an         556
iraq       554
dtype: int64
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
                            retrieve all the included URLs in one DataFrame.
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
