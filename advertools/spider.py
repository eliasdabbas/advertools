"""
.. _crawl:

🕷 Python SEO Crawler / Spider
==============================

A customizable crawler to analyze SEO and content of pages and websites.

This is provided by the :func:`crawl` function which is customized for SEO and
content analysis usage, and is highly configurable. The crawler uses
`Scrapy <https://scrapy.org/>`_ so you get all the power that it provides in
terms of performance, speed, as well as flexibility and customization.

There are two main approaches to crawl:

1. **Discovery (spider mode):** You know the website to crawl, so you provide a
   ``url_list`` (one or more URLs), and you want the crawler to go through the whole
   website(s) by following all available links.

2. **Pre-determined (list mode):** You have a known set of URLs that you
   want to crawl and analyze, without following links or discovering new URLs.

Discovery Crawling Approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest way to use the function is to provide a list of one or more URLs
and the crawler will go through all of the reachable pages.

.. code-block:: python

   >>> import advertools as adv
   >>> adv.crawl('https://example.com', 'my_output_file.jl', follow_links=True)

That's it! To open the file:

.. code-block:: python

   >>> import pandas as pd
   >>> crawl_df = pd.read_json('my_output_file.jl', lines=True)


What this does:

* Check the site's robots.txt file and get the crawl rules, which means that
  your crawl will be affected by these rules and the user agent you are using.
  Check the details below on how to change settings and user agents to control
  this.
* Starting with the provided URL(s) go through all links and parse pages.
* For each URL extract the most important SEO elements.
* Save them to ``my_output_file.jl``.
* The column headers of the output file (once you import it as a DataFrame)
  would be the names of the elements (title, h1, h2, etc.).

Jsonlines is the supported output format because of its flexibility in allowing
different values for different scraped pages, and appending indepentent items
to the output files.

.. note::

    When the crawler parses pages it saves the data to the specified file by
    appending, and not overwriting. Otherwise it would have to store all the
    data in memory, which might crash your computer. A good practice is to have
    a separate ``output_file`` for every crawl with a descriptive name
    `sitename_crawl_YYYY_MM_DD.jl` for example. If you use the same file you
    will probably get duplicate data in the same file.

Extracted On-Page SEO Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The names of these elements become the headers (column names) of the
``output_file``.

================= =============================================================
Element           Remarks
================= =============================================================
url               The response URL that was actually crawled. This might be different from the rquested URL in case of a redirect for example. Please check the ``redirect_*`` columns for more information.
title             The <title> tag(s)
viewport          The `viewport` meta tag if available
charset           The `charset` meta tag if available
meta_desc         Meta description
canonical         The canonical tag if available
alt_href          The `href` attribute of rel=alternate tags
alt_hreflang      The language codes of the alternate links
og:*              Open Graph data
twitter:*         Twitter card data
jsonld_*          JSON-LD data if available. In case multiple snippets occur,
                  the respective column names will include a number to
                  distinguish them, `jsonld_1_{item_a}, jsonld_1_{item_b}`,
                  etc. Note that the first snippet will not contain a number,
                  so the numbering starts with "1", starting from the second
                  snippet. The same applies to OG and Twitter cards.
h1...h6           `<h1>` through `<h6>` tag(s), whichever is available
links_url         The URLs of the links on the page
links_text        The link text (anchor text)
links_nofollow    Boolean, whether or not the link is a nofllow link. Note that
                  this only tells if the link itself contains a rel="nofollow"
                  attribute. The page might indicate "nofollow" using meta
                  robots or X-Robots-Tag, which you have to check separately.
nav_links_text    The anchor text of all links in the `<nav>` tag if
                  available
nav_links_url     The links in the `<nav>` tag if available
header_links_text The anchor text of all links in the `<header>` tag if
                  available
header_links_url  The links in the `<header>` tag if available
footer_links_text The anchor text of all links in the `<footer>` tag if
                  available
footer_links_url  The links in the `<footer>` tag if available
body_text         The text in the <p>, <span>, and <li> tags within <body>
size              The page size in bytes
download_latency  The amount of time it took to get the page HTML, in seconds.
download_timout   The amount of time (in secs) that the downloader will wait
                  before timing out. Defaults to 180.
redirect_times    The number of times the pages was redirected if available
redirect_ttl      The default maximum number of redirects the crawler allows
redirect_urls     The chain of URLs from the requested URL to the one actually
                  fetched
redirect_reasons  The type of redirection(s) 301, 302, etc.
depth             The depth of the current URL, relative to the first URLs
                  where crawling started. The first pages to be crawled have a
                  depth of zero, pages linked from there, a depth of one, etc.
status            Response status code (200, 404, etc.)
img_*             All available ``<img>`` tag attributes. 'alt', 'crossorigin',
                  'height', 'ismap', 'loading', 'longdesc', 'referrerpolicy',
                  'sizes', 'src', 'srcset', 'usemap',  and 'width' (excluding
                  global HTML attributes like ``style`` and ``draggable``)
ip_address        IP address
crawl_time        Date and time the page was crawled
resp_headers_*    All available response headers (last modified, server, etc.)
request_headers_* All available request headers (user-agent, encoding, etc.)
================= =============================================================

.. note::

    All elements that may appear multiple times on a page (like heading tags,
    or images, for example), will be joined with two "@" signs `@@`. For
    example, **"first H2 tag@@second H2 tag@@third tag"** and so on.
    Once you open the file, you simply have to split by `@@` to get the
    elements as a list.

Here is a sample file of a crawl of this site (output truncated for
readability):

.. code-block:: python

    >>> import pandas as pd
    >>> site_crawl = pd.read_json('path/to/file.jl', lines=True)
    >>> site_crawl.head()
                                   url                           title                       meta_desc                              h1                              h2                              h3                        body_text  size  download_timeout              download_slot  download_latency  redirect_times  redirect_ttl                   redirect_urls redirect_reasons  depth  status                      links_href                      links_text                         img_src                         img_alt    ip_address           crawl_time              resp_headers_date resp_headers_content-type     resp_headers_last-modified resp_headers_vary    resp_headers_x-ms-request-id resp_headers_x-ms-version resp_headers_x-ms-lease-status resp_headers_x-ms-blob-type resp_headers_access-control-allow-origin   resp_headers_x-served resp_headers_x-backend resp_headers_x-rtd-project resp_headers_x-rtd-version         resp_headers_x-rtd-path  resp_headers_x-rtd-domain resp_headers_x-rtd-version-method resp_headers_x-rtd-project-method resp_headers_strict-transport-security resp_headers_cf-cache-status  resp_headers_age           resp_headers_expires resp_headers_cache-control          resp_headers_expect-ct resp_headers_server   resp_headers_cf-ray      resp_headers_cf-request-id          request_headers_accept request_headers_accept-language      request_headers_user-agent request_headers_accept-encoding          request_headers_cookie
    0   https://advertools.readthedocs            advertools —  Python  Get productive as an online ma  advertools@@Indices and tables  Online marketing productivity                              NaN   Generate keywords for SEM camp   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN  https://advertools.readthedocs            [302]    NaN     NaN  #@@readme.html@@advertools.kw_  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:35  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  720a8581-501e-0043-01a2-2e77d2                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca7dbaa7e9e-BUD  02d86a3cea00007e9edb0cf2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    1   https://advertools.readthedocs            advertools —  Python                             NaN                      advertools         Change Log - advertools  0.9.1 (2020-05-19)@@0.9.0 (202   Ability to specify robots.txt    NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  4f7bea3b-701e-0039-3f44-2f1d9f                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007h                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bcab7e9e-BUD  02d86a3e0e00007e9edb0d72000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    2   https://advertools.readthedocs            advertools —  Python  Get productive as an online ma  advertools@@Indices and tables  Online marketing productivity                              NaN   Generate keywords for SEM camp   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  #@@readme.html@@advertools.kw_  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  98b729fa-e01e-00bf-24c3-2e494d                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bf26d423-BUD  02d86a3e150000d423322742000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    3   https://advertools.readthedocs    advertools package —  Python                             NaN              advertools package     Submodules@@Module contents                             NaN   Top-level package for advertoo   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:25 GMT   Accept-Encoding  7a28ef3b-801e-00c2-24c3-2ed585                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web000079                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9bddb7ec2-BUD  02d86a3e1300007ec2a808a2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    4   https://advertools.readthedocs   Python Module Index —  Python                             NaN             Python Module Index                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  index.html@@readme.html@@adver  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               _static/minus.png                               -  104.17.32.82  2020-05-21 10:39:36  Thu, 21 May 2020 10:39:35 GMT                 text/html  Wed, 20 May 2020 12:26:23 GMT   Accept-Encoding  75911c9e-201e-00e6-34c3-2e4ccb                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007g                 advertools                     master  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:35 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596daca9b91fd437-BUD  02d86a3e140000d437b81532000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    66  https://advertools.readthedocs  advertools.url_builders —  Pyt                             NaN  Source code for advertools.url                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:38 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  d99f2368-c01e-006f-18c3-2ef5ef                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007a                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:38 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbbb8afd437-BUD  02d86a494f0000d437b828b2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    67  https://advertools.readthedocs  advertools.kw_generate —  Pyth                             NaN  Source code for advertools.kw_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  85855c48-c01e-00ce-13c3-2e3b74                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007g                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd980bd423-BUD  02d86a4a7f0000d423323b42000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    68  https://advertools.readthedocs  advertools.ad_from_string —  P                             NaN  Source code for advertools.ad_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  b0aef497-801e-004a-1647-2f6d5c                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007k                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd980cd423-BUD  02d86a4a7f0000d423209db2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    69  https://advertools.readthedocs  advertools.ad_create —  Python                             NaN  Source code for advertools.ad_                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:39  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  9dfdd38a-101e-00a1-7ec3-2e93a0                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web00007c                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd99847ec2-BUD  02d86a4a7f00007ec2a811f2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004
    70  https://advertools.readthedocs      advertools.emoji —  Python                             NaN  Source code for advertools.emo                             NaN                             NaN            © Copyright 2020, Eli   NaN               NaN  advertools.readthedocs.io               NaN             NaN           NaN                             NaN              NaN    NaN     NaN  ../../index.html@@../../readme  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                             NaN                             NaN  104.17.32.82  2020-05-21 10:39:40  Thu, 21 May 2020 10:39:39 GMT                 text/html  Wed, 20 May 2020 12:26:36 GMT   Accept-Encoding  2ad504a1-101e-000b-03c3-2e454f                2009-09-19                       unlocked                   BlockBlob                                        *  Nginx-Proxito-Sendfile              web000079                 advertools                     latest  /proxito/media/html/advertools  advertools.readthedocs.io                              path                         subdomain         max-age=31536000; includeSubDo                          HIT               NaN  Thu, 21 May 2020 11:39:39 GMT       public, max-age=3600  max-age=604800, report-uri="ht          cloudflare  596dacbd9fb97e9e-BUD  02d86a4a7f00007e9edb13a2000000  text/html,application/xhtml+xm                              en  Mozilla/5.0 (Windows NT 10.0;                    gzip, deflate  __cfduid=d76b68d148ddec1efd004

Pre-Determined Crawling Approach (List Mode)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

    >>> adv.crawl(url_list, 'output_file.jl', follow_links=False)

The difference between the two approaches, is the simple parameter
``follow_links``. If you keep it as ``False`` (the default), the crawler
will only go through the provided URLs. Otherwise, it will discover pages by
following links on pages that it crawls. So how do you make sure that the
crawler doesn't try to crawl the whole web when ``follow_links`` is `True`?
The ``allowed_domains`` parameter gives you the ability to control this,
although it is an optional parameter. If you don't specify it, then it will
default to only the domains in the ``url_list`` and their sub-domains if any.
It's important to note that you have to set this parameter if you want to only
crawl certain sub-domains.

Custom Extraction with CSS and XPath Selectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above approaches are generic, and are useful for exploratory SEO audits
and the output is helpful for most cases.

But what if you want to extract special elements that are not included in the
default output? This is extremely important, as there are key elements on pages
that you need to additionally extract and analyze. Some examples might be tags,
prices, social media shares, product price or availability, comments, and
pretty much any element on a page that might be of interest to you.

For this you can use two special parameters for CSS and/or XPath selectors. You
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

So with CSS you need to append `::text` or `::attr(href)` if you want the text
of the links or the `href` attribute respectively. Similarly with XPath, you
will need to append `/text()` or `/@href` to the selector to get the same.

>>> adv.crawl(
...     "https://advertools.readthedocs.io/en/master/advertools.spider.html",
...     "output_file.jl",
...     css_selectors={
...         "sidebar_links": ".toctree-l1 .internal::text",
...         "sidebar_links_url": ".toctree-l1 .internal::attr(href)",
...     },
... )

Or, instead of ``css_selectors`` you can add a similar dictionary for the
``xpath_selectors`` argument:

>>> adv.crawl(
...     "https://advertools.readthedocs.io/en/master/advertools.spider.html",
...     "output_file.jl",
...     xpath_selectors={
...         "sidebar_links": '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/text()',
...         "sidebar_links_url": '//*[contains(concat( " ", @class, " " ), concat( " ", "toctree-l1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "internal", " " ))]/@href',
...     },
... )

Customizing the Crawling Behavior while Following Links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you set ``follow_links=True`` you might want to restrict this option for a
more customized crawl. This means you can decide whether to include or exclude
certain links based on certain conditions based on URL parameters and/or URL
regex patterns.

URL Query Parameters
--------------------

Two options are available for this:

1. ``exclude_url_params``: By providing a list of URL parameters, any link that
contains any of the parameters will not be followed. For example if you set
this option to ['price', 'country'], and the page currently being crawled
contains three links:

  * **/shoes/model_a?price=10&country=us**: Contains both parameters, will not be followed.
  * **/shoes/model_a?price=10**: Contains one of the parameters, will not be followed.
  * **/shoes/model_b?color=black**: Contains "color" which was not listed, will be followed

To make this efficient, and in case you want to skip all links that contain any
parameter, you can set this option to ``True``, and any link that contains any
URL parameter will not be followed ``exclude_url_params=True``


2. ``include_url_params``: Similarly, you can choose the parameters that links
should contain in order for them to be followed. If a link contains any of the
listed parameters, that link will be followed. Even though this option is
straightforward, it might give you unexpected results. If you set the
parameters to include as ['price'] for example, and you start crawling from a
page that doesn't have any link containing that parameter, crawling will stop.
Yet, the website might have many links with that parameter. Please keep this in
mind, and remember that reasoning about the exclude option is easier than the
include option for this reason/example.

URL Regex Patterns
------------------

You might want even more granular control over which links to follow, and might
be interested in other URL properties than their query parameters. You have two
simple options to include/exclude links based on whether they match a certain
regex pattern.

1. ``exclude_url_regex``: Enter a regex, and the links will be checked if they
match it. If they do, they will not be followed, if not they will.

2. ``include_url_regex``: This is similar but tells the crawler which links to
follow, based on whether or not they match the regex. This option also has the
same potentially tricky behavior like the ``include_url_params`` option.

Here is a simple example showing how you might control following links using
all four options:

.. code-block::

    import advertools as adv
    adv.crawl('https://example.com', 'output_file.jl', follow_links=True,

              # don't follow links containing any of these parameters:
              exclude_url_params=['price', 'region'],
              # follow links containing any of these parameters:
              include_url_params=['source'],
              # don't follow links that contain the pattern "/fr/" or "/de/":
              exclude_url_regex='/fr/|/de/',
              # follow links that contain the pattern "/shop/":
              include_url_regex='/shop/'
              )

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
  seconds for the crawler to wait between consecutive pages of the same
  website. It can also take fractions of a second (0.4, 0.75, etc.)
* `LOG_FILE` If you want to save your crawl logs to a file, which is strongly
  recommended, you can provide a path to it here.
* `USER_AGENT` If you want to identify yourself differently while crawling.
  This is affected by the robots.txt rules, so you would be potentially
  allowed/disallowed from certain pages based on your user-agent.
* `CLOSESPIDER_ERRORCOUNT`, `CLOSESPIDER_ITEMCOUNT`, `CLOSESPIDER_PAGECOUNT`,
  `CLOSESPIDER_TIMEOUT` Stop crawling after that many errors, items, pages, or
  seconds. These can be very useful to limit your crawling in certain cases.
  I particularly like to use `CLOSESPIDER_PAGECOUNT` when exploring a new
  website, and also to make sure that my selectors are working as expected. So
  for your first few crawls you might set this to five hundred for example and
  explore the crawled pages. Then when you are confident things are working
  fine, you can remove this restriction. `CLOSESPIDER_ERRORCOUNT` can also be
  very useful while exploring, just in case you get unexpected errors.

The next page contains a number of :ref:`strategies and recipes for crawling <crawl_strategies>`
with code examples and explanations.

**Usage**

A very simple dictionary to be added to your function call:

>>> adv.crawl(
...     "http://exmaple.com",
...     "outpuf_file.jl",
...     custom_settings={
...         "CLOSESPIDER_PAGECOUNT": 100,
...         "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
...         "USER_AGENT": "custom-user-agent",
...     },
... )

Please refer to the `spider settings documentation <https://docs.scrapy.org/en/latest/topics/settings.html>`_
for the full details.

"""  # noqa: E501

