"""
After crawling a website, or a bunch of URLs, you mostly likely want to analyze the data
and gain a better undersanding of the website's structure, strategy, and content. You
probably also want to check for technical issues that the site might have.

This module provides a few ready-made functions to help in anayzing crawl data.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/rt0LhxNW8GM?si=Pm5v7JKUK5CiS-Lo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

|
There are certain columns in the crawl DataFrame that can be analyzed separately and
independently, like page size and status codes. They can of course be analyzed together
with other columns like URL and title to put these columns and their data in context.

There are also groups of columns the can be thought of as describing one full aspect of
a website, yet spread across a few columns. For exmaple:

Analyzing crawled images
------------------------

Every crawled URL typically contains multiple images. Every image in turn has multiple
attributes (src, alt, width, etc.)
The number of images per URL is not the same, and not all images have the same
attributes. So we need a way to unpack all these data points in a tidy (long form)
DataFrame to get an idea of how images (and their attributes) are used and distributed
across the crawled website (URLs).

Once you have read a crawl output file into a DataFrame, you can summarize the images
in this DataFrame as follows:

>>> import advertools as adv
>>> import pandas as pd
>>> crawldf = pd.read_json('path/to/output_file.jl', lines=True)
>>> img_df = adv.crawlytics.images(crawldf)
>>> img_df

====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============
  ..  url                                                          img_src                                                                                                                                                                             img_alt           img_loading    img_sizes                         img_decoding      img_width    img_height    img_border
====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============
   0  https://www.nytimes.com/                                     /vi-assets/static-assets/icon-the-morning_144x144-b12a6923b6ad9102b766352261b1a847.webp                                                                                             The Morning Logo                 nan                               nan                     nan           nan           nan
   0  https://www.nytimes.com/                                     /vi-assets/static-assets/icon-the-upshot_144x144-0b1553ff703bbd07ac8fe73e6d215888.webp                                                                                              The Upshot Logo                  nan                               nan                     nan           nan           nan
   0  https://www.nytimes.com/                                     https://static01.nyt.com/images/2017/01/29/podcasts/the-daily-album-art/the-daily-album-art-square320-v5.jpg?quality=75&auto=webp&disable=upscale                                   The Daily Logo                   nan                               nan                     nan           nan           nan
   1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://static.nytimes.com/email-images/NYT-Newsletters-Europe-Icon-500px.jpg                                                                                                       morning briefing  nan            nan                               nan                     nan           nan           nan
   2  https://www.nytimes.com/newsletters/australia-letter         https://static.nytimes.com/email-images/NYT-Newsletters-AustraliaLetter-Icon-500px.jpg                                                                                              australia-letter  nan            nan                               nan                     nan           nan           nan
   3  https://www.nytimes.com/newsletters/the-interpreter          https://static.nytimes.com/email-images/NYT-Newsletters-SONL-TheInterpreter-Icon-500px.jpg                                                                                          the interpreter   nan            nan                               nan                     nan           nan           nan
   4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-thumbWide.jpg?quality=75&auto=webp&disable=upscale                                                              nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
   4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-hamas-icj-case-explain-wjth/25israel-hamas-icj-case-explain-wjth-thumbWide.jpg?quality=75&auto=webp&disable=upscale                    nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
   4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-hamas-qatar-israel-ctbv/25israel-hamas-qatar-israel-ctbv-thumbWide.jpg?quality=75&auto=webp&disable=upscale                            nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============

As you can see, for every URL we have all available image attributes listed, and in many
cases with those attributes empty, because they were not used for that particular image.
Also note that each image is represented independently on its own row, and mapped to the
URL on which it was found, which can be seen in the first column.
This is why we have the same URL repeated, to represent data for each image. You can
use those URLs to get more data about the URL of interest from the crawl DataFrame.

Let's get a quick overview of the usage of the various image attributes in this
DataFrame. We do this by checking whether a tag is `notna` and get the averages.

>>> img_df.notna().mean().sort_values(ascending=False).to_frame().round(2)

============  ====
url           1
img_src       0.99
img_alt       0.99
img_width     0.86
img_height    0.86
img_srcset    0.25
img_sizes     0.25
img_decoding  0.25
img_loading   0.01
img_border    0
============  ====

We can now see that almost all (99%) of our images have `src` and `alt` attributes.
About 86% have `width` and `height`, and so on. This immediately gives us an overview of
how our images are managed on the site. We can easily estimate the size of the issues if
any, and plan our work accordingly.

Analyzing links in a crawled website
------------------------------------

Another important aspect of any webpage/website is understanding how its pages are
linked, internally and externally.

The ``crawlytics.links`` function gives you a summary of the links, that is similar to
the format of the ``crawlytics.images`` DataFrame.

>>> link_df = adv.crawlytics.links(crawldf, internal_url_regex='nytimes.com')
>>> link_df

====  ===========================================================  ========================================================================  ==================  ==========  ==========
  ..  url                                                          link                                                                      text                nofollow    internal
====  ===========================================================  ========================================================================  ==================  ==========  ==========
   0  https://www.nytimes.com/                                     https://www.nytimes.com/#site-content                                     Skip to content     False       True
   0  https://www.nytimes.com/                                     https://www.nytimes.com/#site-index                                       Skip to site index  False       True
   0  https://www.nytimes.com/                                     https://www.nytimes.com/#after-dfp-ad-top                                 SKIP ADVERTISEMENT  False       True
   1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/newsletters/morning-briefing-europe#site-content  Skip to content     False       True
   1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/newsletters/morning-briefing-europe#site-index    Skip to site index  False       True
   1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/                                                                      False       True
   2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/newsletters/australia-letter#site-content         Skip to content     False       True
   2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/newsletters/australia-letter#site-index           Skip to site index  False       True
   2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/                                                                      False       True
   3  https://www.nytimes.com/newsletters/the-interpreter          https://www.nytimes.com/newsletters/the-interpreter#site-content          Skip to content     False       True
   3  https://www.nytimes.com/newsletters/the-interpreter          https://www.nytimes.com/newsletters/the-interpreter#site-index            Skip to site index  False       True
   3  https://www.nytimes.com/newsletters/the-interpreter          https://www.nytimes.com/                                                                      False       True
   4  https://www.nytimes.com/section/world/middleeast             https://www.nytimes.com/section/world/middleeast#site-content             Skip to content     False       True
   4  https://www.nytimes.com/section/world/middleeast             https://www.nytimes.com/section/world/middleeast#site-index               Skip to site index  False       True
   4  https://www.nytimes.com/section/world/middleeast             https://www.nytimes.com/section/world/middleeast                          Middle East         False       True
====  ===========================================================  ========================================================================  ==================  ==========  ==========

Every link is represented on a separate row, and we have a few attributes for each link,
it's text, whether or not it has a nofollow rel attribute, and optionally whether or not
it is internal. For the optional `internal` parameter you will have to supply a regex to
define what internal really means. You could include certain sub-domains, or even
consider other domains as part of your same property, and thus they would be considered
"internal".

We can now easily count how many links we have per URL, the most frequently used link
text, and so on.

We now take a look at redirects.

Analyzing the redirects of a crawled website
--------------------------------------------

Like images and links, the information about redirects is presented using a group of
columns:

>>> redirect_df = adv.crawlytics.redirects(crawldf)
>>> redirect_df

====  ==================================================================  ========  =======  ============  ==================  ================
  ..  url                                                                   status    order  type            download_latency    redirect_times
====  ==================================================================  ========  =======  ============  ==================  ================
   0  https://nytimes.com                                                      301        1  requested              0.220263                  1
   0  https://www.nytimes.com/                                                 200        2  crawled                0.220263                  1
  26  https://www.nytimes.com/privacy/privacy-policy                           301        1  requested              0.079844                  1
  26  https://help.nytimes.com/hc/en-us/articles/10940941449492                403        2  crawled                0.079844                  1
 105  https://www.nytimes.com/es/privacy/privacy-policy                        301        1  requested              0.0630789                 1
 105  https://help.nytimes.com/hc/en-us/articles/13537530305428                403        2  crawled                0.0630789                 1
 218  https://nytimes.com/spotlight/privacy-project-data-protection            301        1  requested              0.852014                  1
 218  https://www.nytimes.com/spotlight/privacy-project-data-protection        200        2  crawled                0.852014                  1
 225  https://nytimes.com/spotlight/privacy-project-regulation-solutions       301        1  requested              0.732559                  1
 310  http://nytimes.com/by/sahil-chinoy                                       301        1  requested              0.435062                  2
 310  https://nytimes.com/by/sahil-chinoy                                      301        2  intermediate           0.435062                  2
 310  https://www.nytimes.com/by/sahil-chinoy                                  200        3  crawled                0.435062                  2
====  ==================================================================  ========  =======  ============  ==================  ================

Here each redirect is represented using a group of columns, as well as
a group of rows. Columns show attributes of a redirect (status code, the order of the 
URL in the redirect, the type of the URL in the redirect context, download latency in
seconds, and the number of redirects in this specific process).
Since a redirect contains multiple URLs, each one of those URLs is represented on its
own row. You can use the index of this DataFrame to connect a redirect back to the crawl
DataFrame in case you want more context about it.

Let's now see what can be done with large crawl files.

Handling very large crawl files
-------------------------------

Many times you might end up crawling a large website, and the crawl file file might be
as large as your memory (or even more), making it impossible to analyze.

We have several options availablel to us:

  1. Read a subset of columns
  2. Convert the jsonlines file to parquet
  3. Explore the available column names and their respective data types of a parquet
     file

The ``jl_subset`` function only reads the column subset that you want, massively
reducing the memory consumption of our file.
In some cases you only want a small set of columns, you can read the DataFrame with the
columns of interest, write them to a new file, and delete the old large crawl file.

>>> crawl_subset = adv.crawlytics.jl_subset(
...    filepath='/path/to/output_file.jl',
...    columns=[col1, col2, ...],
...    regex=column_regex)

You can use the ``columns`` parameter to specify exactly which columns you want. You can
also use a regular expression to specify a set of columns. Here are some examples of
regular expressions that you might typically want to use:

* "img\_": Get all image columns, including all availabe `<img>` attributes.
* "jsonld\_": Get all JSON-LD columns.
* "resp_headers\_": Response headers.
* "request_headers\_": Request headers.
* "h\\\d": Heading columns, h1..h6.
* "redirect\_": Columns containing redirect information.
* "links\_": Columns containing link information.

An important characteristic of these groups of columns is that you most likely don't
know how many they are, and what they might include, so a regular expression can save a
lot of time.

You can use the `columns` and `regex` parameters together or either one of them on its
own depending on your needs.

Compressing large crawl files
-----------------------------

Another strategy while dealing with large jsonlines (.jl) files is to convert them to
the highly performant `.parquet` format. You simply have to provide the current path to
the .jl file, and provide a path for the desired .parquet file:

>>> adv.crawlytics.jl_to_parquet("output_file.jl", "output_file.parquet")

Now you have a much smaller file on disk, and you can use the full power of parquet to
efficiently read (and filter) columns and rows. Check the`pandas.read_parquet
<https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html>`_ documentation
for details.


Exploring the columns and data types of parquet files
-----------------------------------------------------

Another simple function gives us a DataFrame of the available columns in a parquet file.
One of the main advantags of using parquet is that you can select which columns you want
to read.

>>> adv.crawlytics.parquet_columns('output_file.parquet') # first 15 columns only

====  ==============  ======
  ..  column          type
====  ==============  ======
   0  url             string
   1  title           string
   2  meta_desc       string
   3  viewport        string
   4  charset         string
   5  h1              string
   6  h2              string
   7  h3              string
   8  canonical       string
   9  alt_href        string
  10  alt_hreflang    string
  11  og:url          string
  12  og:type         string
  13  og:title        string
  14  og:description  string
====  ==============  ======

Check how many columns we have of each type.

>>> adv.crawlytics.parquet_columns('nyt_crawl.parquet')['type'].value_counts()

====  =========================================================================================================================================================  =======
  ..  type                                                                                                                                                         count
====  =========================================================================================================================================================  =======
   0  string                                                                                                                                                         215
   1  double                                                                                                                                                          22
   2  list<element: string>                                                                                                                                            5
   3  int64                                                                                                                                                            4
   4  list<element: struct<@context: string, @type: string, position: int64, url: string>>                                                                             2
   5  list<element: struct<@context: string, @type: string, contentUrl: string, creditText: string, url: string>>                                                      2
   6  list<element: struct<@context: string, @type: string, caption: string, contentUrl: string, creditText: string, height: int64, url: string, width: int64>>        1
   7  timestamp[ns]                                                                                                                                                    1
   8  list<element: struct<@context: string, @type: string, item: string, name: string, position: int64>>                                                              1
   9  list<element: struct<@context: string, @type: string, name: string, url: string>>                                                                                1
====  =========================================================================================================================================================  =======


Module functions
----------------
"""

