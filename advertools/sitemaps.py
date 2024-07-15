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
URLs then you can do some good analysis on their content over time as well.

The :func:`sitemap_to_df` function is very simple to use, and only requires the
URL of a sitemap, a sitemap index, or even a robots.txt file. It goes through
the sitemap(s) and returns a DataFrame containing all the tags and their
information.

*  `loc`: The location of the URLs of hte sitemaps.
*  `lastmod`: The datetime of the date when each URL was last modified, if
   available.
*  `sitemap`: The URL of the sitemap from which the URL on this row was
   retreived.
*  `etag`: The entity tag of the response header, if provided.
*  `sitemap_last_modified`: The datetime when the sitemap file was last
   modified, if provided.
*  `sitemap_size_mb`: The size of the sitemap in mega bytes
   (1MB = 1,024 x 1,024 bytes)
*  `download_date`: The datetime when the sitemap was downloaded.

Sitemap Index
-------------
Large websites typically have a sitmeapindex file, which contains links to all
other regular sitemaps that belong to the site. The :func:`sitemap_to_df`
function retreives all sub-sitemaps recursively by default.
In some cases, especially with very large sites, it might be better to first
get the sitemap index, explore its structure, and then decide which sitemaps
you want to get, or if you want them all. Even with smaller websites, it still
might be interesting to get the index only and see how it is structured.

This behavior can be modified by the ``recursive`` parameter, which is set to
`True` by default. Set it to `False` if you want only the index file.

Another interesting thing you might want to do is to provide a robots.txt URL,
and set `recursive=False` to get all available sitemap index files.

>>> sitemap_to_df("https://example.com/robots.txt", recursive=False)

Let's now go through a quick example of what can be done with sitemaps. We can
start by getting one of the BBC's sitemaps.

Regular XML Sitemaps
--------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv

    bbc_sitemap = adv.sitemap_to_df('https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml')
    bbc_sitemap.head(10)

====  =============================================================================  =========================  ============================================================  ================================  =========================  =================  ================================
  ..  loc                                                                            lastmod                    sitemap                                                       etag                              sitemap_last_modified        sitemap_size_mb  download_date
====  =============================================================================  =========================  ============================================================  ================================  =========================  =================  ================================
   0  https://www.bbc.com/arabic/middleeast/2009/06/090620_as_iraq_explosion_tc2     2009-06-20 14:10:48+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   1  https://www.bbc.com/arabic/middleeast/2009/06/090620_iraq_blast_tc2            2009-06-20 21:07:43+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   2  https://www.bbc.com/arabic/business/2009/06/090622_me_worldbank_tc2            2009-06-22 12:41:48+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   3  https://www.bbc.com/arabic/multimedia/2009/06/090624_me_inpictures_brazil_tc2  2009-06-24 15:27:24+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   4  https://www.bbc.com/arabic/business/2009/06/090618_tomtest                     2009-06-18 15:32:54+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   5  https://www.bbc.com/arabic/multimedia/2009/06/090625_sf_tamim_verdict_tc2      2009-06-25 09:46:39+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   6  https://www.bbc.com/arabic/middleeast/2009/06/090623_iz_cairo_russia_tc2       2009-06-23 13:10:56+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   7  https://www.bbc.com/arabic/sports/2009/06/090622_me_egypt_us_tc2               2009-06-22 15:37:07+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   8  https://www.bbc.com/arabic/sports/2009/06/090624_mz_wimbledon_tc2              2009-06-24 13:57:18+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
   9  https://www.bbc.com/arabic/worldnews/2009/06/090623_mz_leaders_lifespan_tc2    2009-06-23 13:24:23+00:00  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml  e7e15811c65f406f89f89fe10aef29f5  2021-11-05 20:52:56+00:00            7.63124  2022-02-12 01:37:39.461037+00:00
====  =============================================================================  =========================  ============================================================  ================================  =========================  =================  ================================

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    print(bbc_sitemap.shape)
    print(bbc_sitemap.dtypes)

.. code-block::

    (49999, 7)

    loc                                   object
    lastmod                  datetime64[ns, UTC]
    sitemap                               object
    etag                                  object
    sitemap_last_modified    datetime64[ns, UTC]
    sitemap_size_mb                      float64
    download_date            datetime64[ns, UTC]
    dtype: object