import datetime
import json
import logging
import platform
import re
import runpy
import subprocess
from urllib.parse import parse_qs, urlparse, urlsplit

import pandas as pd
import scrapy
import scrapy.logformatter as formatter
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.utils.response import get_base_url

import advertools as adv

if int(pd.__version__[0]) >= 1:
    from pandas import json_normalize
else:
    from pandas.io.json import json_normalize

from advertools import __version__ as adv_version

spider_path = adv.__path__[0] + "/spider.py"

user_agent = f"advertools/{adv_version}"

# BODY_TEXT_SELECTOR = "//body//span//text() | //body//p//text() | //body//li//text()"
BODY_TEXT_SELECTOR = "//body//*[self::a or self::abbr or self::address or self::b or self::blockquote or self::cite or self::code or self::dd or self::del or self::div or self::dl or self::dt or self::em or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::header or self::i or self::ins or self::kbd or self::li or self::mark or self::ol or self::p or self::pre or self::q or self::section or self::small or self::span or self::strong or self::sub or self::sup or self::time or self::u or self::ul][not(ancestor::area) and not(ancestor::aside) and not(ancestor::audio) and not(ancestor::button) and not(ancestor::caption) and not(ancestor::col) and not(ancestor::colgroup) and not(ancestor::datalist) and not(ancestor::details) and not(ancestor::embed) and not(ancestor::fieldset) and not(ancestor::footer) and not(ancestor::form) and not(ancestor::head) and not(ancestor::iframe) and not(ancestor::img) and not(ancestor::input) and not(ancestor::label) and not(ancestor::legend) and not(ancestor::link) and not(ancestor::map) and not(ancestor::meta) and not(ancestor::nav) and not(ancestor::noscript) and not(ancestor::object) and not(ancestor::optgroup) and not(ancestor::option) and not(ancestor::output) and not(ancestor::param) and not(ancestor::picture) and not(ancestor::script) and not(ancestor::select) and not(ancestor::source) and not(ancestor::style) and not(ancestor::svg) and not(ancestor::table) and not(ancestor::tbody) and not(ancestor::td) and not(ancestor::textarea) and not(ancestor::tfoot) and not(ancestor::th) and not(ancestor::thead) and not(ancestor::title) and not(ancestor::tr) and not(ancestor::track) and not(ancestor::video)]/text()"  # noqa: E501

