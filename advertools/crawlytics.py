"""
Crawling and Scraping Analysis
==============================

After crawling a website, or a bunch of URLs, you mostly likely want to analyze the data
and gain a better undersanding of the website's strategy and content. You probably also
want to check for technical issues that the site might have.

This module provides a few ready-made functions for helping in anayzing crawl data.

There are certain columns in the crawl DataFrame that can be analyzed separately and
independently, like page size and status codes. They can of course be analyzed together
with other columns like URL and title to put these columns and their data in context.

There are also groups of columns the can be thought of as describing one full aspect of
a website, yet spread across a few columns. For exmaple:

Analyzing crawled images
------------------------

* Image columns: All available image data are extracted, together with all available
  attributes. Each attribute will have its own column, but collectively they would refer
  and belong to the same image (`src`, `alt`, `width`, etc.) So, you can read only
  columns that belong to images using the ``jl_subset`` function:


>>> import advertools as adv
>>> img_df = adv.crawlytics.jl_subset(
        filepath='/path/to/crawl_file.jl', columns=['url', regex='img_'])

This way you are reading `crawl_file.jl`, but only the columns that you chose.
In this case, we selected `url`, as well as any other column that matches the
regex "img_". This can be very helpful in cases where your crawl file is huge and it
would be a waste of memory.

As a next step, you might want to analyze and learn more about the images in the website
you just crawled.

>>> adv.crawlytics.image_summary(img_df)

====  ====================================================  ==============================================================================================================================================================================  =================================================================================================================================================  =============  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ================================  ==============  ===========  ============  ============
  ..  url                                                   img_src                                                                                                                                                                         img_alt                                                                                                                                            img_loading    img_srcset                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  img_sizes                         img_decoding    img_width    img_height      img_border
====  ====================================================  ==============================================================================================================================================================================  =================================================================================================================================================  =============  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ================================  ==============  ===========  ============  ============
   0  https://www.nytimes.com/                              /vi-assets/static-assets/icon-the-morning_144x144-b12a6923b6ad9102b766352261b1a847.webp                                                                                         The Morning Logo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    nan
   0  https://www.nytimes.com/                              /vi-assets/static-assets/icon-the-upshot_144x144-0b1553ff703bbd07ac8fe73e6d215888.webp                                                                                          The Upshot Logo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     nan
   0  https://www.nytimes.com/                              https://static01.nyt.com/images/2017/01/29/podcasts/the-daily-album-art/the-daily-album-art-square320-v5.jpg?quality=75&auto=webp&disable=upscale                               The Daily Logo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      nan
   7  https://www.nytimes.com/news-event/israel-hamas-gaza  https://static01.nyt.com/images/2024/01/25/multimedia/25-israel-hamas-promo-630-mtvp/25-israel-hamas-promo-630-mtvp-articleLarge.jpg                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            async                                               nan
   7  https://www.nytimes.com/news-event/israel-hamas-gaza  https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-thumbLarge.jpg?auto=webp                                                                  A Palestinian man checking the damage inside a building heavily damaged by Israeli bombardment in Rafah, in the southern Gaza Strip, on Thursday.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   nan
   7  https://www.nytimes.com/news-event/israel-hamas-gaza  https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-mediumThreeByTwo225.jpg?auto=webp                                                         A Palestinian man checking the damage inside a building heavily damaged by Israeli bombardment in Rafah, in the southern Gaza Strip, on Thursday.                 https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-videoLarge.jpg?auto=webp 768w, https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-mediumThreeByTwo225.jpg?auto=webp 225w, https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-mediumThreeByTwo440.jpg?auto=webp 440w, https://static01.nyt.com/images/2024/01/25/multimedia/25israel-1-hbcz/25israel-1-hbcz-threeByTwoMediumAt2X.jpg?auto=webp 1500w                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   nan
   8  https://www.nytimes.com/section/world/europe          https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-thumbWide.jpg?quality=75&auto=webp&disable=upscale                                                                                                                                                                    https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-thumbWide.jpg?quality=100&auto=webp 190w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-videoThumb.jpg?quality=100&auto=webp 75w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-videoLarge.jpg?quality=100&auto=webp 768w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-mediumThreeByTwo210.jpg?quality=100&auto=webp 210w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-mediumThreeByTwo225.jpg?quality=100&auto=webp 225w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-mediumThreeByTwo440.jpg?quality=100&auto=webp 440w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-mediumThreeByTwo252.jpg?quality=100&auto=webp 252w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-mediumThreeByTwo378.jpg?quality=100&auto=webp 378w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-threeByTwoLargeAt2X.jpg?quality=100&auto=webp 4000w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-threeByTwoMediumAt2X.jpg?quality=100&auto=webp 1500w,https://static01.nyt.com/images/2024/01/26/multimedia/26ukraine-musician-profile-01-hvwc/26ukraine-musician-profile-01-hvwc-threeByTwoSmallAt2X.jpg?quality=100&auto=webp 600w  (min-width: 1024px) 205px, 150px  async           150          100                    nan
   8  https://www.nytimes.com/section/world/europe          https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-thumbWide.jpg?quality=75&auto=webp&disable=upscale                                                                                                                                                                                      https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-thumbWide.jpg?quality=100&auto=webp 190w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-videoThumb.jpg?quality=100&auto=webp 75w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-videoLarge.jpg?quality=100&auto=webp 768w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-mediumThreeByTwo210.jpg?quality=100&auto=webp 210w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-mediumThreeByTwo225.jpg?quality=100&auto=webp 225w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-mediumThreeByTwo440.jpg?quality=100&auto=webp 440w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-mediumThreeByTwo252.jpg?quality=100&auto=webp 252w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-mediumThreeByTwo378.jpg?quality=100&auto=webp 378w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-threeByTwoLargeAt2X.jpg?quality=100&auto=webp 4797w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-threeByTwoMediumAt2X.jpg?quality=100&auto=webp 1500w,https://static01.nyt.com/images/2024/01/24/multimedia/00uk-charles-surgery-vfzp/00uk-charles-surgery-vfzp-threeByTwoSmallAt2X.jpg?quality=100&auto=webp 600w                                                                                                                                                                                                        (min-width: 1024px) 205px, 150px  async           150          100                    nan
   8  https://www.nytimes.com/section/world/europe          https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-thumbWide.jpg?quality=75&auto=webp&disable=upscale                                                                                                                                                                            https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-thumbWide.jpg?quality=100&auto=webp 190w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-videoThumb.jpg?quality=100&auto=webp 75w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-videoLarge.jpg?quality=100&auto=webp 768w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-mediumThreeByTwo210.jpg?quality=100&auto=webp 210w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-mediumThreeByTwo225.jpg?quality=100&auto=webp 225w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-mediumThreeByTwo440.jpg?quality=100&auto=webp 440w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-mediumThreeByTwo252.jpg?quality=100&auto=webp 252w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-mediumThreeByTwo378.jpg?quality=100&auto=webp 378w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-threeByTwoLargeAt2X.jpg?quality=100&auto=webp 4583w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-threeByTwoMediumAt2X.jpg?quality=100&auto=webp 1500w,https://static01.nyt.com/images/2024/01/26/multimedia/26ambriefing-asia-nl-GAZA-jmcg/26ambriefing-asia-nl-GAZA-jmcg-threeByTwoSmallAt2X.jpg?quality=100&auto=webp 600w                                                                                          (min-width: 1024px) 205px, 150px  async           150          100                    nan
====  ====================================================  ==============================================================================================================================================================================  =================================================================================================================================================  =============  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================  ================================  ==============  ===========  ============  ============

As you can see, we have URLs, together with any column that contains "img_", and now we
have a summary of our images. 

>>> img_df.notna().mean().sort_values(ascending=False).to_frame().style.format('{:.0%}')

============  =====
..                0
============  =====
url               1
img_src       0.976
img_alt       0.976
img_width     0.648
img_height    0.648
img_srcset    0.456
img_sizes     0.456
img_decoding  0.456
img_loading    0.32
img_border        0
============  =====

We can now see that almost all (97.6%) of our images have `src` and `alt` attributes.
About 65% have `width` and `height`, and so on. This immediately gives us an overview of
how our images are managed on the site. We can easily estimate the size of the issues if
any, and plan our work accordingly.

Handling very large crawl files
-------------------------------

Many times you might end up crawling a large website, and the crawl file file might as
large as your memory (or even more), making it impossible to analyze.

This is where we can use the ``jl_subset`` function to only read the column subset that
we want.

>>> crawl_subset = adv.crawlytics.jl_subset(
        filepath='/path/to/crawl_file.jl', columns=[col1, col2, ...], regex=column_regex)

You can use the ``columns`` parameter to specify exactly which columns you want. You can
also use a regular expression to specify a set of columns. Here are some examples of
regular expressions that you might typically want to use:

* "img_": Get all image columns, including all availabe `<img>` attributes.
* "jsonld_": Get all JSON-LD columns.
* "resp_headers_": Response headers.
* "request_headers_": Request headers.
* "h\d": Heading columns, h1..h6.
* "redirect_": Columns containing redirect information.
* "links_": Columns containing link information.

An important characteristic of these groups of columns is that you mostly don't know
how many they are, and what they might include, so a regular expression can save a lot
of time.

Compressing large crawl files
-----------------------------

Another strategy while dealing with large jsonlines (.jl) files is to convert them to
the highly performant `.parquet` format. You simply have to provide the current path to
the .jl file, and provide a path for the desired .parquet file:

>>> adv.crawlytics.jl_to_parquet(PATH_TO_JL, PATH_TO_PARQUET)



"""

