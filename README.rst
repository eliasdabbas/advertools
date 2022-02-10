.. image:: https://img.shields.io/pypi/v/advertools.svg
        :target: https://pypi.python.org/pypi/advertools

.. image:: https://readthedocs.org/projects/advertools/badge/?version=latest
        :target: https://advertools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: http://pepy.tech/badge/advertools
        :target: http://pepy.tech/project/advertools 

.. image:: https://img.shields.io/lgtm/grade/python/g/eliasdabbas/advertools.svg
        :target: https://lgtm.com/projects/g/eliasdabbas/advertools/context:python

.. image:: https://badges.gitter.im/advertools/community.svg
        :target: https://bit.ly/3hEWZCe

| 🎉 **New:** ``crawl_headers`` Function for `crawling a known list of URLs with the HEAD method only <https://advertools.readthedocs.io/en/master/advertools.header_spider.html>`_
| 🎊 **New:** `SEO crawler <https://advertools.readthedocs.io/en/master/advertools.spider.html>`_
  has new options for following links, include/exclude URL params and/or URL regex.
| 🎉 **New:** ``reverse_dns_lookup`` Function for `getting host information on a list of IP addresses <https://advertools.readthedocs.io/en/master/advertools.reverse_dns_lookup.html>`_


``advertools``: productivity & analysis tools to scale your online marketing
============================================================================

| A digital marketer is a data scientist.
| Your job is to manage, manipulate, visualize, communicate, understand,
  and make decisions based on data.

You might be doing basic stuff, like copying and pasting text on spread
sheets, you might be running large scale automated platforms with
sophisticated algorithms, or somewhere in between. In any case your job
is all about working with data.

As a data scientist you don't spend most of your time producing cool
visualizations or finding great insights. The majority of your time is spent
wrangling with URLs, figuring out how to stitch together two tables, hoping
that the dates, won't break, without you knowing, or trying to generate the
next 124,538 keywords for an upcoming campaign, by the end of the week!

``advertools`` is a Python package that can hopefully make that part of your job a little easier.

Installation
------------

.. code:: bash

   pip install advertools
   # OR:
   pip3 install advertools


SEM Campaigns
-------------
The most important thing to achieve in SEM is a proper mapping between the
three main elements of a search campaign

**Keywords** (the intention) -> **Ads** (your promise) -> **Landing Pages** (your delivery of the promise)
Once you have this done, you can focus on management and analysis. More importantly,
once you know that you can set this up in an easy way, you know you can focus
on more strategic issues. In practical terms you need two main tables to get started:

