"""
.. _urlytics:

Split, Parse, and Analyze URL Structure
=======================================

Extracting information from URLs can be a little tedious, yet very important.
Using the standard for URLs we can extract a lot of information in a fairly
structured manner.

There are many situations in which you have many URLs that you want to better
understand:

* **Analytics reports**: Whichever analytics system you use, whether Google
  Analytics, search console, or any other reporting tool that reports on URLs,
  your reports can be enhanced by splitting URLs, and in effect becoming four
  or five data points as opposed to one.
* :ref:`Crawl datasets <crawl>`: The result of any crawl you run typically
  contains the URLs, which can benefit from the same enhancement.
* :ref:`SERP datasets <serp>`: Which are basically about URLs.
* :ref:`Extracted URLs <extract>`: Extracting URLs from social media posts is
  one thing you might want to do to better understand those posts, and further
  splitting URLs can also help.
* :ref:`XML sitemaps <sitemaps>`: Right after downloading a sitemap(s)
  splitting it further can help in giving a better perspective on the dataset.

The main function here is :func:`url_to_df`, which as the name suggests,
converts URLs to DataFrames.


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv

    urls = ['https://netloc.com/path_1/path_2?price=10&color=blue#frag_1',
            'https://netloc.com/path_1/path_2?price=15&color=red#frag_2',
            'https://netloc.com/path_1/path_2/path_3?size=sm&color=blue#frag_1',
            'https://netloc.com/path_1?price=10&color=blue']
    adv.url_to_df(urls)

====  =================================================================  ========  ==========  =====================  ===================  ==========  =======  =======  =======  ==========  =============  =============  ============
  ..  url                                                                scheme    netloc      path                   query                fragment    dir_1    dir_2    dir_3    last_dir    query_color      query_price  query_size
====  =================================================================  ========  ==========  =====================  ===================  ==========  =======  =======  =======  ==========  =============  =============  ============
   0  https://netloc.com/path_1/path_2?price=10&color=blue#frag_1        https     netloc.com  /path_1/path_2         price=10&color=blue  frag_1      path_1   path_2   nan      path_2      blue                      10  nan
   1  https://netloc.com/path_1/path_2?price=15&color=red#frag_2         https     netloc.com  /path_1/path_2         price=15&color=red   frag_2      path_1   path_2   nan      path_2      red                       15  nan
   2  https://netloc.com/path_1/path_2/path_3?size=sm&color=blue#frag_1  https     netloc.com  /path_1/path_2/path_3  size=sm&color=blue   frag_1      path_1   path_2   path_3   path_3      blue                     nan  sm
   3  https://netloc.com/path_1?price=10&color=blue                      https     netloc.com  /path_1                price=10&color=blue              path_1   nan      nan      path_1      blue                      10  nan
====  =================================================================  ========  ==========  =====================  ===================  ==========  =======  =======  =======  ==========  =============  =============  ============

ِA more elaborate exmaple on :ref:`how to analyze URLs <sitemaps>` shows how you
might use this function after obtaining a set of URLs.

The resulting DataFrame contains the following columns:

* **url**: The original URLs are listed as a reference. They are decoded for
  easier reading, and you can set ``decode=False`` if you want to retain the
  original encoding.
* **scheme**: Self-explanatory. Note that you can also provide relative URLs
  `/category/sub-category?one=1&two=2` in which case the `url`, `scheme` and
  `netloc` columns would be empty. You can mix relative and absolute URLs as
  well.
* **netloc**: The network location is the sub-domain (optional) together with
  the domain and top-level domain and/or the country domain.
* **path**: The slug of the URL, excluding the query parameters and fragments
  if any. The path is also split into directories ``dir_1/dir_2/dir_3/...`` to
  make it easier to categorize and analyze the URLs.
* **last_dir**: The last directory of each of the URLs. This is usually the
  part that contains information about the page itself (blog post title,
  product name, etc.) with previous directories providing meta data (category,
  sub-category, author name, etc.). In many cases you don't have all URLs with
  the same number of directories, so they end up unaligned. This extracts all
  ``last_dir``'s in one column.
* **query**: If query parameters are available they are given in this column,
  but more importantly they are parsed and included in separate columns, where
  each parameter has its own column (with the keys being the names). As in the
  example above, the query `price=10&color=blue` becomes two columns, one for
  price and the other for color. If any other URLs in the dataset contain the
  same parameters, their values will be populated in the same column, and `NA`
  otherwise.
* **fragment**: The final part of the URL after the hash mark `#`, linking to a
  part in the page.
* **query_***: The query parameter names are prepended with `query_` to make
  it easy to filter them out, and to avoid any name collissions with other
  columns, if some URL contains a query parameter called "url" for example.
  In the unlikely event of having a repeated parameter in the same URL, then
  their values would be delimited by two "@" signs `one@@two@@three`. It's
  unusual, but it happens.
* **hostname and port**: If available a column for ports will be shown, and if
  the hostname is different from `netloc` it would also have its own column.

Query Parameters
----------------
The great thing about parameters is that the names are descriptive (mostly!)
and once given a certain column you can easily understand what data they
contain. Once this is done, you can sort the products by price, filter by
destination, get the red and blue items, and so on.

The URL Path (Directories):
---------------------------
Here things are not as straightforward, and there is no way to know what the
first or second directory is supposed to indicate. In general, I can think of
three main situations that you can encounter while analyzing directories.

* **Consistent URLs**: This is the simplest case, where all URLs follow the
  same structure. `/en/product1` clearly shows that the first directory
  indicates the language of the page. So it can also make sense to rename those
  columns once you have discovered their meaning.

* **Inconsistent URLs**: This is similar to the previous situation. All URLs
  follow the same pattern with a few exceptions. Take the following URLs for
  example:

    * /topic1/title-of-article-1
    * /es/topic1/title-of-article-2
    * /es/topic2/title-of-article-3
    * /topic2/title-of-artilce-4

  You can see that they follow the pattern `/language/topic/article-title`,
  except for English, which is not explicitly mentioned, but its articles can
  be identified by having two instead of three directories, as we have for
  "/es/". If URLs are split in this case, yout will end up with `dir_1` having
  "topic1", "es", "es", and "topic2", which distorts the data. Actually you
  want to have "en", "es", "es", "en". In such cases, after making sure you
  have the right rules and patterns, you might create special columns or
  replace/insert values to make them consistent, and get them to a state
  similar to the first example.

* **URLs of different types**: In many cases you will find that sites have
  different types of pages with completely different roles on the site.

    * /blog/post-1-title.html
    * /community/help/topic_1
    * /community/help/topic_2

  Here, once you split the directories, you will see that they don't align
  properly (because of different lengths), and they can't be compared easily. A
  good approach is to split your dataset into one for blog posts and another
  for community content for example.

The ideal case for the `path` part of the URL is to be split into directories
of equal length across the dataset, having the right data in the right columns
and `NA` otherwise. Or, splitting the dataset and analyzing separately.

Analyzing a large number of URLs
--------------------------------

Having a very long list of URLs is a thing that you might encounter with log files,
big XML sitemaps, crawling a big website, and so on.
You can still use ``url_to_df`` but you might consume a massive amount of memory, in
some cases making impossible to process the data. For these cases you can use the
``output_file`` parameter.
All you have to do is provide a path for this output file, and it has to have the
.parquet extension. This allows you to compress the data, analyze it way more
efficiently, and you can refer back to the same dataset without having to go through
the process again (it can take a few minutes with big datasets).

.. code-block:: python
   :linenos:

    import advertools as adv
    import pandas as pd

    adv.url_to_df([url_1, url_2, ...], ouput_file="output_file.parquet")
    pd.read_parquet("output_file.parquet", columns=["scheme"])
    pd.read_parquet("output_file.parquet", columns=["dir_1", "dir_2"])
    pd.read_parquet(
        "output_file.parquet",
        columns=["dir_1", "dir_2"],
        filters=[("dir_1", "in", ["news", "politics"])],
    )

"""  # noqa: E501