Since ``lastmod`` is a ``datetime`` object, we can easily use it for various
time-related operations.
Here we look at how many articles have been published (last modified) per year.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    bbc_sitemap.set_index('lastmod').resample('A')['loc'].count()

.. code-block::

    lastmod
    2008-12-31 00:00:00+00:00     2287
    2009-12-31 00:00:00+00:00    47603
    2010-12-31 00:00:00+00:00        0
    2011-12-31 00:00:00+00:00        0
    2012-12-31 00:00:00+00:00        0
    2013-12-31 00:00:00+00:00        0
    2014-12-31 00:00:00+00:00        0
    2015-12-31 00:00:00+00:00        0
    2016-12-31 00:00:00+00:00        0
    2017-12-31 00:00:00+00:00        0
    2018-12-31 00:00:00+00:00        0
    2019-12-31 00:00:00+00:00       99
    2020-12-31 00:00:00+00:00       10
    Freq: A-DEC, Name: loc, dtype: int64

As the majority are in 2009 with a few in other years, it seems these were
later updated, but we would have to check to verify (in this special case BBC's
URLs contain date information, which can be compared to ``lastmod`` to check if
there is a difference between them).

We can take a look at a sample of the URLs to get the URL template that they
use.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    bbc_sitemap['loc'].sample(10).tolist()

.. code-block::

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

This is quite a rich structure, full of useful information. We can
:ref:`analyze the URL structure <urlytics>` using the ``url_to_df`` function:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    url_df = adv.url_to_df(bbc_sitemap['loc'])
    url_df

=====  =============================================================================  ========  ===========  ==========================================================  =======  ==========  ==========  ==========  =======  =======  ===============================  =======  =======  ===============================
   ..  url                                                                            scheme    netloc       path                                                        query    fragment    dir_1       dir_2         dir_3    dir_4  dir_5                              dir_6    dir_7  last_dir
=====  =============================================================================  ========  ===========  ==========================================================  =======  ==========  ==========  ==========  =======  =======  ===============================  =======  =======  ===============================
    0  https://www.bbc.com/arabic/middleeast/2009/06/090620_as_iraq_explosion_tc2     https     www.bbc.com  /arabic/middleeast/2009/06/090620_as_iraq_explosion_tc2                          arabic      middleeast     2009       06  090620_as_iraq_explosion_tc2         nan      nan  090620_as_iraq_explosion_tc2
    1  https://www.bbc.com/arabic/middleeast/2009/06/090620_iraq_blast_tc2            https     www.bbc.com  /arabic/middleeast/2009/06/090620_iraq_blast_tc2                                 arabic      middleeast     2009       06  090620_iraq_blast_tc2                nan      nan  090620_iraq_blast_tc2
    2  https://www.bbc.com/arabic/business/2009/06/090622_me_worldbank_tc2            https     www.bbc.com  /arabic/business/2009/06/090622_me_worldbank_tc2                                 arabic      business       2009       06  090622_me_worldbank_tc2              nan      nan  090622_me_worldbank_tc2
    3  https://www.bbc.com/arabic/multimedia/2009/06/090624_me_inpictures_brazil_tc2  https     www.bbc.com  /arabic/multimedia/2009/06/090624_me_inpictures_brazil_tc2                       arabic      multimedia     2009       06  090624_me_inpictures_brazil_tc2      nan      nan  090624_me_inpictures_brazil_tc2
    4  https://www.bbc.com/arabic/business/2009/06/090618_tomtest                     https     www.bbc.com  /arabic/business/2009/06/090618_tomtest                                          arabic      business       2009       06  090618_tomtest                       nan      nan  090618_tomtest