_IMG_ATTRS = {
    "alt",
    "crossorigin",
    "decoding",
    "fetchpriority",
    "height",
    "ismap",
    "loading",
    "referrerpolicy",
    "sizes",
    "src",
    "srcset",
    "usemap",
    "width",
    # Depracated tags, also included for completeness and QA:
    "align",
    "border",
    "hspace",
    "longdesc",
    "name",
    "vspace",
}


def _crawl_or_not(
    url,
    exclude_url_params=None,
    include_url_params=None,
    exclude_url_regex=None,
    include_url_regex=None,
):
    qs = parse_qs(urlsplit(url).query)
    supplied_conditions = []
    if exclude_url_params is not None:
        if exclude_url_params is True and qs:
            return False
        if exclude_url_params is True and not qs:
            pass
        else:
            exclude_params_in_url = not bool(set(exclude_url_params).intersection(qs))
            supplied_conditions.append(exclude_params_in_url)

    if include_url_params is not None:
        include_params_in_url = bool(set(include_url_params).intersection(qs))
        supplied_conditions.append(include_params_in_url)

    if exclude_url_regex is not None:
        exclude_pattern_matched = not bool(re.findall(exclude_url_regex, url))
        supplied_conditions.append(exclude_pattern_matched)

    if include_url_regex is not None:
        include_pattern_matched = bool(re.findall(include_url_regex, url))
        supplied_conditions.append(include_pattern_matched)
    return all(supplied_conditions)


