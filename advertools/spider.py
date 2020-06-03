"""
🕷 Python SEO Crawler / Spider
==============================

A straightforward crawler to analyze SEO and content of pages and websites.

This is provided by the :func:`crawl` function which is customized for SEO and
content analysis usage, and is highly configurable. The crawler uses
`Scrapy <https://scrapy.org/>`_ so you get all the power that it provides in
terms of performance, speed, as well as flexibility and customization.

There are two main approaches to crawl:

1. **Discovery:** You know the website to crawl, so you provide a ``url_list``
   (one or more URLs), and you want the crawler to go through the whole
   website(s) by following all available links.

2. **Pre-determined:** You have a known set of URLs that you want to crawl and
   analyze, without following links or discovering new URLs.

Discovery Crawling Approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest way to use the function is to provide a list of one or more URLs
and the crawler will go through all of the reachable pages.

.. code-block:: python

   >>> crawl('https://example.com', 'my_output_file.csv', follow_links=True)

That's it!

What this does:

* Check the site's robots.txt file and get the crawl rules, which means that
  your crawl will be affected by these rules and the user agent you are using.
  Check the details below on how to change settings and user agents to control
  this.
* Starting with the provided URL(s) go through all links and parse pages.
* For each URL extract the most important SEO elements.
* Save them to ``output_file`` in the specified format.
* The column headers of the output file (if you specify csv) would be the names
  of the elements.

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

================= =============================================================
Element           Remarks
================= =============================================================
url               The URL requested
url_redirected_to The actual URL that was parsed, usually but not always the
                  same as `url`
title             The <title> tag(s)
meta_desc         Meta description
h1                `<h1>` tag(s)
h2                `<h2>` tag(s)
h3                `<h3>` tag(s)
body_text         The text in the <p> tags
size              The page size in bytes
resp_meta_*       Several metadata for the response download_latency, timeout
                  etc.
status            Response status (200, 301, 302, 404, etc.)
links_url         The URLs of the links on the page
links_text        The link text (anchor text)
links_fragment    The fragment part of the link (#fragment)
links_nofollow    Boolean, whether or not the link is a nofllow link
img_src           The ``src`` attribute of images
img_alt           The ``alt`` attribute if available or an empty string
page_depth        The depth of the crawled page
ip_address        IP address
crawl_time        Date and time the page was crawled
resp_headers_*    All available response headers (last modified, server, etc.)
request_headers_* All available request headers (user-agent, encoding, etc.)
================= =============================================================

.. note::

    All elements that may appear multiple times on a page (like header tags, or
    images, for example), will be joined with two "@" signs `@@`. For example,
    **"first H2 tag@@second H2 tag@@third tag"** and so on.
    Once you open the file, you simply have to split by `@@` to get the
    elements as a list.

Here is a sample file of a crawl of this site (output truncated for
readability):

.. code-block:: python

    >>> import pandas as pd
    >>> site_crawl = pd.read_csv('path/to/file.csv')
    >>> site_crawl.head()
                                   url               url_redirected_to                           title                       meta_desc                              h1                              h2                              h3                        body_text  size  download_timeout              download_slot  download_latency  redirect_times  redirect_ttl                   redirect_urls redirect_reasons  depth  status                      links_href                      links_text                         img_src                         img_alt    ip_address           crawl_time              resp_headers_date resp_headers_content-type     resp_headers_last-modified resp_headers_vary    resp_headers_x-ms-request-id resp_headers_x-ms-version resp_headers_x-ms-lease-status resp_headers_x-ms-blob-type resp_headers_access-control-allow-origin   resp_headers_x-served resp_headers_x-backend resp_headers_x-rtd-project resp_headers_x-rtd-version         resp_headers_x-rtd-path  resp_headers_x-rtd-domain resp_headers_x-rtd-version-method resp_headers_x-rtd-project-method resp_headers_strict-transport-security resp_headers_cf-cache-status  resp_headers_age           resp_headers_expires resp_headers_cache-control          resp_headers_expect-ct resp_headers_server   resp_headers_cf-ray      resp_headers_cf-request-id          request_headers_accept request_headers_accept-language      request_headers_user-agent request_headers_accept-encoding          request_headers_cookie
    0   https://advertools.readthedocs  https://advertools.readthedocs            advertools —  Python  Get productive as an online ma  advertools@@Indices and tables  Online marketing productivity                              NaN   Generate keywords for SEM camp   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN  https://advertools.readthedocs            [302]    NaN     NaN  #@@readme.html@@advertools.kw_  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:35  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  720a8581-501e-0043-01a2-2e77d2                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca7dbaa7e9e-BUD  02d86a3cea00007e9edb0cf2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    1   https://advertools.readthedocs  https://advertools.readthedocs            advertools —  Python                             NaN                      advertools         Change Log - advertools  0.9.1 (2020-05-19)@@0.9.0 (202   Ability to specify robots.txt    NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  4f7bea3b-701e-0039-3f44-2f1d9f                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007h                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bcab7e9e-BUD  02d86a3e0e00007e9edb0d72000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    2   https://advertools.readthedocs  https://advertools.readthedocs            advertools —  Python  Get productive as an online ma  advertools@@Indices and tables  Online marketing productivity                              NaN   Generate keywords for SEM camp   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  #@@readme.html@@advertools.kw_  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  98b729fa-e01e-00bf-24c3-2e494d                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bf26d423-BUD  02d86a3e150000d423322742000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    3   https://advertools.readthedocs  https://advertools.readthedocs    advertools package —  Python                             NaN              advertools package     Submodules@@Module contents                             NaN   Top-level package for advertoo   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:25 GMT   Accept-Encoding  7a28ef3b-801e-00c2-24c3-2ed585                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web000079                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bddb7ec2-BUD  02d86a3e1300007ec2a808a2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    4   https://advertools.readthedocs  https://advertools.readthedocs   Python Module Index —  Python                             NaN             Python Module Index                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               _static/minus.png                               -  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  75911c9e-201e-00e6-34c3-2e4ccb                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007g                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9b91fd437-BUD  02d86a3e140000d437b81532000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    66  https://advertools.readthedocs  https://advertools.readthedocs  advertools.url_builders —  Pyt                             NaN  Source code for advertools.url                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:38 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  d99f2368-c01e-006f-18c3-2ef5ef                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007a                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:38 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbbb8afd437-BUD  02d86a494f0000d437b828b2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    67  https://advertools.readthedocs  https://advertools.readthedocs  advertools.kw_generate —  Pyth                             NaN  Source code for advertools.kw_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  85855c48-c01e-00ce-13c3-2e3b74                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007g                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd980bd423-BUD  02d86a4a7f0000d423323b42000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    68  https://advertools.readthedocs  https://advertools.readthedocs  advertools.ad_from_string —  P                             NaN  Source code for advertools.ad_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  b0aef497-801e-004a-1647-2f6d5c                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007k                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd980cd423-BUD  02d86a4a7f0000d423209db2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    69  https://advertools.readthedocs  https://advertools.readthedocs  advertools.ad_create —  Python                             NaN  Source code for advertools.ad_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  9dfdd38a-101e-00a1-7ec3-2e93a0                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd99847ec2-BUD  02d86a4a7f00007ec2a811f2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    70  https://advertools.readthedocs  https://advertools.readthedocs      advertools.emoji —  Python                             NaN  Source code for advertools.emo                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:40  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  2ad504a1-101e-000b-03c3-2e454f                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web000079                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd9fb97e9e-BUD  02d86a4a7f00007e9edb13a2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004

Pre-Determined Crawling Approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you might have a fixed set of URLs for which you want to scrape and
analyze SEO or content performance. Some ideas:

SERP Data
---------
Let's say you just ran :ref:`serp_goog <serp>` and got a bunch of top-ranking
pages that you would like to analyze, and see how that relates to their SERP
ranking.

You simply provide the ``url_list`` parameter and again specify the
``output_file``. This will only crawl the specified URLs, and will not follow
any links.

Now you have the SERP DataFrame, as well as the crawl output file. All you have
to do is to merge them by the URL columns, and end up with a richer dataset

News Articles
-------------
You want to follow the latest news of a certain publication, and you extract
their latest news URLs from their news sitemap using
:ref:`sitemap_to_df <sitemaps>` . You provide those URLs and crawl them only.

Google Analytics / Google Search Console
----------------------------------------
Since they provide reports for URLs, you can also combine them with the ones
crawled and end up with a better perspective. You might be interested in
knowing more about high bounce-rate pages, pages that convert well, pages that
get less traffic than you think they should and so on. You can simply export
those URLs and crawl them.

Any tool that has data about a set of URLs can be used.

Again running the function is as simple as providing a list of URLs, as well as
a filepath where you want the result saved.

.. code-block:: python

    >>> crawl(url_list, output_file, follow_links=False)

The difference between the two approaches, is the simple parameter
``follow_links``. If you keep it as ``False`` (the default), the crawler
will only go through the provided URLs. Otherwise, it will discover pages by
following links on pages that it crawls. So how do you make sure that the
crawler doesn't try to crawl the whole web when ``follow_links`` is `True`?
The ``allowed_domains`` parameter gives you the ability to control this,
although it is and optional parameter. If you don't specify it, then it will
default to only the domains in the ``url_list``. It's important to note that
you have to set this parameter if you have certain sub-domains that you want to
crawl.

CSS and XPath Selectors
^^^^^^^^^^^^^^^^^^^^^^^

The above approaches are generic, and are useful for an exploratory SEO audit
and the output is helpful for most cases.

But what if you want to extract special elements that are not included in the
default output? This is extremely important, as there are key elements on pages
that you need to additionally extract and analyze. Some examples might be tags,
prices, social media shares, product price or availability, comments, and
pretty much any element on a page that might be of interest to you.

For this you can use two special arguments for CSS and/or XPath selectors. You
simply provide a dictionary `{'name_1': 'selector_1', 'name_2': 'selector_2'}`
where the keys become the column names, and the values (selectors) will be
used to extract the required elements.

I mostly rely on `SlectorGadget <https://selectorgadget.com/>`_ which is a
really great tool for getting the CSS/XPath selecotrs of required elements.
In some pages it can get really tricky to figure that out. Other resources for
learning more about selectors:

* `Scrapy's documentaion for selectors <https://docs.scrapy.org/en/latest/topics/selectors.html>`_
* `CSS Selector Reference on W3C <https://www.w3schools.com/cssref/css_selectors.asp>`_
* `XPath tutorial on W3C <https://www.w3schools.com/xml/xpath_intro.asp>`_

Once you have determined the elements that you want to extract and figured out
what their names are going to be, you simply pass them as arguments to
``css_selectors`` and/or ``xpath_selectors`` as dictionaries, as decribed
above.

Let's say you want to extract the links in the sidebar of this page. By default
you would get all the links from the page, but you want to put those in the
sidebar in a separate column. It seems that the CSS selector for them is
`.toctree-l1 .internal`, and the XPath equivalent is
`//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]`.
Note that this selects the *element* (the whole link object), which is not
typically what you might be interested in.

So with CSS you need to append `::text` or `::attr(href)` if you want the text of
the links or the `href` attribute respectively. Similarly with XPath, you will
need to append `/text()` or `/@href` to the selector to get the same.

>>> crawl('https://advertools.readthedocs.io/en/master/advertools.spider.html',
...       'output_file.csv',
...       css_selectors={'sidebar_links': '.toctree-l1 .internal::text',
...                      'sidebar_links_url': '.toctree-l1 .internal::attr(href)'})

Or, instead of ``css_selectors`` you can add a similar dictionary for the
``xpath_selectors`` argument:

>>> crawl('https://advertools.readthedocs.io/en/master/advertools.spider.html',
...       'output_file.csv',
...       xpath_selectors={'sidebar_links': '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/text()',
...                        'sidebar_links_url': '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/@href'})

Spider Custom Settings and Additional Functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to what you can control regarding the items you can extract, you
can also customize the behaviour of the spider and set rules for crawling so
you can control it even further.

This is provided by the ``custom_settings`` parameter. It is optional, and
takes a dictionary of settings and their values. Scrapy provides a very large
number of settings, and they are all available through this parameter
(assuming some conditions for some of the settings).

Here are some examples that you might find interesting:

* `CONCURRENT_REQUESTS_PER_DOMAIN` Defaults to 8, and controls the number of
  simultaneous requests to be performed for each domain. You might want to
  lower this if you don't want to put too much pressure on the website's
  server, and you probably don't want to get blocked!
* `DEFAULT_REQUEST_HEADERS` You can change this if you need to.
* `DEPTH_LIMIT` How deep your crawl will be allowed. The default has no limit.
* `DOWNLOAD_DELAY` Similar to the first option. Controls the amount of time in
  seconds for the crawler to wait between consecutive pages of the same website.
  It can also take fractions of a second (0.4, 0.75, etc.)
* `LOG_FILE` If you want to save your crawl logs to a file, you can provide a
  path to it here.
* `USER_AGENT` If you want to identify yourself differently while crawling.
* `CLOSESPIDER_ERRORCOUNT`, `CLOSESPIDER_ITEMCOUNT`, `CLOSESPIDER_PAGECOUNT`,
  `CLOSESPIDER_TIMEOUT` Stop crawling after that many errors, items, pages, or
  seconds. These can be very useful to limit your crawling in certain cases.
  I particularly like to use `CLOSESPIDER_PAGECOUNT` when exploring a new
  website, and also to make sure that my selectors are working as expected. So
  for your first few crawls you might set this to one hundred for example and
  explore the crawled pages. Then when you are confident things are working
  fine, you can remove this restriction. `CLOSESPIDER_ERRORCOUNT` can also be
  very useful while exploring, just in case you get unexpected errors.

**Usage**

A very simpl dictionary to be added to your function call:

>>> crawl('http://exmaple.com', 'outpuf_file.csv',
...       custom_settings={'CLOSESPIDER_PAGECOUNT': 100,
...                        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
...                        'USER_AGENT': 'custom-user-agent'})

Please refer to the `spider settings documentation <https://docs.scrapy.org/en/latest/topics/settings.html>`_
for the full details.

"""
import datetime
import json
import os
import subprocess