import re

import pandas as pd
import pyarrow.parquet as pq

__all__ = [
    "images",
    "links",
    "redirects",
    "jl_subset",
    "jl_to_parquet",
    "parquet_columns",
]


def redirects(crawldf):
    """Create a tidy DataFrame for the redirects in `crawldf` with the columns:

    - url: All the URLs in the redirect (chain).
    - status: The status code of each URL.
    - type: "requested", "inermediate", or "crawled".
    - order: 1, 2, 3... up to the number of urls in the redirect chain.
    - redirect_times: The number of redirects in the chain (URLs in the chain minus one).

    Parameters
    ----------
    crawldf : pandas.DataFrame
        A DataFrame of an advertools crawl file

    Examples
    --------
    >>> import advertools as adv
    >>> import pandas as pd
    >>> crawldf = pd.read_json('output_file.jl', lines=True)
    >>> redirect_df = adv.crawlytics.redirects(crawldf)
    >>> redirect_df

    ====  =========================================================  ========  =======  =========  ==================  ================
      ..  url                                                          status    order  type         download_latency    redirect_times
    ====  =========================================================  ========  =======  =========  ==================  ================
       0  https://nytimes.com                                             301        1  requested           0.220263                  1
       0  https://www.nytimes.com/                                        200        2  crawled             0.220263                  1
      26  https://www.nytimes.com/privacy/privacy-policy                  301        1  requested           0.079844                  1
      26  https://help.nytimes.com/hc/en-us/articles/10940941449492       403        2  crawled             0.079844                  1
     105  https://www.nytimes.com/es/privacy/privacy-policy               301        1  requested           0.0630789                 1
     105  https://help.nytimes.com/hc/en-us/articles/13537530305428       403        2  crawled             0.0630789                 1
    ====  =========================================================  ========  =======  =========  ==================  ================
    """
    if "redirect_urls" not in crawldf.columns:
        return pd.DataFrame()
    if "redirect_urls" in crawldf:
        if crawldf["redirect_urls"].isna().all():
            return pd.DataFrame()
    redirect_df = crawldf[
        ["url", "status", "redirect_urls", "redirect_reasons"]
    ].dropna(subset=["redirect_urls", "redirect_reasons"])
    redirect_df["redirect_urls"] = (
        redirect_df["redirect_urls"].astype(str).str.split("@@")
    )
    redirect_df["redirect_reasons"] = (
        redirect_df["redirect_reasons"].astype(str).str.split("@@")
    )
    for url, redirect_urls in redirect_df[["url", "redirect_urls"]].values:
        redirect_urls.append(url)
    for status, redirect_reasons in redirect_df[["status", "redirect_reasons"]].values:
        redirect_reasons.append(status)
    redirect_df["order"] = [
        list(range(1, len(x) + 1)) for x in redirect_df["redirect_reasons"]
    ]
    redirect_df["type"] = [
        [
            (
                "requested"
                if o == min(order)
                else "crawled" if o == max(order) else "intermediate"
            )
            for o in order
        ]
        for order in redirect_df["order"]
    ]
    redirect_df.columns = ["NA1", "NA2", "url", "status", "order", "type"]
    exploded = redirect_df[["url", "status", "order", "type"]].apply(pd.Series.explode)
    final_df = pd.merge(
        exploded,
        crawldf[["download_latency", "redirect_times"]],
        left_index=True,
        right_index=True,
    )
    final_df["redirect_times"] = final_df["redirect_times"].astype(int)
    return final_df