def _extract_images(response):
    page_has_images = response.xpath("//img")
    if page_has_images:
        img_df = pd.DataFrame([x.attrib for x in response.xpath("//img")])
        if "src" in img_df:
            img_df["src"] = [
                response.urljoin(url) if isinstance(url, str) else url
                for url in img_df["src"]
            ]
        img_df = img_df.apply(lambda col: col.fillna("").str.cat(sep="@@")).to_frame().T
        img_df = img_df[img_df.columns.intersection(_IMG_ATTRS)]
        img_df = img_df.add_prefix("img_")
        d = img_df.to_dict("records")[0]
        return d
    return {}


def get_max_cmd_len():
    system = platform.system()
    cmd_dict = {"Windows": 7000, "Linux": 100000, "Darwin": 100000}
    if system in cmd_dict:
        return cmd_dict[system]
    return 6000


MAX_CMD_LENGTH = get_max_cmd_len()

formatter.SCRAPEDMSG = "Scraped from %(src)s"
formatter.DROPPEDMSG = "Dropped: %(exception)s"
formatter.DOWNLOADERRORMSG_LONG = "Error downloading %(request)s"


class MyLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [
                subdoc for x in self.restrict_xpaths for subdoc in response.xpath(x)
            ]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return all_links


le = MyLinkExtractor(unique=False)
le_nav = MyLinkExtractor(unique=False, restrict_xpaths="//nav")
le_header = MyLinkExtractor(unique=False, restrict_xpaths="//header")
le_footer = MyLinkExtractor(unique=False, restrict_xpaths="//footer")