from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import scrapy.logformatter as formatter
import advertools as adv

spider_path = adv.__path__[0] + '/spider.py'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',

BODY_TEXT_SELECTOR = '//body//span//text() | //body//p//text() | //body//li//text()'

formatter.SCRAPEDMSG = "Scraped from %(src)s" + os.linesep
formatter.DROPPEDMSG = "Dropped: %(exception)s" + os.linesep
formatter.DOWNLOADERRORMSG_LONG = "Error downloading %(request)s" + os.linesep

le = LinkExtractor()


class SEOSitemapSpider(Spider):
    name = 'seo_sitemap_spider'
    follow_links = False
    css_selectors = {}
    xpath_selectors = {}
    custom_settings = {
        'USER_AGENT': user_agent,
        'ROBOTSTXT_OBEY': True,
        'HTTPERROR_ALLOW_ALL': True,
    }

    def __init__(self, url_list=None, allowed_domains=None,
                 css_selectors=None, xpath_selectors=None,
                 follow_links=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(url_list.split(',')))
        self.allowed_domains = json.loads(json.dumps(allowed_domains.split(',')))
        self.follow_links = eval(json.loads(json.dumps(follow_links)))
        self.css_selectors = eval(json.loads(json.dumps(css_selectors)))
        self.xpath_selectors = eval(json.loads(json.dumps(xpath_selectors)))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        links = le.extract_links(response)
        if self.css_selectors:
            css_selectors = {key: '@@'.join(response.css('{}'.format(val)).getall())
                             for key, val in self.css_selectors.items()}
        else:
            css_selectors = {}

        if self.xpath_selectors:
            xpath_selectors = {key: '@@'.join(response.xpath('{}'.format(val)).getall())
                               for key, val in self.xpath_selectors.items()}
        else:
            xpath_selectors = {}

        yield dict(
            url=response.request.url,
            url_redirected_to=response.url,
            title='@@'.join(response.css('title::text').getall()),
            meta_desc=response.xpath("//meta[@name='description']/@content").get(),
            h1='@@'.join(response.css('h1::text').getall()),
            h2='@@'.join(response.css('h2::text').getall()),
            h3='@@'.join(response.css('h3::text').getall()),
            body_text=' '.join(response.xpath(BODY_TEXT_SELECTOR).extract()),
            size=len(response.body),
            **css_selectors,
            **xpath_selectors,
            **{'resp_meta_' + k: v
               for k, v in response.meta.items()},
            status=response.status,
            links_url='@@'.join(link.url for link in links),
            links_text='@@'.join(link.text for link in links),
            links_fragment='@@'.join(link.fragment for link in links),
            links_nofollow='@@'.join(str(link.nofollow) for link in links),
            img_src='@@'.join([im.attrib.get('src') or ''
                               for im in response.css('img')]),
            img_alt='@@'.join([im.attrib.get('alt') or ''
                               for im in response.css('img')]),
            ip_address=response.ip_address,
            crawl_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            **{'resp_headers_' + k: v
               for k, v in response.headers.to_unicode_dict().items()},
            **{'request_headers_' + k: v
               for k, v in response.request.headers.to_unicode_dict().items()},
        )
        if self.follow_links:
            next_pages = [link.url for link in links]
            if next_pages:
                for page in next_pages:
                    yield Request(page, callback=self.parse)