def links(crawldf, internal_url_regex=None):
    """Summarize links from a crawl DataFrame.

    Parameters
    ----------
    crawldf : DataFrame
        A DataFrame of a website crawled with advertools.
    internal_url_regex : str
        A regular expression for identifying if a link is internal or not.
        For example if your website is example.com, this would be "example.com".

    Returns
    -------
    link_df : pandas.DataFrame

    Examples
    --------
    >>> import advertools as adv
    >>> import pandas as pd
    >>> crawldf = pd.read_json('output_file.jl', lines=True)
    >>> link_df = adv.crawlytics.links(crawldf)
    >>> link_df

    ====  ===========================================================  ========================================================================  ==================  ==========  ==========
      ..  url                                                          link                                                                      text                nofollow    internal
    ====  ===========================================================  ========================================================================  ==================  ==========  ==========
       0  https://www.nytimes.com/                                     https://www.nytimes.com/#site-content                                     Skip to content     False       True
       0  https://www.nytimes.com/                                     https://www.nytimes.com/#site-index                                       Skip to site index  False       True
       0  https://www.nytimes.com/                                     https://www.nytimes.com/#after-dfp-ad-top                                 SKIP ADVERTISEMENT  False       True
       1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/newsletters/morning-briefing-europe#site-content  Skip to content     False       True
       1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/newsletters/morning-briefing-europe#site-index    Skip to site index  False       True
       1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://www.nytimes.com/                                                                      False       True
       2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/newsletters/australia-letter#site-content         Skip to content     False       True
       2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/newsletters/australia-letter#site-index           Skip to site index  False       True
       2  https://www.nytimes.com/newsletters/australia-letter         https://www.nytimes.com/                                                                      False       True
    ====  ===========================================================  ========================================================================  ==================  ==========  ==========
    """
    if "links_url" not in crawldf:
        return pd.DataFrame()
    link_df = pd.merge(
        crawldf[["url"]],
        crawldf.filter(regex="^links_").apply(lambda s: s.str.split("@@").explode()),
        left_index=True,
        right_index=True,
    )
    link_df["links_nofollow"] = link_df["links_nofollow"].replace(
        {"True": True, "False": False}
    )
    if internal_url_regex is not None:
        link_df["internal"] = (
            link_df["links_url"].fillna("").str.contains(internal_url_regex, regex=True)
        )
    link_df = link_df.rename(
        columns={
            "links_url": "link",
            "links_text": "text",
            "links_nofollow": "nofollow",
        }
    )
    return link_df