import os
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, unquote, urlsplit

import numpy as np
import pandas as pd


def _url_to_df(urls, decode=True):
    """Split the given URLs into their components to a DataFrame.

    Each column will have its own component, and query parameters and
    directories will also be parsed and given special columns each.

    :param url urls: A list of URLs to split into components
    :param bool decode: Whether or not to decode the given URLs
    :return DataFrame split: A DataFrame with a column for each component
    """
    if isinstance(urls, str):
        urls = [urls]
    decode = unquote if decode else lambda x: x
    split_list = []
    for url in urls:
        split = urlsplit(decode(url))
        port = split.port
        hostname = split.hostname if split.hostname != split.netloc else None
        split = split._asdict()
        if hostname:
            split["hostname"] = hostname
        if port:
            split["port"] = port
        parsed_query = parse_qs(split["query"])
        parsed_query = {
            "query_" + key: "@@".join(val) for key, val in parsed_query.items()
        }
        split.update(**parsed_query)
        dirs = split["path"].strip("/").split("/")
        if dirs[0]:
            dir_cols = {"dir_{}".format(n): d for n, d in enumerate(dirs, 1)}
            split.update(**dir_cols)
        split_list.append(split)
    df = pd.DataFrame(split_list)

    query_df = df.filter(regex="query_")
    if not query_df.empty:
        sorted_q_params = query_df.notna().mean().sort_values(ascending=False).index
        query_df = query_df[sorted_q_params]
        df = df.drop(query_df.columns, axis=1)
    dirs_df = df.filter(regex="^dir_")
    if not dirs_df.empty:
        df = df.drop(dirs_df.columns, axis=1)
        dirs_df = dirs_df.assign(last_dir=dirs_df.ffill(axis=1).iloc[:, -1:].squeeze())
    df = pd.concat([df, dirs_df, query_df], axis=1).replace("", pd.NA)
    url_list_df = pd.DataFrame({"url": [decode(url) for url in urls]})
    final_df = pd.concat([url_list_df, df], axis=1)
    return final_df


def url_to_df(urls, decode=True, output_file=None):
    """Split the given URLs into their components to a DataFrame.

    Each column will have its own component, and query parameters and
    directories will also be parsed and given special columns each.

    Parameters
    ----------
    urls : list,pandas.Series
      A list of URLs to split into components
    decode : bool, default True
      Whether or not to decode the given URLs
    output_file : str
      The path where to save the output DataFrame with a .parquet extension

    Returns
    -------
    urldf : pandas.DataFrame
      A DataFrame with a column for each URL component
    """
    if output_file is not None:
        if output_file.rsplit(".")[-1] != "parquet":
            raise ValueError("Your output_file has to have a .parquet extension.")
    step = 1000
    sublists = (urls[sub : sub + step] for sub in range(0, len(urls), step))

    with TemporaryDirectory() as tmpdir:
        for i, sublist in enumerate(sublists):
            urldf = _url_to_df(sublist, decode=decode)
            urldf.index = range(i * step, (i * step) + len(urldf))
            urldf.to_parquet(f"{tmpdir}/{i:08}.parquet", index=True, version="2.6")
        final_df_list = [
            pd.read_parquet(f"{tmpdir}/{tmpfile}") for tmpfile in os.listdir(tmpdir)
        ]
        final_df = pd.concat(final_df_list).sort_index()
    if output_file is not None:
        final_df.to_parquet(output_file, index=False, version="2.6")
    else:
        return final_df
