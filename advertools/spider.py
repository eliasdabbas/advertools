"""
Python SEO Crawler / Spider
===========================

A straightforward crawler to analyze SEO and content of pages and websites.

This is provided by the :func:`crawl` function which is customized for SEO and
content analysis usage, and is highly configurable. The crawler uses
`Scrapy <https://scrapy.org/>`_ so you get all the power that it provides in
terms of performance, speed, as well as flexibility and customization.

There are two main approaches to crawl:

1. **Discovery:** You know the website to crawl, so you provide a ``url_list``
   or the website's sitemap(s), and you want the crawler to go through the
   whole website(s) by following all available links.

2. **Pre-determined:** You have a known set of URLs that you want to crawl and
   analyze, without following links or discovering new URLs.

Discovery
^^^^^^^^^

The simplest way to use the function is to provide a list of one or more
sitemap URLs. You can alternatively provide a link to a sitemap index URL, and
the crawler will go through all of the sitemaps.

.. code-block:: python

   >>> crawl(['https://example.com/sitemap.xml'], 'my_output_file.csv')  # OR
   >>> crawl(['https://example.com/sitemap-index.xml'], 'my_output_file.csv')

That's it!

What this does:

* Check the site's robots.txt file and get the crawl rules, together with any
  sitemaps if available
* Go to the specified sitemap (or sitemap index)
* Go through all the URLs in the sitemap(s)
* For each URL extract the most important SEO elements
* Save them to ``output_file`` in the specified format
* The column headers of the output file (if you specify csv) would be the names
  of the elements

Supported file extensions:

* csv
* json
* jl
* xml
* marshal
* pickle


Extracted On-Page SEO Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The names of these elements become the headers (column names) of the
``output_file``.

==============    =============================================================
Element           Remarks
==============    =============================================================
url               The URL requested
title             The <title> tag(s)
meta_desc         Meta description
h1                `<h1>` tag(s)
h2                `<h2>` tag(s)
h3                `<h3>` tag(s)
body_text         The text in the <p> tags
size              The page size in bytes
load_time         The load time of the HTML (does NOT include images or videos)
status            Response status (200, 301, 302, 404, etc.)
links_href        The links in the page ``href`` attribute
links_text        The link titles (empty string if not available)
img_src           The ``src`` attribute of images
img_alt           The ``alt`` attribute if available or an empty string
page_depth        The depth of the crawled page
crawl_time        Date and time of the crawl
==============    =============================================================

.. note::

    All elements that may appear multiple times in a page (like header tags, or
    images, for example), will be joined with two @ signs `@@`. For example,
    **"first H2 tag@@second H2 tag@@third tag"** and so on.
    Once you open the file, you simply have to split by `@@` to get the
    elements as a list.

Here is a sample file:

.. code-block:: python

    >>> import pandas as pd
    >>> site_crawl = pd.read_csv('path/to/file.csv')
    >>> site_crawl.head()
                                                    url                                              title                                          meta_desc                                                 h1                                                 h2                                                 h3                                          body_text    size  load_time  status                                         links_href                                         links_text                                            img_src                                            img_alt  page_depth           crawl_time
    0  https://www.wsj.com/articles/u-s-extends-indiv...  U.S. Extends Individual Tax Filing Deadline fr...  The U.S. will extend the individual tax filing...       U.S. Extends Individual Tax Filing Deadl...  Tax preparers and lawmakers in both parties ur...                                                NaN  March 20, 2020 WASHINGTON—The U.S. extended t...  599133   0.828943     200  #main@@https://www.barrons.com@@http://bigchar...  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@...  https://m.wsj.net/video/20200320/032020virusne...  [https://m.wsj.net/video/20200320/032020virusn...           1  2020-03-20 23:58:13
    1  https://www.wsj.com/livecoverage/coronavirus-p...  States Hold Primary Elections in Coronavirus O...  Three states held the first primary elections,...  States Hold Primary Elections in Coronavirus O...  Three states held the first primary elections,...  Biden Wins Florida, Illinois and Arizona@@Main...  March 20, 2020 Joe Biden won all three primar...  495898   0.818214     200  #main@@https://www.barrons.com@@http://bigchar...  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@...            https://images.wsj.net/im-165947/social                                                NaN           1  2020-03-20 23:58:14
    2       https://www.wsj.com/livecoverage/coronavirus  Coronavirus Updates: Dow, Stocks Waver; Califo...  As the coronavirus pandemic roils markets and ...  Coronavirus Updates: Stocks Drop as More State...  As the coronavirus pandemic roils markets and ...  What to Know Now@@Business-Development Compani...  March 20, 2020 , which raise money from inves...  523662   0.826189     200  #main@@https://www.barrons.com@@http://bigchar...  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@...                                                NaN                                                NaN           1  2020-03-20 23:58:14
    3  https://www.wsj.com/articles/ford-marriott-ama...  Ford, Marriott, Amazon.com: Stocks That Define...  Here are seven major companies whose shares mo...       Ford, Marriott, Amazon.com: Stocks That ...  Here are seven major companies whose shares mo...                                                NaN  March 20, 2020  Ford Motor Co.  Detroit’s au...  600647   0.846521     200  #main@@https://www.barrons.com@@http://bigchar...  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@...  https://m.wsj.net/video/20200320/032020virusne...  [https://m.wsj.net/video/20200320/032020virusn...           1  2020-03-20 23:58:14
    4  https://www.wsj.com/articles/airbnb-racks-up-h...  Airbnb Racks Up Hundreds of Millions in Losses...  Airbnb is considering raising capital from new...       Airbn

Pre-Determined Crawling Approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you might have a fixed set of URLs for which you want to scrape and
analyze SEO or content performance. Let's say you just ran
:ref:`serp_goog <serp>` and got a bunch of top-ranking pages that you would
like to analyze, and see how that relates to their SERP ranking.

You simply provide the ``url_list`` parameter and again specify the
``output_file``. This will only crawl the specified URLs, and will not follow
any links.

Other than crawling SERP results landing pages, this might be useful for
monitoring certain pages that change all the time.

Again running the function is as simple as providing a list of URLs, as well as
a filepath where you want the result saved.

.. code-block:: python

    >>> crawl(url_list, output_file)

The difference between the two approaches, is the simple parameter
``follow_links``. If you specify this as ``False`` (the default), the crawler
will only go through the provided URLs (or sitemaps). Otherwise, it will
discover pages by following links on pages that it crawls.
So how do you make sure that the crawler doesn't try to crawl the whole web
when ``follow_links`` is `True`?
The ``allowed_domains`` parameter ensures that you specify which domains you
want to limit your crawler to.
This is an optional parameter. If you don't specify it, then it will
default to only the domains in the ``url_list`` and/or the ``sitemap_urls``.


.. code-block:: python

    >>> crawl(sitemap_urls, url_list, output_file, allowed_domains,
    ...       follow_links, custom_settings)



"""
import datetime
import json
import subprocess