crawl_headers = {
    "url",
    "title",
    "meta_desc",
    "viewport",
    "charset",
    "alt_href",
    "alt_hreflang",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "canonical",
    "body_text",
    "size",
    "download_timeout",
    "download_slot",
    "download_latency",
    "redirect_times",
    "redirect_ttl",
    "redirect_urls",
    "redirect_reasons",
    "depth",
    "status",
    "links_url",
    "links_text",
    "links_nofollow",
    "img_src",
    "img_alt",
    "ip_address",
    "crawl_time",
    "blocked_by_robotstxt",
    "jsonld_errors",
    "request_headers_accept",
    "request_headers_accept-language",
    "request_headers_user-agent",
    "request_headers_accept-encoding",
    "request_headers_cookie",
}


def _split_long_urllist(url_list, max_len=MAX_CMD_LENGTH):
    """Split url_list if their total length is greater than MAX_CMD_LENGTH."""
    split_list = [[]]

    for u in url_list:
        temp_len = sum(len(temp_u) for temp_u in split_list[-1])
        if (temp_len < max_len) and (temp_len + len(u) < max_len):
            split_list[-1].append(u)
        else:
            split_list.append([u])
    return split_list


def _numbered_duplicates(items):
    """Append a number to all duplicated items starting at 1.

    ['og:site', 'og:image', 'og:image', 'og:type', 'og:image']
    becomes:
    ['og:site', 'og:image_1', 'og:image_2', 'og:type', 'og:image_3']
    """
    item_count = dict.fromkeys(items, 0)
    numbered_items = []
    for item in items:
        numbered_items.append(item + "_" + str(item_count[item]))
        item_count[item] += 1
    for i, num_item in enumerate(numbered_items):
        split_number = num_item.rsplit("_", maxsplit=1)
        if split_number[1] == "0":
            numbered_items[i] = split_number[0]
    return numbered_items


def _json_to_dict(jsonobj, i=None):
    try:
        df = json_normalize(jsonobj)
        if i:
            df = df.add_prefix("jsonld_{}_".format(i))
        else:
            df = df.add_prefix("jsonld_")
        return dict(zip(df.columns, df.values[0]))
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(msg=str(e))
        return {}


tags_xpaths = {
    "title": "//title/text()",
    "meta_desc": '//meta[@name="description"]/@content',
    "viewport": '//meta[@name="viewport"]/@content',
    "charset": "//meta[@charset]/@charset",
    "h1": "//h1",
    "h2": "//h2",
    "h3": "//h3",
    "h4": "//h4",
    "h5": "//h5",
    "h6": "//h6",
    "canonical": '//link[@rel="canonical"]/@href',
    "alt_href": '//link[@rel="alternate"]/@href',
    "alt_hreflang": '//link[@rel="alternate"]/@hreflang',
}


def _extract_content(resp, **tags_xpaths):
    d = {}
    for tag, xpath in tags_xpaths.items():
        if not tag.startswith("h"):
            value = "@@".join(resp.xpath(xpath).getall())
            if value:
                d.update({tag: value})
        else:
            value = "@@".join([h.root.text_content() for h in resp.xpath(xpath)])
            if value:
                d.update({tag: value})
    return d