49994  https://www.bbc.com/vietnamese/world/2009/08/090831_dalailamataiwan            https     www.bbc.com  /vietnamese/world/2009/08/090831_dalailamataiwan                                 vietnamese  world          2009       08  090831_dalailamataiwan               nan      nan  090831_dalailamataiwan
49995  https://www.bbc.com/vietnamese/world/2009/09/090901_putin_regret_pact          https     www.bbc.com  /vietnamese/world/2009/09/090901_putin_regret_pact                               vietnamese  world          2009       09  090901_putin_regret_pact             nan      nan  090901_putin_regret_pact
49996  https://www.bbc.com/vietnamese/culture/2009/09/090901_tiananmen_movie          https     www.bbc.com  /vietnamese/culture/2009/09/090901_tiananmen_movie                               vietnamese  culture        2009       09  090901_tiananmen_movie               nan      nan  090901_tiananmen_movie
49997  https://www.bbc.com/vietnamese/pictures/2009/08/090830_ugc_ddh_sand            https     www.bbc.com  /vietnamese/pictures/2009/08/090830_ugc_ddh_sand                                 vietnamese  pictures       2009       08  090830_ugc_ddh_sand                  nan      nan  090830_ugc_ddh_sand
49998  https://www.bbc.com/vietnamese/business/2009/09/090901_japecontask             https     www.bbc.com  /vietnamese/business/2009/09/090901_japecontask                                  vietnamese  business       2009       09  090901_japecontask                   nan      nan  090901_japecontask
=====  =============================================================================  ========  ===========  ==========================================================  =======  ==========  ==========  ==========  =======  =======  ===============================  =======  =======  ===============================

It seems that the ``dir_1`` is where they have the language information, so we
can easily count how many articles they have per language:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    url_df['dir_1'].value_counts()

.. code-block::

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
    Name: dir_1, dtype: int64

We can also get a subset of articles written in a certain language, and see how
many articles they publish per month, week, year, etc.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    (bbc_sitemap[bbc_sitemap['loc']
     .str.contains('/russian/')]
     .set_index('lastmod')
     .resample('M')['loc'].count())

.. code-block::

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

The topic or category of the article seems to be in ``dir_2`` for which we can
do the same and count the values.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    url_df['dir_2'].value_counts()[:20]

.. code-block::

    rolling_news        9044
    world               5050
    noticias            4224
    iran                3682
    pakistan            2103
    afghanistan         1959
    multimedia          1657
    internacional       1555
    sport               1350
    international       1293
    india               1285
    america_latina      1274
    business            1204
    cultura_sociedad     913
    middleeast           874
    worldnews            872
    russia               841
    radio                769
    science              755
    football             674
    Name: dir_2, dtype: int64

There is much more you can do, and a lot depends on the URL structure, which
you have to explore and run the right operation.

For example, we can use the ``last_dir`` column which contains the slugs
of the articles, replace underscores with spaces, split, concatenate all, put
in a ``pd.Series`` and count the values. This way we see how many times each
word occurred in an article. The same code can also be run after filtering for
articles in a particular language to get a more meaningful list of words.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    url_df['last_dir'].str.split('_').str[1:].explode().value_counts()[:20]

.. code-block::

    rn          8808
    tc2         3153
    iran        1534
    video        973
    obama        882
    us           862
    china        815
    ir88         727
    russia       683
    si           640
    np           638
    afghan       632
    ka           565
    an           556
    iraq         554
    pakistan     547
    nh           533
    cq           520
    zs           510
    ra           491
    Name: last_dir, dtype: int64

This was a quick overview and data preparation for a sample sitemap. Once you
are familiar with the sitemap's structure, you can more easily start analyzing
the content.

.. note::

    There is a bug currently with tags that contain multiple values in
    sitemaps. If an image column in a news sitemap contains multiple images,
    only the last one is retreived. The same applies for any other sitemap that
    has a tag with multiple values.


News Sitemaps
-------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    nyt_news = adv.sitemap_to_df('https://www.nytimes.com/sitemaps/new/news.xml.gz')
    print(nyt_news.shape)
    # (5085, 16)
    nyt_news

====  =======================================================================================================  =========================  ======  ==================  ==================  ======================  =======================  ====================================================================================  ========================================================================================================================  =======  ==================================================================================================================================================================================  ==================================================  ================================  =========================  =================  ================================
  ..  loc                                                                                                      lastmod                    news    news_publication    publication_name    publication_language    news_publication_date    news_title                                                                            news_keywords                                                                                                             image    image_loc                                                                                                                                                                           sitemap                                             etag                              sitemap_last_modified        sitemap_size_mb  download_date