from urllib.parse import urlparse
from itertools import zip_longest

from scrapy.spiders import Spider, SitemapSpider
from scrapy import Request
import advertools as adv
from advertools.sitemaps import sitemap_to_df
import pandas as pd

spider_path = adv.__path__[0] + '/spider.py'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',


class SEOSitemapSpider(Spider):
    name = 'seo_sitemap_spider'
    # follow_links = False
    lastmods = []
    custom_settings = {
        'USER_AGENT': user_agent,
        'ROBOTSTXT_OBEY': True,
        'HTTPERROR_ALLOW_ALL': True,
        # 'CLOSESPIDER_PAGECOUNT': 5,
        'BOT_NAME': 'bot'
    }

    def __init__(self, url_list=None, allowed_domains=None, lastmods=None,
                 follow_links=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(url_list.split(',')))
        self.allowed_domains = json.loads(json.dumps(allowed_domains.split(',')))
        self.lastmods = json.loads(json.dumps(lastmods.split(',')))
        self.follow_links = eval(json.loads(json.dumps(follow_links)))
        print('#' * 80)
        print(follow_links, type(follow_links))
        print(self.follow_links, type(self.follow_links))
        print('START URLS:', len(self.start_urls))
        print('LASTMODS:', len(self.lastmods))
        print('#' * 80)

    def start_requests(self):
        for url, lastmod in zip_longest(self.start_urls, self.lastmods):
            yield Request(url, callback=self.parse,
                          cb_kwargs={'url': url,
                                     'lastmod': lastmod})

    def parse(self, response, url=None, lastmod=None):
        yield dict(
            url=url,
            url_redirected_to=response.url,
            lastmod=lastmod,
            title='@@'.join(response.css('title::text').getall()),
            meta_desc=response.xpath("//meta[@name='description']/@content").get(),
            h1='@@'.join(response.css('h1::text').getall()),
            h2='@@'.join(response.css('h2::text').getall()),
            h3='@@'.join(response.css('h3::text').getall()),
            body_text='\n'.join(response.css('p::text').getall()),
            size=len(response.body),
            load_time=response.meta['download_latency'],
            status=response.status,
            links_href='@@'.join([link.attrib.get('href') or '' for link in response.css('a')]),
            links_text='@@'.join([link.attrib.get('title') or '' for link in response.css('a')]),
            img_src='@@'.join([im.attrib.get('src') or '' for im in response.css('img')]),
            img_alt='@@'.join([im.attrib.get('alt') or '' for im in response.css('img')]),
            page_depth=response.meta['depth'],
            crawl_time= datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        )
        if self.follow_links:
            next_pages = response.css('a::attr(href)').getall()
            if next_pages:
                for page in next_pages:
                    yield Request(response.urljoin(page), callback=self.parse)
                    # yield response.follow(page, callback=self.parse)