class SEOSitemapSpider(Spider):
    name = "seo_spider"
    follow_links = False
    skip_url_params = False
    css_selectors = {}
    xpath_selectors = {}
    custom_headers = {}
    custom_settings = {
        "USER_AGENT": user_agent,
        "ROBOTSTXT_OBEY": True,
        "HTTPERROR_ALLOW_ALL": True,
    }

    def __init__(
        self,
        url_list,
        follow_links=False,
        allowed_domains=None,
        exclude_url_params=None,
        include_url_params=None,
        exclude_url_regex=None,
        include_url_regex=None,
        css_selectors=None,
        xpath_selectors=None,
        meta=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(url_list.split(",")))
        self.allowed_domains = json.loads(json.dumps(allowed_domains.split(",")))
        self.follow_links = eval(json.loads(json.dumps(follow_links)))
        self.exclude_url_params = eval(json.loads(json.dumps(exclude_url_params)))
        self.include_url_params = eval(json.loads(json.dumps(include_url_params)))
        self.exclude_url_regex = str(json.loads(json.dumps(exclude_url_regex)))
        if self.exclude_url_regex == "None":
            self.exclude_url_regex = None
        self.include_url_regex = str(json.loads(json.dumps(include_url_regex)))
        if self.include_url_regex == "None":
            self.include_url_regex = None
        self.css_selectors = eval(json.loads(json.dumps(css_selectors)))
        self.xpath_selectors = eval(json.loads(json.dumps(xpath_selectors)))
        self.meta = eval(json.loads(json.dumps(meta)))

    def get_custom_headers(self):
        if self.meta:
            custom_headers = self.meta.get("custom_headers") or {}
            if isinstance(custom_headers, str):
                module = runpy.run_path(custom_headers)
                custom_headers = module["custom_headers"]
        else:
            custom_headers = {}
        self.custom_headers = custom_headers

    def start_requests(self):
        self.get_custom_headers()
        for url in self.start_urls:
            try:
                yield Request(
                    url,
                    callback=self.parse,
                    errback=self.errback,
                    meta=self.meta,
                    headers=self.custom_headers.get(url),
                )
            except Exception as e:
                self.logger.error(repr(e))

    def errback(self, failure):
        if not failure.check(scrapy.exceptions.IgnoreRequest):
            self.logger.error(repr(failure))
            yield {
                "url": failure.request.url,
                "crawl_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "errors": repr(failure),
            }

    def parse(self, response):
        links = le.extract_links(response)
        nav_links = le_nav.extract_links(response)
        header_links = le_header.extract_links(response)
        footer_links = le_footer.extract_links(response)
        images = _extract_images(response)

        if links:
            parsed_links = dict(
                links_url="@@".join(link.url for link in links),
                links_text="@@".join(link.text for link in links),
                links_nofollow="@@".join(str(link.nofollow) for link in links),
            )
        else:
            parsed_links = {}
        if nav_links:
            parsed_nav_links = dict(
                nav_links_url="@@".join(link.url for link in nav_links),
                nav_links_text="@@".join(link.text for link in nav_links),
                nav_links_nofollow="@@".join(str(link.nofollow) for link in nav_links),
            )
        else:
            parsed_nav_links = {}
        if header_links:
            parsed_header_links = dict(
                header_links_url="@@".join(link.url for link in header_links),
                header_links_text="@@".join(link.text for link in header_links),
                header_links_nofollow="@@".join(
                    str(link.nofollow) for link in header_links
                ),
            )
        else:
            parsed_header_links = {}
        if footer_links:
            parsed_footer_links = dict(
                footer_links_url="@@".join(link.url for link in footer_links),
                footer_links_text="@@".join(link.text for link in footer_links),
                footer_links_nofollow="@@".join(
                    str(link.nofollow) for link in footer_links
                ),
            )
        else:
            parsed_footer_links = {}
        if self.css_selectors:
            css_selectors = {
                key: "@@".join(response.css("{}".format(val)).getall())
                for key, val in self.css_selectors.items()
            }
            css_selectors = {k: v for k, v in css_selectors.items() if v}
        else:
            css_selectors = {}

        if self.xpath_selectors:
            xpath_selectors = {
                key: "@@".join(response.xpath("{}".format(val)).getall())
                for key, val in self.xpath_selectors.items()
            }
            xpath_selectors = {k: v for k, v in xpath_selectors.items() if v}
        else:
            xpath_selectors = {}
        canonical = {
            "canonical": "@@".join(
                response.css('link[rel="canonical"]::attr(href)').getall()
            )
        }
        canonical = canonical if canonical.get("canonical") else {}
        alt_href = {
            "alt_href": "@@".join(
                response.css("link[rel=alternate]::attr(href)").getall()
            )
        }
        alt_href = alt_href if alt_href.get("alt_href") else {}
        alt_hreflang = {
            "alt_hreflang": "@@".join(
                response.css("link[rel=alternate]::attr(hreflang)").getall()
            )
        }
        alt_hreflang = alt_hreflang if alt_hreflang.get("alt_hreflang") else {}
        og_props = response.xpath(
            '//meta[starts-with(@property, "og:")]/@property'
        ).getall()
        og_content = response.xpath(
            '//meta[starts-with(@property, "og:")]/@content'
        ).getall()
        if og_props and og_content:
            og_props = _numbered_duplicates(og_props)
            open_graph = dict(zip(og_props, og_content))
        else:
            open_graph = {}
        twtr_names = response.xpath(
            '//meta[starts-with(@name, "twitter:")]/@name'
        ).getall()
        twtr_content = response.xpath(
            '//meta[starts-with(@name, "twitter:")]/@content'
        ).getall()
        if twtr_names and twtr_content:
            twtr_card = dict(zip(twtr_names, twtr_content))
        else:
            twtr_card = {}
        try:
            ld = [
                json.loads(s.replace("\r", "").replace("\n", " "))
                for s in response.css(
                    'script[type="application/ld+json"]::text'
                ).getall()
            ]
            if not ld:
                jsonld = {}
            else:
                if len(ld) == 1:
                    if isinstance(ld, list):
                        ld = ld[0]
                    jsonld = _json_to_dict(ld)
                else:
                    ld_norm = [_json_to_dict(x, i) for i, x in enumerate(ld)]
                    jsonld = {}
                    for norm in ld_norm:
                        jsonld.update(**norm)
        except Exception as e:
            jsonld = {"jsonld_errors": str(e)}
            self.logger.exception(
                " ".join([str(e), str(response.status), response.url])
            )
        page_content = _extract_content(response, **tags_xpaths)
        yield dict(
            url=response.request.url,
            **page_content,
            **open_graph,
            **twtr_card,
            **jsonld,
            body_text=" ".join(response.xpath(BODY_TEXT_SELECTOR).extract()),
            size=len(response.body),
            **css_selectors,
            **xpath_selectors,
            **{
                k: "@@".join(str(val) for val in v) if isinstance(v, list) else v
                for k, v in response.meta.items()
                if k != "custom_headers"
            },
            status=response.status,
            **parsed_links,
            **parsed_nav_links,
            **parsed_header_links,
            **parsed_footer_links,
            **images,
            ip_address=str(response.ip_address),
            crawl_time=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            **{
                "resp_headers_" + k: v
                for k, v in response.headers.to_unicode_dict().items()
            },
            **{
                "request_headers_" + k: v
                for k, v in response.request.headers.to_unicode_dict().items()
            },
        )
        if self.follow_links:
            next_pages = [link.url for link in links]
            if next_pages:
                for page in next_pages:
                    cond = _crawl_or_not(
                        page,
                        exclude_url_params=self.exclude_url_params,
                        include_url_params=self.include_url_params,
                        exclude_url_regex=self.exclude_url_regex,
                        include_url_regex=self.include_url_regex,
                    )
                    if cond:
                        yield Request(
                            page,
                            callback=self.parse,
                            errback=self.errback,
                            meta=self.meta,
                            headers=self.custom_headers.get(page),
                        )