import re

import pandas as pd
import pyarrow.parquet as pq

__all__ = [
    "image_summary",
    "jl_subset",
    "jl_to_parquet",
    "link_summary",
    "parquet_columns",
    "redirects",
]


def redirects(crawldf):
    """Create a tidy DataFrame for redirects with the columns:

    url: All the URLs in the redirect chain.
    status: The status code of each URL.
    type: "requested", "inermediate", or "crawled".
    order: 1, 2, 3... up to the number of urls in the redirect chain.
    redirect_times: The number of redirects in the chain (URLs in the chain minus one).

    Parameters:
    -----------
    crawldf : pandas.DataFrame
      A DataFrame of an advertools crawl file
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
            "requested"
            if o == min(order)
            else "crawled"
            if o == max(order)
            else "intermediate"
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


def link_summary(crawldf, internal_url_regex=None):
    """Get a DataFrame summary of links from a crawl DataFrame

    Parameters:
    -----------
    crawldf : DataFrame
      A DataFrame of a website crawled with advertools.
    internal_url_regex : str
      A regular expression for identifying if a link is internal or not.
      For example if your website is example.com, this would be "example.com".

    Returns:
    --------
    link_df : pandas.DataFrame
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


def image_summary(crawldf):
    """Get a DataFrame summary of images in a crawl DataFrame.

    Parameters
    ----------
    crawldf : pandas.DataFrame
      A crawl DataFrame as a result of the advertools.crawl function.

    Returns
    -------
    img_summary : pandas.DataFrame
      A DataFrame containing all available img tags mapped to their respective URLs
      where each image data is represented in a row.
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
    """Read a jsonlines file only extracting selected columns and/or a regex.

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

    # Read only the columns "url" and "meta_desc":
    >>> adv.crawlytics.jl_subset('output_file.jl', columns=['url', 'meta_desc'])

    # Read columns matching the regex "jsonld":
    >>> adv.crawlytics.jl_subset('output_file.jl', regex='jsonld')

    # Read only the columns "url" and "meta_desc" as well as columns matching teh regex "jsonld":
    >>> adv.crawlytics.jl_subset('output_file.jl', columns=['url', 'meta_desc'], regex='jsonld')

    Returns
    -------
    df_subset : pandas.DataFrame
      A DataFrame containing the list of `column` and/or columns matching `regex`.
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
