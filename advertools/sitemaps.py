"""
.. _sitemaps:

Download, Parse, and Analyze XML Sitemaps
=========================================

One of the fastest and easiest ways to get insights on a website's content is
to simply download its XML sitemap(s).

Sitemaps are also important SEO tools as they reveal a lot of information about
the website, and help search engines in indexing those pages. You might want to
run an SEO audit and check if the URLs in the sitemap properly correspond to
the actual URLs of the site, so this would be an easy way to get them.

Sitemaps basically contain a log of publishing activity, and if they have rich
URLs then you can do some good analysis on their content across time as well.

The :func:`sitemap_to_df` function is very simple to use, and only requires the
URL of a sitemap, a sitemap index, or even a robots.txt file. It goes through
the sitemap(s) and returns a DataFrame containing the tags and their
information.

Let's go through a quick example of what can be done with sitemaps. We can
start by getting one of the BBC's sitemaps.

Regular XML Sitemaps
--------------------

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


This was a quick overview and data preparation for a sample sitemap. Once you
are familiar with the sitemap's structure, you can more easily start analyzing
the content.

News Sitemaps
-------------

>>> nyt_news = sitemap_to_df('https://www.nytimes.com/sitemaps/new/news.xml.gz')
>>> nyt_news
                                                   loc                    lastmod    publication_name publication_language news_publication_date                                          news_title                                      news_keywords                                          image_loc                                           sitemap                sitemap_downloaded
0    https://www.nytimes.com/2020/05/19/sports/hors...  2020-05-19 15:49:28+00:00  The New York Times                en-US  2020-05-19T15:49:28Z   Belmont Stakes to Run June 20 as First Leg of ...  Triple Crown (Horse Racing), Horse Racing, Bel...  https://static01.nyt.com/images/2020/05/19/spo...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
1    https://www.nytimes.com/2020/05/19/us/coronavi...  2020-05-19 15:49:10+00:00  The New York Times                en-US  2020-05-19T09:21:33Z                   Coronavirus Live News and Updates                            Coronavirus (2019-nCoV)  https://static01.nyt.com/images/2020/05/19/wor...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
2    https://www.nytimes.com/interactive/2020/obitu...  2020-05-19 15:48:46+00:00  The New York Times                en-US  2020-04-16T22:28:14Z                                    Those We’ve Lost                                Deaths (Obituaries)                                                NaN  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
3    https://www.nytimes.com/2020/05/19/nyregion/co...  2020-05-19 15:48:06+00:00  The New York Times                en-US  2020-05-19T11:24:24Z   Number of N.Y.C. Students Slated for Summer Sc...  Coronavirus (2019-nCoV), New York State, New Y...  https://static01.nyt.com/images/2020/05/19/nyr...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
4    https://www.nytimes.com/2020/05/19/books/coron...  2020-05-19 15:46:10+00:00  The New York Times                en-US  2020-05-19T15:46:10Z           Coronavirus Shutdowns Weigh on Book Sales  Books and Literature, Book Trade and Publishin...  https://static01.nyt.com/images/2020/05/19/boo...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
..                                                 ...                        ...                 ...                  ...                   ...                                                 ...                                                ...                                                ...                                               ...                               ...
502  https://www.nytimes.com/2020/05/14/books/revie...  2020-05-17 16:17:52+00:00  The New York Times                   en  2020-05-14T09:00:03Z   The Title of Emma Straub’s New Novel Is Mockin...  Books and Literature, Straub, Emma, All Adults...  https://static01.nyt.com/images/2020/04/21/boo...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
503  https://www.nytimes.com/2020/05/17/opinion/nur...  2020-05-17 16:08:29+00:00  The New York Times                en-US  2020-05-17T15:00:07Z   Coronavirus Is Hitting Nursing Homes Hard. How...  Nursing Homes, Coronavirus (2019-nCoV), Elderl...  https://static01.nyt.com/images/2020/05/17/opi...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
504  https://www.nytimes.com/2020/05/17/business/co...  2020-05-17 16:00:08+00:00  The New York Times                en-US  2020-05-17T16:00:08Z   Autoworkers Are Returning as Carmakers Gradual...  Automobiles, Shutdowns (Institutional), Labor ...  https://static01.nyt.com/images/2020/05/18/bus...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
505  https://www.nytimes.com/2020/05/17/opinion/let...  2020-05-17 16:00:05+00:00  The New York Times                en-US  2020-05-17T16:00:05Z              Fathers, Sons, Forgiveness and Regrets                  Children and Childhood, Parenting  https://static01.nyt.com/images/2020/05/10/opi...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
506  https://www.nytimes.com/2020/05/17/opinion/let...  2020-05-17 16:00:05+00:00  The New York Times                en-US  2020-05-17T16:00:05Z                                To the Class of 2020          Coronavirus (2019-nCoV), Education (K-12)  https://static01.nyt.com/images/2020/04/16/wor...  https://www.nytimes.com/sitemaps/new/news.xml.gz  2020-05-19 15:49:44.459267+00:00
[507 rows x 13 columns]

Video Sitemaps
--------------

>>> wired_video = sitemap_to_df('https://www.wired.com/video/sitemap.xml')
>>> wired_video
                                                    loc                                video_thumbnail_loc                                          video_title                                    video_description                                    video_content_loc video_duration       video_publication_date video_expiration_date                                   sitemap               sitemap_downloaded
0     https://www.wired.com/video/watch/autocomplete...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...    WIRED Autocomplete Interviews - Lele Pons Answ...    Lele Pons takes the WIRED Autocomplete Intervi...    http://dp8hsntg6do36.cloudfront.net/5db75425bc...            478    2019-10-29T16:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
1     https://www.wired.com/video/watch/professor-ex...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...    Laser Expert Explains One Concept in 5 Levels ...    Donna Strickland, PhD, professor at the Univer...    http://dp8hsntg6do36.cloudfront.net/5da6107834...           1476    2019-10-28T17:18:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
2     https://www.wired.com/video/watch/6-levels-of-...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...           6 Levels of Knife Making: Easy to Complex     Knife maker Chelsea Miller explains knife maki...    http://dp8hsntg6do36.cloudfront.net/5db32c4a34...            963    2019-10-25T19:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
3     https://www.wired.com/video/watch/mycologist-e...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...    Mycologist Explains How a Slime Mold Can Solve...    Physarum polycephalum is a single-celled, brai...    http://dp8hsntg6do36.cloudfront.net/5db31cfabc...            606    2019-10-25T16:27:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
4     https://www.wired.com/video/watch/almost-impos...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...    Why It's Almost Impossible to Do a Quintuple C...    Tricking is a sport with roots in martial arts...    http://dp8hsntg6do36.cloudfront.net/5db2005238...            644    2019-10-24T20:34:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
...                                                 ...                                                ...                                                  ...                                                  ...                                                  ...            ...                          ...                   ...                                       ...                              ...
2338  https://www.wired.com/video/watch/how-to-make-...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...                            How To Make Wired Origami    Robert Lang explains how to fold the Wired iss...    http://dp8hsntg6do36.cloudfront.net/5171b3cbc2...            150    2008-09-23T00:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
2339  https://www.wired.com/video/watch/clover-coffe...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...                                Clover Coffee Machine    Wired.com takes a look at the 'Clover', an $11...    http://dp8hsntg6do36.cloudfront.net/5171b42ec2...            147    2008-09-23T00:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
2340  https://www.wired.com/video/watch/original-war...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...                            Original WarGames Trailer                            Original WarGames Trailer    http://dp8hsntg6do36.cloudfront.net/5171b427c2...            140    2008-07-21T04:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
2341  https://www.wired.com/video/watch/rock-band-tr...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...                                    Rock Band Trailer                                    Rock Band Trailer    http://dp8hsntg6do36.cloudfront.net/5171b431c2...             70    2007-09-14T04:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
2342  https://www.wired.com/video/watch/arrival-full...  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/...                             ‘Arrival’ — Full Trailer    Louise Banks (Amy Adams) must learn to communi...    http://dp8hsntg6do36.cloudfront.net/57b344f4fd...            145    2003-10-22T04:00:00+00:00                   NaN   https://www.wired.com/video/sitemap.xml 2020-05-19 16:18:17.813461+00:00
[2343 rows x 11 columns]
"""
from gzip import GzipFile
import logging
from xml.etree import ElementTree
from urllib.request import urlopen, Request