def crawl(url_list, output_file, follow_links=False, css_selectors=None,
          xpath_selectors=None, custom_settings=None, allowed_domains=None):
    """
    Crawl a website's URLs based on the given :attr:`url_list`

    :param url,list url_list: One or more URLs to crawl. If ``follow_links``
                          is True, the crawler will start with these URLs and
                          follow all links on pages recursively.
    :param str output_file: The path to the output of the crawl. Supported
                            formats: `csv`, `json`, `jsonlines`, `jl`, `xml`,
                            `marshal`, `pickle`.
    :param bool follow_links: Defaults to False. Whether or not to follow links
                              on crawled pages.
    :param dict css_selectors: A dictionary mapping names to CSS selectors. The
                               names will become column headers, and the
                               selectors will be used to extract the required
                               data/content.
    :param dict xpath_selectors: A dictionary mapping names to XPath selectors.
                                 The names will become column headers, and the
                                 selectors will be used to extract the required
                                 data/content.
    :param dict custom_settings: A dictionary of optional custom settings that
                                 you might want to add to the spider's
                                 functionality. There are over 170 settings for
                                 all kinds of options. For details please
                                 refer to the `spider settings <https://docs.scrapy.org/en/latest/topics/settings.html>`_
                                 documentation.
    :param list allowed_domains: (optional) A list of the allowed domains to
                                 crawl. This ensures that the crawler does not
                                 attempt to crawl the whole web. If not
                                 specified, it defaults to the domains of the
                                 URLs provided in ``url_list``. You can use it
                                 for sub-domains if you want them to be crawled
                                 as they will not be crawled if not specified.
    :Examples:

    Crawl a website and let the crawler discover as many pages as available

    >>> crawl('http://example.com', 'output_file.csv', follow_links=True)

    Crawl a known set of pages (on a single or multiple sites) without
    following links (just crawl the specified pages):

    >>> crawl(['http://exmaple.com/product', 'http://exmaple.com/product2',
    ...        'https://anotherexample.com', 'https://anotherexmaple.com/hello'],
    ...        'output_file.csv', follow_links=False)

    Crawl a website, and in addition to standard SEO elements, also get the
    required CSS selectors.
    Here we will get three additional columns `price`, `author`, and
    `author_url`. Note that you need to specify if you want the text attribute
    or the `href` attribute if you are working with links (and all other
    selectors).

    >>> crawl('http://example.com', 'output_file.csv',
    ...       css_selectors={'price': '.a-color-price::text',
    ...                      'author': '.contributorNameID::text',
    ...                      'author_url': '.contributorNameID::attr(href)'})
    """
    if isinstance(url_list, str):
        url_list = [url_list]
    if isinstance(allowed_domains, str):
        allowed_domains = [allowed_domains]

    if allowed_domains is None:
        allowed_domains = {urlparse(url).netloc for url in url_list}
    settings_list = []
    if custom_settings is not None:
        for key, val in custom_settings.items():
            setting = '='.join([key, str(val)])
            settings_list.extend(['-s', setting])

    command = ['scrapy', 'runspider', spider_path,
               '-a', 'url_list=' + ','.join(url_list),
               '-a', 'allowed_domains=' + ','.join(allowed_domains),
               '-a', 'follow_links=' + str(follow_links),
               '-a', 'css_selectors=' + str(css_selectors),
               '-a', 'xpath_selectors=' + str(xpath_selectors),
               '-o', output_file] + settings_list
    subprocess.run(command)