def images(crawldf):
    """Summarize crawled images from a crawl DataFrame.

    Parameters
    ----------
    crawldf : pandas.DataFrame
        A crawl DataFrame as a result of the advertools.crawl function.

    Returns
    -------
    img_summary : pandas.DataFrame
        A DataFrame containing all available img tags and their attributes mapped to
        their respective URLs where each image data is represented with a separate row.


    Examples
    --------
    >>> import advertools as adv
    >>> import pandas as pd
    >>> crawldf = pd.read_json('output_file.jl', lines=True)
    >>> image_df = adv.crawlytics.images(crawldf)
    >>> image_df

    ====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============
      ..  url                                                          img_src                                                                                                                                                                             img_alt           img_loading    img_sizes                         img_decoding      img_width    img_height    img_border
    ====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============
       0  https://www.nytimes.com/                                     /vi-assets/static-assets/icon-the-morning_144x144-b12a6923b6ad9102b766352261b1a847.webp                                                                                             The Morning Logo                 nan                               nan                     nan           nan           nan
       0  https://www.nytimes.com/                                     /vi-assets/static-assets/icon-the-upshot_144x144-0b1553ff703bbd07ac8fe73e6d215888.webp                                                                                              The Upshot Logo                  nan                               nan                     nan           nan           nan
       0  https://www.nytimes.com/                                     https://static01.nyt.com/images/2017/01/29/podcasts/the-daily-album-art/the-daily-album-art-square320-v5.jpg?quality=75&auto=webp&disable=upscale                                   The Daily Logo                   nan                               nan                     nan           nan           nan
       1  https://www.nytimes.com/newsletters/morning-briefing-europe  https://static.nytimes.com/email-images/NYT-Newsletters-Europe-Icon-500px.jpg                                                                                                       morning briefing  nan            nan                               nan                     nan           nan           nan
       2  https://www.nytimes.com/newsletters/australia-letter         https://static.nytimes.com/email-images/NYT-Newsletters-AustraliaLetter-Icon-500px.jpg                                                                                              australia-letter  nan            nan                               nan                     nan           nan           nan
       3  https://www.nytimes.com/newsletters/the-interpreter          https://static.nytimes.com/email-images/NYT-Newsletters-SONL-TheInterpreter-Icon-500px.jpg                                                                                          the interpreter   nan            nan                               nan                     nan           nan           nan
       4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-thumbWide.jpg?quality=75&auto=webp&disable=upscale                                                              nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
       4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-hamas-icj-case-explain-wjth/25israel-hamas-icj-case-explain-wjth-thumbWide.jpg?quality=75&auto=webp&disable=upscale                    nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
       4  https://www.nytimes.com/section/world/middleeast             https://static01.nyt.com/images/2024/01/25/multimedia/25israel-hamas-qatar-israel-ctbv/25israel-hamas-qatar-israel-ctbv-thumbWide.jpg?quality=75&auto=webp&disable=upscale                            nan            (min-width: 1024px) 205px, 150px  async                   150           100           nan
    ====  ===========================================================  ==================================================================================================================================================================================  ================  =============  ================================  ==============  ===========  ============  ============
    """
    dfs = []
    img_df = crawldf.filter(regex="^url$|img_")
    for index, row in img_df.iterrows():
        notna = row.dropna().index
        if len(notna) == 1:
            temp = pd.DataFrame({"url": row["url"]}, index=[index])
        else:
            temp = (
                row.to_frame()
                .T.set_index("url")
                .apply(lambda s: s.str.split("@@"))
                .explode(notna.tolist()[1:])
            )
            temp = temp.reset_index()
            temp.index = [index for i in range(len(temp))]
        dfs.append(temp)
    final_df = pd.concat(dfs)
    return final_df