* Keywords: You can `generate keywords <https://advertools.readthedocs.io/en/master/advertools.kw_generate.html>`_ (note I didn't say research)  with the
  `kw_generate` function.

* Ads: There are two approaches that you can use:

  * Bottom-up: You can create text ads for a large number of products by simple
    replacement of product names, and providing a placeholder in case your text
    is too long. Check out the `ad_create <https://advertools.readthedocs.io/en/master/advertools.ad_create.html>`_ function for more details.
  * Top-down: Sometimes you have a long description text that you want to split
    into headlines, descriptions and whatever slots you want to split them into.
    `ad_from_string <https://advertools.readthedocs.io/en/master/advertools.ad_from_string.html>`_
    helps you accomplish that.

* Tutorials and additional resources

  * Get started with `Data Science for Digital Marketing and SEO/SEM <https://www.oncrawl.com/technical-seo/data-science-seo-digital-marketing-guide-beginners/>`_
  * `Setting a full SEM campaign <https://www.datacamp.com/community/tutorials/sem-data-science>`_ for DataCamp's website tutorial
  * Project to practice `generating SEM keywords with Python <https://www.datacamp.com/projects/400>`_ on DataCamp
  * `Setting up SEM campaigns on a large scale <https://www.semrush.com/blog/setting-up-search-engine-marketing-campaigns-on-large-scale/>`_ tutorial on SEMrush
  * Visual `tool to generate keywords <https://www.dashboardom.com/advertools>`_ online based on the `kw_generate` function


SEO
---
Probably the most comprehensive online marketing area that is both technical
(crawling, indexing, rendering, redirects, etc.) and non-technical (content
creation, link building, outreach, etc.). Here are some tools that can help
with your SEO

* `SEO crawler: <https://advertools.readthedocs.io/en/master/advertools.spider.html>`_
  A generic SEO crawler that can be customized, built with Scrapy, & with several
  features:

  * Standard SEO elements extracted by default (title, header tags, body text,
    status code, reponse and request headers, etc.)
  * CSS and XPath selectors: You probably have more specific needs in mind, so
    you can easily pass any selectors to be extracted in addition to the
    standard elements being extracted
  * Custom settings: full access to Scrapy's settings, allowing you to better
    control the crawling behavior (set custom headers, user agent, stop spider
    after x pages, seconds, megabytes, save crawl logs, run jobs at intervals
    where you can stop and resume your crawls, which is ideal for large crawls
    or for continuous monitoring, and many more options)
  * Following links: option to only crawl a set of specified pages or to follow
    and discover all pages through links

* `robots.txt downloader <https://advertools.readthedocs.io/en/master/advertools.sitemaps.html#advertools.sitemaps.robotstxt_to_df>`_
  A simple downloader of robots.txt files in a DataFrame format, so you can
  keep track of changes across crawls if any, and check the rules, sitemaps,
  etc.
* `XML Sitemaps downloader / parser <https://advertools.readthedocs.io/en/master/advertools.sitemaps.html>`_
  An essential part of any SEO analysis is to check XML sitemaps. This is a
  simple function with which you can download one or more sitemaps (by
  providing the URL for a robots.txt file, a sitemap file, or a sitemap index
* `SERP importer and parser for Google & YouTube <https://advertools.readthedocs.io/en/master/advertools.serp.html>`_
  Connect to Google's API and get the search data you want. Multiple search
  parameters supported, all in one function call, and all results returned in a
  DataFrame

* Tutorials and additional resources

  * A visual tool built with the ``serp_goog`` function to get `SERP rankings on Google <https://www.dashboardom.com/google-serp>`_
  * A tutorial on `analyzing SERPs on a large scale with Python <https://www.semrush.com/blog/analyzing-search-engine-results-pages/>`_ on SEMrush
  * `SERP datasets on Kaggle <https://www.kaggle.com/eliasdabbas/datasets?search=engine>`_ for practicing on different industries and use cases
  * `SERP notebooks on Kaggle <https://www.kaggle.com/eliasdabbas/notebooks?sortBy=voteCount&group=everyone&pageSize=20&userId=484496&tagIds=1220>`_
    some examples on how you might tackle such data
  * `Content Analysis with XML Sitemaps and Python <https://www.semrush.com/blog/content-analysis-xml-sitemaps-python/>`_
  * XML dataset examples: `news sites <https://www.kaggle.com/eliasdabbas/news-sitemaps>`_, `Turkish news sites <https://www.kaggle.com/eliasdabbas/turk-haber-sitelerinin-site-haritalari>`_,
    `Bloomberg news <https://www.kaggle.com/eliasdabbas/bloomberg-business-articles-urls>`_


Text & Content Analysis (for SEO & Social Media)
------------------------------------------------

URLs, page titles, tweets, video descriptions, comments, hashtags are some
exmaples of the types of text we deal with. ``advertools`` provides a few
options for text analysis


* `Word frequency <https://advertools.readthedocs.io/en/master/advertools.word_frequency.html>`_
  Counting words in a text list is one of the most basic and important tasks in
  text mining. What is also important is counting those words by taking in
  consideration their relative weights in the dataset. ``word_frequency`` does
  just that.
* `URL Analysis <https://advertools.readthedocs.io/en/master/advertools.urlytics.html>`_
  We all have to handle many thousands of URLs in reports, crawls, social media
  extracts, XML sitemaps and so on. ``url_to_df`` converts your URLs into
  easily readable DataFrames.

* `Emoji <https://advertools.readthedocs.io/en/master/advertools.emoji.html>`_
  Produced with one click, extremely expressive, highly diverse (3k+ emoji),
  and very popular, it's important to capture what people are trying to communicate
  with emoji. Extracting emoji, get their names, groups, and sub-groups is
  possible. The full emoji database is also available for convenience, as well
  as an ``emoji_search`` function in case you want some ideas for your next
  social media or any kind of communication
* `extract_ functions <https://advertools.readthedocs.io/en/master/advertools.extract.html>`_
  The text that we deal with contains many elements and entities that have
  their own special meaning and usage. There is a group of convenience
  functions to help in extracting and getting basic statistics about structured
  entities in text; emoji, hashtags, mentions, currency, numbers, URLs, questions
  and more. You can also provide a special regex for your own needs.
* `Stopwords <https://advertools.readthedocs.io/en/master/advertools.stopwords.html>`_
  A list of stopwords in forty different languages to help in text analysis.
* Tutorial on DataCamp for creating the ``word_frequency`` function and
  explaining the importance of the difference between `absolute and weighted word frequency <https://www.datacamp.com/community/tutorials/absolute-weighted-word-frequency>`_
* `Text Analysis for Online Marketers <https://www.semrush.com/blog/text-analysis-for-online-marketers/>`_
  An introductory article on SEMrush

Social Media
------------

In addition to the text analysis techniques provided, you can also connect to
the Twitter and YouTube data APIs. The main benefits of using ``advertools``
for this:

* Handles pagination and request limits: typically every API has a limited
  number of results that it returns. You have to handle pagination when you
  need more than the limit per request, which you typically do. This is handled
  by default
* DataFrame results: APIs send you back data in a formats that need to be
  parsed and cleaned so you can more easily start your analysis. This is also
  handled automatically
* Multiple requests: in YouTube's case you might want to request data for the
  same query across several countries, languages, channels, etc. You can
  specify them all in one request and get the product of all the requests in
  one response

* Tutorials and additional resources

* A visual tool to `check what is trending on Twitter <https://www.dashboardom.com/trending-twitter>`_ for all available locations
* A `Twitter data analysis dashboard <https://www.dashboardom.com/twitterdash>`_ with many options
* How to use the `Twitter data API with Python <https://www.kaggle.com/eliasdabbas/twitter-in-a-dataframe>`_
* `Extracting entities from social media posts <https://www.kaggle.com/eliasdabbas/extract-entities-from-social-media-posts>`_ tutorial on Kaggle
* `Analyzing 131k tweets <https://www.kaggle.com/eliasdabbas/extract-entities-from-social-media-posts>`_ by European Football clubs tutorial on Kaggle
* An overview of the `YouTube data API with Python <https://www.kaggle.com/eliasdabbas/youtube-data-api>`_


Conventions
-----------

Function names mostly start with the object you are working on, so you can use
autocomplete to discover other options:

| ``kw_``: for keywords-related functions
| ``ad_``: for ad-related functions
| ``url_``: URL tracking and generation
| ``extract_``: for extracting entities from social media posts (mentions, hashtags, emoji, etc.)
| ``emoji_``: emoji related functions and objects
| ``twitter``: a module for querying the Twitter API and getting results in a DataFrame
| ``youtube``: a module for querying the YouTube Data API and getting results in a DataFrame
| ``serp_``: get search engine results pages in a DataFrame, currently available: Google and YouTube
| ``crawl``: a function you will probably use a lot if you do SEO
| ``*_to_df``: a set of convenience functions for converting to DataFrames
  (log files, XML sitemaps, robots.txt files, and lists of URLs)