====  =======================================================================================================  =========================  ======  ==================  ==================  ======================  =======================  ====================================================================================  ========================================================================================================================  =======  ==================================================================================================================================================================================  ==================================================  ================================  =========================  =================  ================================
   0  https://www.nytimes.com/interactive/2021/us/ottawa-ohio-covid-cases.html                                 2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Ottawa County, Ohio Covid Case and Exposure Risk Tracker                              Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/ohio-coronavirus-cases-promo-1585539358901/ohio-coronavirus-cases-promo-1585539358901-articleLarge-v274.png                           https://www.nytimes.com/sitemaps/new/news-6.xml.gz  0cff645fbb74c21791568b78a888967d  2022-02-12 20:17:31+00:00          0.0774069  2022-02-12 20:18:39.744247+00:00
   1  https://www.nytimes.com/interactive/2021/us/hopewell-virginia-covid-cases.html                           2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Hopewell, Virginia Covid Case and Exposure Risk Tracker                               Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/virginia-coronavirus-cases-promo-1585539536519/virginia-coronavirus-cases-promo-1585539536519-articleLarge-v271.png                   https://www.nytimes.com/sitemaps/new/news-6.xml.gz  0cff645fbb74c21791568b78a888967d  2022-02-12 20:17:31+00:00          0.0774069  2022-02-12 20:18:39.744247+00:00
   2  https://www.nytimes.com/interactive/2021/us/box-butte-nebraska-covid-cases.html                          2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Box Butte County, Nebraska Covid Case and Exposure Risk Tracker                       Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/nebraska-coronavirus-cases-promo-1585539237156/nebraska-coronavirus-cases-promo-1585539237156-articleLarge-v281.png                   https://www.nytimes.com/sitemaps/new/news-6.xml.gz  0cff645fbb74c21791568b78a888967d  2022-02-12 20:17:31+00:00          0.0774069  2022-02-12 20:18:39.744247+00:00
   3  https://www.nytimes.com/interactive/2021/us/stearns-minnesota-covid-cases.html                           2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Stearns County, Minnesota Covid Case and Exposure Risk Tracker                        Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/minnesota-coronavirus-cases-promo-1585539172701/minnesota-coronavirus-cases-promo-1585539172701-articleLarge-v282.png                 https://www.nytimes.com/sitemaps/new/news-6.xml.gz  0cff645fbb74c21791568b78a888967d  2022-02-12 20:17:31+00:00          0.0774069  2022-02-12 20:18:39.744247+00:00
   4  https://www.nytimes.com/interactive/2021/us/benton-iowa-covid-cases.html                                 2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Benton County, Iowa Covid Case and Exposure Risk Tracker                              Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/iowa-coronavirus-cases-promo-1585539039190/iowa-coronavirus-cases-promo-1585539039190-articleLarge-v286.png                           https://www.nytimes.com/sitemaps/new/news-6.xml.gz  0cff645fbb74c21791568b78a888967d  2022-02-12 20:17:31+00:00          0.0774069  2022-02-12 20:18:39.744247+00:00