def jl_subset(filepath, columns=None, regex=None, chunksize=500):
    """Read a jl file extracting selected `columns` and/or columns matching `regex`.

    Parameters
    ----------
    filepath : str
      The path of the .jl (jsonlines) file to read.
    columns : list
      An optional list of column names that you want to read.
    regex : str
      An optional regular expression of the pattern of columns to read.
    chunksize : int
      How many rows to read per chunk.

    Examples
    --------

    >>> import advertools as adv

    Read only the columns "url" and "meta_desc":

    >>> adv.crawlytics.jl_subset('output_file.jl', columns=['url', 'meta_desc'])

    Read columns matching the regex "jsonld":

    >>> adv.crawlytics.jl_subset('output_file.jl', regex='jsonld')

    Read the columns "url" and "meta_desc" as well as columns matching "jsonld":

    >>> adv.crawlytics.jl_subset('output_file.jl', columns=['url', 'meta_desc'], regex='jsonld')

    Returns
    -------
    df_subset : pandas.DataFrame
      A DataFrame containing the list of `columns` and/or columns matching `regex`.
    """
    if columns is None and regex is None:
        raise ValueError("Please supply either a list of columns or a regex.")
    if columns is not None:
        col_regex = "^" + "$|^".join(columns) + "$"
    else:
        col_regex = None
    if (columns is not None) and (regex is not None):
        full_regex = "|".join([col_regex, regex])
    else:
        full_regex = col_regex or regex
    dfs = []
    for chunk in pd.read_json(filepath, lines=True, chunksize=chunksize):
        chunk_subset = chunk.filter(regex=full_regex)
        dfs.append(chunk_subset)
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df