import pandas as pd

logging.basicConfig(level=logging.INFO)


def _sitemaps_from_robotstxt(robots_url):
    sitemaps = []
    robots_page = urlopen(robots_url)
    for line in robots_page.readlines():
        if line.decode().lower().startswith('sitemap:'):
            sitemaps.append(line.decode().split()[-1])
    return sitemaps


def _parse_sitemap(root):
    d = dict()
    for node in root:
        for n in node:
            if 'loc' in n.tag:
                d[n.text] = {}

    def parse_xml_node(node, node_url, prefix=''):
        nonlocal d
        keys = []
        for element in node:
            if element.text:
                tag = element.tag.split('}')[-1]
                d[node_url][prefix + tag] = element.text
                keys.append(tag)
                prefix = prefix if tag in keys else ''
            if list(element):
                parse_xml_node(element, node_url, prefix=element.tag.split('}')[-1] + '_')
    for node in root:
        node_url = [n.text for n in node if 'loc' in n.tag][0]
        parse_xml_node(node, node_url=node_url)
    return pd.DataFrame(d.values())


def sitemap_to_df(sitemap_url):
    """
    Retrieve all URLs and other available tags of a sitemap(s) and put them in
    a DataFrame.

    You can also pass the URL of a sitemap index, or a link to a robots.txt
    file.

    :param url sitemap_url: The URL of a sitemap, either a regular sitemap, a
                            sitemap index, or a link to a robots.txt file.
                            In the case of a sitemap index or robots.txt, the
                            function will go through all the sub sitemaps and
                            retrieve all the included URLs in one DataFrame.
    :return sitemap_df: A pandas DataFrame containing all URLs, as well as
                        other tags if available (``lastmod``, ``changefreq``,
                        ``priority``, ``alternate``, or others found in news,
                        video, or image sitemaps).
    """
    if sitemap_url.endswith('robots.txt'):
        return pd.concat([sitemap_to_df(sitemap)
                          for sitemap in _sitemaps_from_robotstxt(sitemap_url)])
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
                if 'loc' in el.tag:
                    try:
                        sitemap_df = sitemap_df.append(sitemap_to_df(el.text),
                                                       ignore_index=True)
                    except Exception as e:
                        logging.warning(msg=str(e) + el.text)
                        error_df = pd.DataFrame(dict(sitemap=el.text),
                                                index=range(1))
                        error_df['errors'] = str(e)
                        sitemap_df = sitemap_df.append(error_df,
                                                       ignore_index=True)

    else:
        logging.info(msg='Getting ' + sitemap_url)
        elem_df = _parse_sitemap(root)
        sitemap_df = sitemap_df.append(elem_df, ignore_index=True)
        sitemap_df['sitemap'] = [sitemap_url] if sitemap_df.empty else sitemap_url
    if 'lastmod' in sitemap_df:
        sitemap_df['lastmod'] = pd.to_datetime(sitemap_df['lastmod'], utc=True)
    if 'priority' in sitemap_df:
        sitemap_df['priority'] = sitemap_df['priority'].astype(float)
    sitemap_df['sitemap_downloaded'] = pd.Timestamp.now(tz='UTC')
    return sitemap_df


def robotstxt_to_df(robotstxt_url):
    """Download the contents of ``robotstxt_url`` into a DataFrame

    :param url robotstxt_url: The URL of the robots.txt file
    :returns DataFrame robotstxt_df: A DataFrame containing directives, their
                                     content, the URL and time of download
    """
    logging.info(msg='Getting: ' + robotstxt_url)
    robots_open = urlopen(robotstxt_url)
    robots_text = robots_open.readlines()

    lines = []
    for line in robots_text:
        if line and line.decode().startswith('#'):
            lines.append(['comment', line.decode().replace('#', '').strip()])
        if line and line.decode()[0].isupper():
            split = line.decode().split(':', maxsplit=1)
            lines.append([split[0], split[1].strip()])
    df = pd.DataFrame(lines, columns=['directive', 'content'])
    df['robotstxt_url'] = robotstxt_url
    df['file_downloaded'] = pd.Timestamp.now(tz='UTC')
    return df