5080  https://www.nytimes.com/interactive/2021/us/hodgeman-kansas-covid-cases.html                             2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Hodgeman County, Kansas Covid Case and Exposure Risk Tracker                          Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/kansas-coronavirus-cases-promo-1585539054298/kansas-coronavirus-cases-promo-1585539054298-articleLarge-v285.png                       https://www.nytimes.com/sitemaps/new/news-2.xml.gz  f53301c8286f9bf59ef297f0232dcfc1  2022-02-12 20:17:31+00:00          0.914107   2022-02-12 20:18:39.995323+00:00
5081  https://www.nytimes.com/interactive/2021/us/miller-georgia-covid-cases.html                              2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Miller County, Georgia Covid Case and Exposure Risk Tracker                           Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/georgia-coronavirus-cases-promo-1585538956622/georgia-coronavirus-cases-promo-1585538956622-articleLarge-v290.png                     https://www.nytimes.com/sitemaps/new/news-2.xml.gz  f53301c8286f9bf59ef297f0232dcfc1  2022-02-12 20:17:31+00:00          0.914107   2022-02-12 20:18:39.995323+00:00
5082  https://www.nytimes.com/interactive/2020/11/03/us/elections/results-west-virginia-house-district-1.html  2022-02-12 00:00:00+00:00                              The New York Times  en                      2020-11-03T17:00:00Z     West Virginia First Congressional District Results: David McKinley vs. Natalie Cline  Elections, Presidential Election of 2020, United States, internal-election-open, House of Representatives, West Virginia           https://static01.nyt.com/images/2020/11/03/us/elections/eln-promo-race-west-virginia-house-1WINNER-mckinleyd/eln-promo-race-west-virginia-house-1WINNER-mckinleyd-articleLarge.png  https://www.nytimes.com/sitemaps/new/news-2.xml.gz  f53301c8286f9bf59ef297f0232dcfc1  2022-02-12 20:17:31+00:00          0.914107   2022-02-12 20:18:39.995323+00:00
5083  https://www.nytimes.com/interactive/2020/11/03/us/elections/results-maine-senate.html                    2022-02-12 00:00:00+00:00                              The New York Times  en                      2020-11-03T17:00:00Z     Maine Senate Results: Susan Collins Defeats Sara Gideon                               Elections, Presidential Election of 2020, United States, internal-election-open, Senate, Maine                                     https://static01.nyt.com/images/2020/11/03/us/elections/eln-promo-race-maine-senateWINNER-collinss/eln-promo-race-maine-senateWINNER-collinss-articleLarge.png                      https://www.nytimes.com/sitemaps/new/news-2.xml.gz  f53301c8286f9bf59ef297f0232dcfc1  2022-02-12 20:17:31+00:00          0.914107   2022-02-12 20:18:39.995323+00:00
5084  https://www.nytimes.com/interactive/2021/us/randolph-missouri-covid-cases.html                           2022-02-12 00:00:00+00:00                              The New York Times  en                      2021-01-27T17:00:00Z     Randolph County, Missouri Covid Case and Exposure Risk Tracker                        Coronavirus (2019-nCoV), States (US), Deaths (Fatalities), United States, Disease Rates                                            https://static01.nyt.com/images/2020/03/29/us/missouri-coronavirus-cases-promo-1585539206866/missouri-coronavirus-cases-promo-1585539206866-articleLarge-v282.png                   https://www.nytimes.com/sitemaps/new/news-2.xml.gz  f53301c8286f9bf59ef297f0232dcfc1  2022-02-12 20:17:31+00:00          0.914107   2022-02-12 20:18:39.995323+00:00
====  =======================================================================================================  =========================  ======  ==================  ==================  ======================  =======================  ====================================================================================  ========================================================================================================================  =======  ==================================================================================================================================================================================  ==================================================  ================================  =========================  =================  ================================

Video Sitemaps
--------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    wired_video = adv.sitemap_to_df('https://www.wired.com/video/sitemap.xml')
    print(wired_video.shape)
    # (2955, 14)
    wired_video

====  ==============================================================================================================  =======  ======================================================================================================================================================================================================================================  ==============================================================================  ==========================================================================================================================================================================================================================================================================================================================================  ========================================================================================================  ================  =========================  =======================  =========  =======================================  ==================================  =================  ================================
  ..  loc                                                                                                             video    video_thumbnail_loc                                                                                                                                                                                                                     video_title                                                                     video_description                                                                                                                                                                                                                                                                                                                           video_content_loc                                                                                           video_duration  video_publication_date       video_expiration_date  lastmod    sitemap                                  etag                                  sitemap_size_mb  download_date