def jl_to_parquet(jl_filepath, parquet_filepath):
    """Convert a jsonlines crawl file to the parquet format.

    Parameters
    ----------
    jl_filepath : str
      The path of an existing .jl file.
    parquet_fileapth : str
      The pather where you want the new file to be saved.

    Examples
    --------
    >>> import advertools as adv
    >>> adv.crawlytics.jl_to_parquet("output_file.jl", "output_file.parquet")
    """
    status = "not done"
    crawldf = pd.read_json(jl_filepath, lines=True)
    while status == "not done":
        try:
            crawldf.to_parquet(parquet_filepath, index=False, version="2.6")
            status = "done"
        except Exception as e:
            error = e.args[-1]
            column = re.findall(r"column (\S+)", error)
            print(f"converting to string: {column[0]}")
            crawldf[column[0]] = crawldf[column[0]].astype(str).replace("nan", pd.NA)


def parquet_columns(filepath):
    """Get column names and datatypes of a parquet file.

    Parameters
    ----------
    filepath : str
      The path of the file that you want to get columns names and types.

    Returns
    -------
    columns_types : pandas.DataFrame
      A DataFrame with two columns "column" and "type".
    """
    pqdataset = pq.ParquetDataset(filepath)
    columns_df = pd.DataFrame(
        zip(pqdataset.schema.names, pqdataset.schema.types), columns=["column", "type"]
    )
    return columns_df