def crawl(sitemap_urls=None, url_list=None, allowed_domains=None,
          follow_links=False, output_file=None, custom_settings=None):
    """
    Crawl a website's URLs based on the given :attr:`sitemap_urls`

    :param list sitemap_urls: A list of one or more XML sitemap (or sitemap
                              index) URLs.
    :param list url_list: A list of URLs to crawl. If ``follow_links`` is True,
                          the crawler will start with these URLs and follow all
                          links on pages recursively.
    :param list allowed_domains: (optional) A list of the allowed domains to
                                 crawl. This ensures that the crawler does not
                                 attempt to crawl the whole web. If not
                                 specified, it defaults to the domains of the
                                 URLs provided in ``sitemap_urls`` and/or
                                 ``url_list``.
    :param bool follow_links: Defaults to False. Whether or not to follow links
                              on crawled pages.
    :param str output_file: The path to the output of the crawl. Supported
                            formats 'csv', 'json', 'jsonlines', 'jl', 'xml',
                            'marshal', 'pickle'.
    :param dict custom_settings: An optional dictionary of settings to
                                 override.
    """
    if sitemap_urls is None or isinstance(sitemap_urls, str):
        sitemap_urls = [str(sitemap_urls)]  # call str() in case it was None
    if isinstance(url_list, str):
        url_list = [url_list]
    if url_list is None:
        url_list = []
    if isinstance(allowed_domains, str):
        allowed_domains = [allowed_domains]

    if allowed_domains is None:
        sitemap_domains = {urlparse(url).netloc for url in sitemap_urls}
        url_list_domains = {urlparse(url).netloc for url in url_list}
        allowed_domains = list(sitemap_domains) + list(url_list_domains)
    lastmods = []
    if sitemap_urls[0] != 'None':
        sitemap_df = pd.concat([sitemap_to_df(sitemap)
                                for sitemap in sitemap_urls],
                               ignore_index=True)
        url_list = sitemap_df['loc'].tolist() + url_list
        if 'lastmod' in sitemap_df:
            lastmods = sitemap_df['lastmod'].astype(str).tolist()

    command = ['scrapy', 'runspider', spider_path,
               '-a', 'url_list=' + ','.join(url_list),
               '-a', 'lastmods=' + ','.join(lastmods),
               '-a', 'allowed_domains=' + ','.join(allowed_domains),
               '-a', 'follow_links=' + str(follow_links),
               '-o', output_file]
    # return command
    print(command)
    subprocess.run(command)