====  ==============================================================================================================  =======  ======================================================================================================================================================================================================================================  ==============================================================================  ==========================================================================================================================================================================================================================================================================================================================================  ========================================================================================================  ================  =========================  =======================  =========  =======================================  ==================================  =================  ================================
   0  https://www.wired.com/video/watch/autocomplete-inverviews-owen-wilson-answers-the-webs-most-searched-questions           http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1644595412/wired_autocomplete-inverviews-owen-wilson-answers-the-webs-most-searched-questions.jpg  Autocomplete Interview - Owen Wilson Answers The Web’s Most Searched Questions  Owen Wilson takes the WIRED Autocomplete Interview and answers the internet's most searched questions about himself. How did Owen Wilson break his nose? How many movies is he in with Ben Stiller? Is Owen in every Wes Anderson movie? Is he a good skateboarder? Owen answers all these questions and much more!                         http://dp8hsntg6do36.cloudfront.net/62067f085577c277dd9acf42/39687acb-505b-4c69-94f1-afaa7cb5e636low.mp4               645  2022-02-11T17:00:00+00:00                      nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
   1  https://www.wired.com/video/watch/wired-news-and-science-samsung-s22                                                     http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1644418652/wired_wired-news-and-science-samsung-s22.jpg                                            Currents - Samsung S22 Ultra Explained in 3 Minutes                             Julian Chokkattu, Reviews Editor for WIRED, walks us through a few of the Samsung S22 Ultra's new features.                                                                                                                                                                                                                                 http://dp8hsntg6do36.cloudfront.net/6203cd7b5577c23d19622259/fe546b9b-a320-4883-9cbd-0d790f23c36dlow.mp4               184  2022-02-10T17:00:00+00:00                      nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
   2  https://www.wired.com/video/watch/first-look-samsung-galaxy-unpacked-2022                                                http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1644381627/wired_first-look-samsung-galaxy-unpacked-2022.jpg                                       First Look: Samsung Galaxy Unpacked 2022                                        Samsung has debuted three new smartphones—the Galaxy S22 Ultra, S22+, S22—and three Android tablets in various sizes at Samsung Unpacked 2022. WIRED's Julian Chokkattu takes a look at the newest features.                                                                                                                                http://dp8hsntg6do36.cloudfront.net/620345a15577c23d46622256/d74930cf-11e1-466e-b023-1d9b91664204low.mp4               373  2022-02-09T15:00:00+00:00                      nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
   3  https://www.wired.com/video/watch/reinventing-with-data                                                                  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1642801328/wired_reinventing-with-data.jpg                                                         Reinventing With Data | WIRED Brand Lab                                         Produced by WIRED Brand Lab with AWS | What can the Seattle Seahawks winning strategy teach businesses?                                                                                                                                                                                                                                     http://dp8hsntg6do36.cloudfront.net/619bd9be1d75db41adee6b58/d4889b15-4f34-41b0-b935-0c79465a9793low.mp4               292  2022-02-09T13:00:00+00:00                      nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
                                                                                                                                                                                                                                                                                                                                                                                                                                                       Swami Sivasubramanian, VP of AI at Amazon Web Services helps us to understand how the Seattle Seahawks are using data and AI to remain a top performing team in the NFL, and how their process of data capture, storage, and machine learning to gain strategic insights is a model for making better business decision across industries.
   4  https://www.wired.com/video/watch/seth-rogen-answers-the-webs-most-searched-questions                                    http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1644335726/wired_seth-rogen-answers-the-webs-most-searched-questions.jpg                           Autocomplete Interview - Seth Rogen Answers The Web’s Most Searched Questions   "Pam &amp; Tommy" star Seth Rogen takes the WIRED Autocomplete Interview once again and answers the internet's most searched questions about himself. Who does Seth Rogen look like? Does Seth have a podcast? Does he sell pottery? Does he celebrate Christmas? Does he play Call of Duty?                                                http://dp8hsntg6do36.cloudfront.net/6201430a1d75db06ae1f62e8/488ed635-91d0-4281-9e64-34be9bf74f00low.mp4               635  2022-02-08T17:00:00+00:00                      nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00

                                                                                                                                                                                                                                                                                                                                                                                                                                                       Pam &amp; Tommy premieres February 2 on Hulu (finale on March 9)
2950  https://www.wired.com/video/genres/how-to                                                                       nan      nan                                                                                                                                                                                                                                     nan                                                                             nan                                                                                                                                                                                                                                                                                                                                         nan                                                                                                                    nan  nan                                            nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
2951  https://www.wired.com/video/genres/movies-tv                                                                    nan      nan                                                                                                                                                                                                                                     nan                                                                             nan                                                                                                                                                                                                                                                                                                                                         nan                                                                                                                    nan  nan                                            nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
2952  https://www.wired.com/video/genres/events                                                                       nan      nan                                                                                                                                                                                                                                     nan                                                                             nan                                                                                                                                                                                                                                                                                                                                         nan                                                                                                                    nan  nan                                            nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
2953  https://www.wired.com/video/genres/promotion                                                                    nan      nan                                                                                                                                                                                                                                     nan                                                                             nan                                                                                                                                                                                                                                                                                                                                         nan                                                                                                                    nan  nan                                            nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
2954  https://www.wired.com/video/genres/transportation                                                               nan      nan                                                                                                                                                                                                                                     nan                                                                             nan                                                                                                                                                                                                                                                                                                                                         nan                                                                                                                    nan  nan                                            nan  NaT        https://www.wired.com/video/sitemap.xml  W/90b11f47f8b2ab57cb180cbd3c6f06f9            2.86199  2022-02-12 20:24:55.841851+00:00
====  ==============================================================================================================  =======  ======================================================================================================================================================================================================================================  ==============================================================================  ==========================================================================================================================================================================================================================================================================================================================================  ========================================================================================================  ================  =========================  =======================  =========  =======================================  ==================================  =================  ================================