def crawl(
    url_list,
    output_file,
    follow_links=False,
    allowed_domains=None,
    exclude_url_params=None,
    include_url_params=None,
    exclude_url_regex=None,
    include_url_regex=None,
    css_selectors=None,
    xpath_selectors=None,
    custom_settings=None,
    meta=None,
):
    """
    Crawl a website or a list of URLs based on the supplied options.

    Parameters
    ----------
    url_list : url, list
      One or more URLs to crawl. If ``follow_links`` is True, the crawler will start
      with these URLs and follow all links on pages recursively.
    output_file : str
      The path to the output of the crawl. Jsonlines only is supported to allow for
      dynamic values. Make sure your file ends with ".jl", e.g. `output_file.jl`.
    follow_links : bool
      Defaults to False. Whether or not to follow links on crawled pages.
    allowed_domains : list
      A list of the allowed domains to crawl. This ensures that the crawler does not
      attempt to crawl the whole web. If not specified, it defaults to the domains of
      the URLs provided in ``url_list`` and all their sub-domains. You can also specify
      a list of sub-domains, if you want to only crawl those.
    exclude_url_params : list, bool
      A list of URL parameters to exclude while following links. If a link contains any
      of those parameters, don't follow it. Setting it to ``True`` will exclude links
      containing any parameter.
    include_url_params : list
      A list of URL parameters to include while following links. If a link contains any
      of those parameters, follow it. Having the same parmeters to include and exclude
      raises an error.
    exclude_url_regex : str
      A regular expression of a URL pattern to exclude while following links. If a link
      matches the regex don't follow it.
    include_url_regex : str
      A regular expression of a URL pattern to include while following links. If a link
      matches the regex follow it.
    css_selectors : dict
      A dictionary mapping names to CSS selectors. The names will become column headers,
      and the selectors will be used to extract the required data/content.
    xpath_selectors : dict
      A dictionary mapping names to XPath selectors. The names will become column
      headers, and the selectors will be used to extract the required data/content.
    custom_settings : dict
      A dictionary of optional custom settings that you might want to add to the
      spider's functionality. There are over 170 settings for all kinds of options. For
      details please refer to the `spider settings <https://docs.scrapy.org/en/latest/topics/settings.html>`_
      documentation.
    meta : dict
      Additional data to pass to the crawler; add arbitrary metadata, set custom request
      headers per URL, and/or enable some third party plugins.
    Examples
    --------
    Crawl a website and let the crawler discover as many pages as available

    >>> import advertools as adv
    >>> adv.crawl("http://example.com", "output_file.jl", follow_links=True)
    >>> import pandas as pd
    >>> crawl_df = pd.read_json("output_file.jl", lines=True)

    Crawl a known set of pages (on a single or multiple sites) without
    following links (just crawl the specified pages) or "list mode":

    >>> adv.crawl(
    ...     [
    ...         "http://exmaple.com/product",
    ...         "http://exmaple.com/product2",
    ...         "https://anotherexample.com",
    ...         "https://anotherexmaple.com/hello",
    ...     ],
    ...     "output_file.jl",
    ...     follow_links=False,
    ... )

    Crawl a website, and in addition to standard SEO elements, also get the
    required CSS selectors.
    Here we will get three additional columns `price`, `author`, and
    `author_url`. Note that you need to specify if you want the text attribute
    or the `href` attribute if you are working with links (and all other
    selectors).

    >>> adv.crawl(
    ...     "http://example.com",
    ...     "output_file.jl",
    ...     css_selectors={
    ...         "price": ".a-color-price::text",
    ...         "author": ".contributorNameID::text",
    ...         "author_url": ".contributorNameID::attr(href)",
    ...     },
    ... )

    Using the ``meta`` parameter:

    **Adding custom meta data** for the crawler using the `meta` parameter for
    tracking/context purposes. If you supply {"purpose": "pre-launch test"}, then you
    will get a column called "purpose", and all its values will be "pre-launch test" in
    the crawl DataFrame.

    >>> adv.crawl(
    ...     "https://example.com",
    ...     "output_file.jl",
    ...     meta={"purpose": "pre-launch test"},
    ... )

    Or maybe mention which device(s) you crawled with, which is much easier than reading
    the user-agent string:

    >>> adv.crawl(
    ...     "https://example.com",
    ...     "output.jsonl",
    ...     custom_settings={
    ...         "USER_AGENT": "Mozilla/5.0 (iPhone; CPUiPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    ...     },
    ...     meta={"device": "Apple iPhone 12 Pro (Safari)"},
    ... )

    Of course you can combine any such meta data however way you want:

    >>> {"device": "iphone", "purpose": "initial audit", "crawl_country": "us", ...}

    **Custom request headers**: Supply custom request headers per URL with the special
    key ``custom_headers``. It's value is a dictionary where its keys are URLs, and
    every URL's values is a dictionary, each with its own custom request headers.

    >>> adv.crawl(
    ...     URL_LIST,
    ...     OUTPUT_FILE,
    ...     meta={
    ...         "custom_headers": {
    ...             "URL_A": {"HEADER_1": "VALUE_1", "HEADER_2": "VALUE_1"},
    ...             "URL_B": {"HEADER_1": "VALUE_2", "HEADER_2": "VALUE_2"},
    ...             "URL_C": {"HEADER_1": "VALUE_3"},
    ...         }
    ...     },
    ... )

    OR:

    >>> meta = {
    ...     "custom_headers": {
    ...         "https://example.com/A": {"If-None-Match": "Etag A"},
    ...         "https://example.com/B": {
    ...             "If-None-Match": "Etag B",
    ...             "User-Agent": "custom UA",
    ...         },
    ...         "https://example.com/C": {
    ...             "If-None-Match": "Etag C",
    ...             "If-Modified-Since": "Sat, 17 Oct 2024 16:24:00 GMT",
    ...         },
    ...     }
    ... }

    **Long lists of requests headers:** In some cases you might have a very long list
    and that might raise an `Argument list too long` error. In this case you can provide
    the path of a Python script that contains a dictionary for the headers. Keep in
    mind:

    - The dictionary has to be named ``custom_headers`` with the same structure mentioned above
    - The file has to be a Python script, having the extension ".py"
    - The script can generate the dictionary programmatically to make it easier to
      incorporate in various workflows
    - The path to the file can be absolute or relative to where the command is
      run from.

      >>> meta = {"custom_headers": "my_custom_headers.py"}

      OR

      >>> meta = {"custom_headers": "/full/path/to/my_custom_headers.py"}

    **Use with third party plugins** like scrapy playwright. To enable it, set
    ``{"playwright": True}`` together with other settings.
    """
    if isinstance(url_list, str):
        url_list = [url_list]
    if isinstance(allowed_domains, str):
        allowed_domains = [allowed_domains]
    if output_file.rsplit(".")[-1] not in ["jl", "jsonl"]:
        raise ValueError(
            "Please make sure your output_file ends with '.jl' or '.jsonl'.\n"
            "For example:\n"
            "{}.jl".format(output_file.rsplit(".", maxsplit=1)[0])
        )
    if (xpath_selectors is not None) and (css_selectors is not None):
        css_xpath = set(xpath_selectors).intersection(css_selectors)
        if css_xpath:
            raise ValueError(
                "Please make sure you don't set common keys for"
                "`css_selectors` and `xpath_selectors`.\n"
                "Duplicated keys: {}".format(css_xpath)
            )
    for selector in [xpath_selectors, css_selectors]:
        if selector is not None and set(selector).intersection(crawl_headers):
            raise ValueError(
                "Please make sure you don't use names of default "
                "headers. Avoid using any of these as keys: \n"
                "{}".format(sorted(crawl_headers))
            )
    if allowed_domains is None:
        allowed_domains = {urlparse(url).netloc for url in url_list}
    if exclude_url_params is not None and include_url_params is not None:
        if exclude_url_params is True:
            raise ValueError(
                "Please make sure you don't exclude and include "
                "parameters at the same time."
            )
        common_params = set(exclude_url_params).intersection(include_url_params)
        if common_params:
            raise ValueError(
                f"Please make sure you don't include and exclude "
                f"the same parameters.\n"
                f"Common parameters entered: "
                f"{', '.join(common_params)}"
            )
    if include_url_regex is not None and exclude_url_regex is not None:
        if include_url_regex == exclude_url_regex:
            raise ValueError(
                f"Please make sure you don't include and exclude "
                f"the same regex pattern.\n"
                f"You entered '{include_url_regex}'."
            )

    settings_list = []
    if custom_settings is not None:
        for key, val in custom_settings.items():
            if isinstance(val, (dict, list, set, tuple)):
                setting = "=".join([key, json.dumps(val)])
            else:
                setting = "=".join([key, str(val)])
            settings_list.extend(["-s", setting])

    command = [
        "scrapy",
        "runspider",
        spider_path,
        "-a",
        "url_list=" + ",".join(url_list),
        "-a",
        "allowed_domains=" + ",".join(allowed_domains),
        "-a",
        "follow_links=" + str(follow_links),
        "-a",
        "exclude_url_params=" + str(exclude_url_params),
        "-a",
        "include_url_params=" + str(include_url_params),
        "-a",
        "exclude_url_regex=" + str(exclude_url_regex),
        "-a",
        "include_url_regex=" + str(include_url_regex),
        "-a",
        "css_selectors=" + str(css_selectors),
        "-a",
        "xpath_selectors=" + str(xpath_selectors),
        "-a",
        "meta=" + str(meta),
        "-o",
        output_file,
    ] + settings_list
    if len(",".join(url_list)) > MAX_CMD_LENGTH:
        split_urls = _split_long_urllist(url_list)

        for u_list in split_urls:
            command[4] = "url_list=" + ",".join(u_list)
            subprocess.run(command)
    else:
        subprocess.run(command)