Request Headers
---------------
You can set and change any request header while runnig this function if you want to
modify its behavior. This can be done using a simple dictionary, where the keys are the
names of the headers and values are their values.

For example, one of the common use-cases is to set a different User-agent than the
default one:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    adv.sitemap_to_df("https://www.ft.com/sitemaps/news.xml", headers={"User-agent": "YOUR-USER-AGENT"})

Another interesting thing you might want to do is utilize the `If-None-Match` header.
In many cases the sitemaps return an etag for the sitemap. This is to make it easier to
know whether or not a sitemap has changed. A different etag means the sitemap has been
updated/changed.

With large sitemaps, where many sub-sitemaps don't change that much you don't need to
re-download the sitemap every time. You can simply use this header which would download
the sitemap only if it has a different etag. This can also be useful with frequently
changing sitemaps like news sitemaps for example. In this case you probably want to
constantly check but only fetch the sitemap if it was changed.


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    # First time:
    ft = adv.sitemap_to_df("https://www.ft.com/sitemaps/news.xml")
    etag = ft['etag'][0]

    # Second time:
    ft = adv.sitemap_to_df("https://www.ft.com/sitemaps/news.xml", headers={"If-None-Match": etag})
"""  # noqa: E501

import logging
from concurrent import futures
from gzip import GzipFile
from urllib.request import Request, urlopen
from xml.etree import ElementTree

import pandas as pd

from advertools import __version__ as version

logging.basicConfig(level=logging.INFO)

headers = {"User-Agent": "advertools-" + version}


def _sitemaps_from_robotstxt(robots_url, request_headers):
    sitemaps = []
    robots_page = urlopen(Request(robots_url, headers=request_headers))
    for line in robots_page.readlines():
        line_split = [s.strip() for s in line.decode().split(":", maxsplit=1)]
        if line_split[0].lower() == "sitemap":
            sitemaps.append(line_split[1])
    return sitemaps


def _parse_sitemap(root):
    d = dict()
    for node in root:
        for n in node:
            if "loc" in n.tag:
                d[n.text] = {}

    def parse_xml_node(node, node_url, prefix=""):
        nonlocal d
        keys = []
        for element in node:
            if element.text:
                tag = element.tag.split("}")[-1]
                d[node_url][prefix + tag] = element.text
                keys.append(tag)
                prefix = prefix if tag in keys else ""
            if list(element):
                parse_xml_node(
                    element, node_url, prefix=element.tag.split("}")[-1] + "_"
                )

    for node in root:
        node_url = [n.text for n in node if "loc" in n.tag][0]
        parse_xml_node(node, node_url=node_url)
    return pd.DataFrame(d.values())


def _build_request_headers(user_headers=None):
    # Must ensure lowercase to avoid introducing duplicate keys
    final_headers = {key.lower(): val for key, val in headers.items()}
    if user_headers:
        user_headers = {key.lower(): val for key, val in user_headers.items()}
        final_headers.update(user_headers)
    return final_headers


def sitemap_to_df(sitemap_url, max_workers=8, recursive=True, request_headers=None):
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
    :param int max_workers: The maximum number of workers to use for threading.
                            The higher the faster, but with high numbers you
                            risk being blocked and/or missing some data as you
                            might appear like an attacker.
    :param bool recursive: Whether or not to follow and import all sub-sitemaps
                           (in case you have a sitemap index), or to only
                           import the given sitemap. This might be useful in
                           case you want to explore what sitemaps are available
                           after which you can decide which ones you are
                           interested in.
    :param dict request_headers: One or more request headers to use while
                                 fetching the sitemap.
    :return sitemap_df: A pandas DataFrame containing all URLs, as well as
                        other tags if available (``lastmod``, ``changefreq``,
                        ``priority``, or others found in news, video, or image
                        sitemaps).
    """
    final_headers = _build_request_headers(request_headers)

    if sitemap_url.endswith("robots.txt"):
        return pd.concat(
            [
                sitemap_to_df(sitemap, recursive=recursive)
                for sitemap in _sitemaps_from_robotstxt(sitemap_url, final_headers)
            ],
            ignore_index=True,
        )

    if sitemap_url.endswith("xml.gz"):
        final_headers["accept-encoding"] = "gzip"
        xml_text = urlopen(
            Request(
                sitemap_url,
                headers=final_headers,
            )
        )
        try:
            resp_headers = xml_text.getheaders()
        except AttributeError:
            resp_headers = ""
            pass
        xml_text = GzipFile(fileobj=xml_text)
    else:
        xml_text = urlopen(Request(sitemap_url, headers=final_headers))
        try:
            resp_headers = xml_text.getheaders()
        except AttributeError:
            resp_headers = ""
            pass
    xml_string = xml_text.read()
    root = ElementTree.fromstring(xml_string)

    sitemap_df = pd.DataFrame()

    if (root.tag.split("}")[-1] == "sitemapindex") and recursive:
        multi_sitemap_df = pd.DataFrame()
        sitemap_url_list = []
        for elem in root:
            for el in elem:
                if "loc" in el.tag:
                    if el.text == sitemap_url:
                        error_df = pd.DataFrame(
                            {
                                "sitemap": [sitemap_url],
                                "errors": [
                                    "WARNING: Sitemap contains a link to itself"
                                ],
                            }
                        )
                        multi_sitemap_df = pd.concat(
                            [multi_sitemap_df, error_df], ignore_index=True
                        )
                    else:
                        sitemap_url_list.append(el.text)
        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            to_do = []
            for sitemap in sitemap_url_list:
                future = executor.submit(sitemap_to_df, sitemap)
                to_do.append(future)
            done_iter = futures.as_completed(to_do)
            for future in done_iter:
                try:
                    multi_sitemap_df = pd.concat(
                        [multi_sitemap_df, future.result()], ignore_index=True
                    )
                except Exception as e:
                    error_df = pd.DataFrame(dict(errors=str(e)), index=range(1))
                    future_str = hex(id(future))
                    hexes = [hex(id(f)) for f in to_do]
                    index = hexes.index(future_str)
                    error_df["sitemap"] = sitemap_url_list[index]
                    logging.warning(msg=str(e) + " " + sitemap_url_list[index])
                    multi_sitemap_df = pd.concat(
                        [multi_sitemap_df, error_df], ignore_index=True
                    )
        return multi_sitemap_df

    else:
        logging.info(msg="Getting " + sitemap_url)
        elem_df = _parse_sitemap(root)
        sitemap_df = pd.concat([sitemap_df, elem_df], ignore_index=True)
        sitemap_df["sitemap"] = [sitemap_url] if sitemap_df.empty else sitemap_url
    if "lastmod" in sitemap_df:
        try:
            sitemap_df["lastmod"] = pd.to_datetime(sitemap_df["lastmod"], utc=True)
        except Exception:
            pass
    if "priority" in sitemap_df:
        try:
            sitemap_df["priority"] = sitemap_df["priority"].astype(float)
        except Exception:
            pass
    if resp_headers:
        etag_lastmod = {
            header.lower().replace("-", "_"): val
            for header, val in resp_headers
            if header.lower() in ["etag", "last-modified"]
        }
        sitemap_df = sitemap_df.assign(**etag_lastmod)
    if "last_modified" in sitemap_df:
        sitemap_df["sitemap_last_modified"] = pd.to_datetime(
            sitemap_df["last_modified"]
        )
        del sitemap_df["last_modified"]
    sitemap_df["sitemap_size_mb"] = len(xml_string) / 1024 / 1024
    sitemap_df["download_date"] = pd.Timestamp.now(tz="UTC")
    return sitemap_df
