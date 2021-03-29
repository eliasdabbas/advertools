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

>>> sitemap_to_df('https://example.com/robots.txt', recursive=False)

Let's now go through a quick example of what can be done with sitemaps. We can
start by getting one of the BBC's sitemaps.

Regular XML Sitemaps
--------------------

>>> bbc_sitemap = sitemap_to_df('https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml')
>>> bbc_sitemap.head(10)
	                                                                            loc	                    lastmod	                                                       sitemap	                              etag	      sitemap_last_modified	     sitemap_size_mb	                     download_date
0	     https://www.bbc.com/arabic/middleeast/2009/06/090620_as_iraq_explosion_tc2	  2009-06-20 14:10:48+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
1	            https://www.bbc.com/arabic/middleeast/2009/06/090620_iraq_blast_tc2	  2009-06-20 21:07:43+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
2	            https://www.bbc.com/arabic/business/2009/06/090622_me_worldbank_tc2	  2009-06-22 12:41:48+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
3	  https://www.bbc.com/arabic/multimedia/2009/06/090624_me_inpictures_brazil_tc2	  2009-06-24 15:27:24+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
4	                     https://www.bbc.com/arabic/business/2009/06/090618_tomtest	  2009-06-18 15:32:54+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
5	      https://www.bbc.com/arabic/multimedia/2009/06/090625_sf_tamim_verdict_tc2	  2009-06-25 09:46:39+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
6	       https://www.bbc.com/arabic/middleeast/2009/06/090623_iz_cairo_russia_tc2	  2009-06-23 13:10:56+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
7	               https://www.bbc.com/arabic/sports/2009/06/090622_me_egypt_us_tc2	  2009-06-22 15:37:07+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
8	              https://www.bbc.com/arabic/sports/2009/06/090624_mz_wimbledon_tc2	  2009-06-24 13:57:18+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00
9	    https://www.bbc.com/arabic/worldnews/2009/06/090623_mz_leaders_lifespan_tc2	  2009-06-23 13:24:23+00:00	  https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml	  5f78c818962d9c3656960a852a1fd9a5	  2020-05-27 14:38:31+00:00	  7.6312408447265625	  2021-01-16 20:16:34.403337+00:00

>>> bbc_sitemap.shape
(49999, 7)

>>> bbc_sitemap.dtypes
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

>>> bbc_sitemap.set_index('lastmod').resample('A')['loc'].count()
lastmod
2008-12-31 00:00:00+00:00     2261
2009-12-31 00:00:00+00:00    47225
2010-12-31 00:00:00+00:00        0
2011-12-31 00:00:00+00:00        0
2012-12-31 00:00:00+00:00        0
2013-12-31 00:00:00+00:00        0
2014-12-31 00:00:00+00:00        0
2015-12-31 00:00:00+00:00        0
2016-12-31 00:00:00+00:00        0
2017-12-31 00:00:00+00:00        0
2018-12-31 00:00:00+00:00        0
2019-12-31 00:00:00+00:00      481
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

.. note::

    There is a bug currently with tags that contain multiple values in
    sitemaps. If an image column in a news sitemap contains multiple images,
    only the last one is retreived. The same applies for any other sitemap that
    has a tag with multiple values.


News Sitemaps
-------------

>>> nyt_news = sitemap_to_df('https://www.nytimes.com/sitemaps/new/news.xml.gz')
>>> nyt_news
	                                                                                          loc              	        lastmod       publication_name publication_language	 news_publication_date	                                                                    news_title	                                                                                                                                                                                            news_keywords	            image                                                                                                                                                                    	image_loc                                              sitemap	                              etag        sitemap_last_modified	     sitemap_size_mb	                     download_date
0	                            https://www.nytimes.com/live/2021/01/16/us/inauguration-day-biden	  2021-01-16 20:22:56+00:00	    The New York Times                   en	  2021-01-16T13:58:07Z	  Biden Inauguration, Trump Approval Rating and Protests: Live Weekend Updates	                                                                                                                                                                                                      nan	              nan	                                                                                                                                                                          nan	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
1	           https://www.nytimes.com/live/2021/01/16/science/nasa-space-launch-rocket-fire-test	  2021-01-16 20:18:17+00:00	    The New York Times                   en	  2021-01-16T20:15:56Z	                                Live: NASA’s Space Launch System Hot-Fire Test	                                                                                                                                                                                                      nan	              nan	                                                                                                                                                                          nan	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
2	  https://www.nytimes.com/interactive/2020/obituaries/people-died-coronavirus-obituaries.html	  2021-01-16 20:17:36+00:00	    The New York Times                en-US	  2020-04-16T22:28:14Z	                                                              Those We’ve Lost	                                                                                                                                                             Deaths (Obituaries), Coronavirus (2019-nCoV)	                 	                                        https://static01.nyt.com/images/2020/12/01/obituaries/25Houser/merlin_180391827_78fe8f74-0a8e-43c9-bc96-51859d84c2a5-articleLarge.jpg	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
3	              https://www.nytimes.com/2021/01/16/opinion/coronavirus-biden-vaccine-covid.html	  2021-01-16 20:13:19+00:00	    The New York Times                en-US	  2021-01-16T19:30:07Z	                                           Joe Biden Actually Has a Covid Plan	                                         Coronavirus (2019-nCoV), Contact Tracing (Public Health), Vaccination and Immunization, United States Politics and Government, Biden, Joseph R Jr, United States	                 	                                  https://static01.nyt.com/images/2021/01/17/opinion/16pandemic1-print/merlin_173210889_b98256be-c87b-4a48-b3ab-14c0c064e33f-articleLarge.jpg	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
4	                           https://www.nytimes.com/2021/01/13/opinion/capitol-attack-war.html	  2021-01-16 20:06:43+00:00	    The New York Times                   en	  2021-01-13T10:06:54Z	                                       Why the Capitol Riot Reminded Me of War	                                                                                                    Storming of the US Capitol (Jan, 2021), Video Recordings, Downloads and Streaming, Iraq War (2003-11)	                 	                                                                           https://static01.nyt.com/images/2021/01/18/opinion/sunday/18Ackermann/13Ackermann-articleLarge.jpg	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
5	                   https://www.nytimes.com/interactive/2020/us/wyoming-coronavirus-cases.html	  2021-01-16 20:01:26+00:00	    The New York Times                en-US	  2020-04-01T15:47:57Z	                                        Wyoming Coronavirus Map and Case Count	                                                                                                                                                          Coronavirus (2019-nCoV), Wyoming, Disease Rates	                 	              https://static01.nyt.com/images/2020/03/29/us/wyoming-coronavirus-cases-promo-1585539595289/wyoming-coronavirus-cases-promo-1585539595289-articleLarge-v117.png	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
6	                         https://www.nytimes.com/interactive/2020/world/coronavirus-maps.html	  2021-01-16 20:01:21+00:00	    The New York Times                en-US	  2020-01-28T22:57:20Z	                           Coronavirus World Map: Tracking the Global Outbreak	  Coronavirus (2019-nCoV), Epidemics, Centers for Disease Control and Prevention, Johns Hopkins University, Wuhan (China), China, United States, Australia, Singapore, Disease Rates, Deaths (Fatalities)	                 	        https://static01.nyt.com/images/2020/09/29/us/china-wuhan-coronavirus-maps-promo-1601396059552/china-wuhan-coronavirus-maps-promo-1601396059552-articleLarge-v354.png	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
7	                 https://www.nytimes.com/interactive/2020/us/wisconsin-coronavirus-cases.html	  2021-01-16 20:01:16+00:00	    The New York Times                en-US	  2020-04-01T15:47:54Z	                                      Wisconsin Coronavirus Map and Case Count	                                                                                                                                                        Coronavirus (2019-nCoV), Wisconsin, Disease Rates	                 	          https://static01.nyt.com/images/2020/03/29/us/wisconsin-coronavirus-cases-promo-1585539580772/wisconsin-coronavirus-cases-promo-1585539580772-articleLarge-v118.png	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
8	             https://www.nytimes.com/interactive/2020/us/west-virginia-coronavirus-cases.html	  2021-01-16 20:01:12+00:00	    The New York Times                en-US	  2020-04-01T15:47:51Z	                                  West Virginia Coronavirus Map and Case Count	                                                                                                                                                    Coronavirus (2019-nCoV), West Virginia, Disease Rates	                 	  https://static01.nyt.com/images/2020/03/29/us/west-virginia-coronavirus-cases-promo-1585539566313/west-virginia-coronavirus-cases-promo-1585539566313-articleLarge-v118.png	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
9	                https://www.nytimes.com/interactive/2020/us/washington-coronavirus-cases.html	  2021-01-16 20:01:07+00:00	    The New York Times                en-US	  2020-04-01T15:47:47Z	                                     Washington Coronavirus Map and Case Count	                                                                                                                                               Coronavirus (2019-nCoV), Washington (State), Disease Rates	                 	        https://static01.nyt.com/images/2020/03/29/us/washington-coronavirus-cases-promo-1585539550650/washington-coronavirus-cases-promo-1585539550650-articleLarge-v116.png	  https://www.nytimes.com/sitemaps/new/news.xml.gz	  5bfc0575bbabef04ced9f8e33e05fdcd	  2021-01-16 20:23:13+00:00	  0.6700353622436523	  2021-01-16 20:23:59.469793+00:00
[741 rows x 13 columns]

Video Sitemaps
--------------

>>> wired_video = sitemap_to_df('https://www.wired.com/video/sitemap.xml')
>>> wired_video
                                                                                  loc                                                                                                                                                                                         video_thumbnail_loc                                         video_title                                                                                                                             video_description                                                                                          video_content_loc  video_duration       video_publication_date                                   sitemap                                   etag         sitemap_size_mb                         download_date
0	               https://www.wired.com/video/watch/behind-the-scenes-with-jj-abrams	               http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1389040164/wired_behind-the-scenes-with-jj-abrams.jpg	               Behind the Scenes with J.J. Abrams	       Wired magazine teams up with J.J. Abrams for the May issue. Look in on the creative process with J.J. and the edit and design teams.	                                      http://dp8hsntg6do36.cloudfront.net/5171b42ac2b4c00dd0c1ff9e/low.mp4	           205	  2009-04-20T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
1	        https://www.wired.com/video/watch/trip-hop-pioneer-tricky-sweet-and-naive	        http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1389040238/wired_trip-hop-pioneer-tricky-sweet-and-naive.jpg	         Trip-Hop Pioneer Tricky: Sweet and Naive	                                             Tricky, of Massive Attack fame, shows Wired.com the ropes on becoming a musician and producer.	                                      http://dp8hsntg6do36.cloudfront.net/5171b424c2b4c00dd0c1fe4e/low.mp4	           267	  2009-04-18T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
2	                      https://www.wired.com/video/watch/trash-foils-diamond-heist	                      http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1464291637/wired_trash-foils-diamond-heist.jpg	                        Trash Foils Diamond Heist	                                                                                                                  Trash Foils Diamond Heist	                                      http://dp8hsntg6do36.cloudfront.net/5171b424c2b4c00dd0c1fe3c/low.mp4	           278	  2009-03-12T04:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
3	  https://www.wired.com/video/watch/the-toxic-cloud-emitting-portable-dry-ice-mak	  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1389040172/wired_the-toxic-cloud-emitting-portable-dry-ice-mak.jpg	  The Toxic Cloud-Emitting Portable Dry Ice Maker	                                                                                 The Toxic Cloud-Emitting Portable Dry Ice Maker in action.	                                      http://dp8hsntg6do36.cloudfront.net/5171b424c2b4c00dd0c1fe42/low.mp4	            31	  2009-02-11T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
4	                  https://www.wired.com/video/watch/chef-ferran-adria-of-el-bulli	                  http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1368475899/wired_chef-ferran-adria-of-el-bulli.jpg	                    Chef Ferran Adria of El Bulli	                                                                  Ferran Adria on why the knife is the most essential tool in your kitchen.	                                      http://dp8hsntg6do36.cloudfront.net/5171b42ec2b4c00dd0c20064/low.mp4	            72	  2008-11-25T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
5	                      https://www.wired.com/video/watch/how-to-make-wired-origami	                      http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1389040170/wired_how-to-make-wired-origami.jpg	                        How To Make Wired Origami	                                                                Robert Lang explains how to fold the Wired issue 16.07 origami splash page.	                                      http://dp8hsntg6do36.cloudfront.net/5171b3cbc2b4c00dd0c1e969/low.mp4	           150	  2008-09-23T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
6	                          https://www.wired.com/video/watch/clover-coffee-machine	                          http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1389040152/wired_clover-coffee-machine.jpg	                            Clover Coffee Machine	                                        Wired.com takes a look at the 'Clover', an $11,000 coffee machine hand-built by Stanford engineers.	                                      http://dp8hsntg6do36.cloudfront.net/5171b42ec2b4c00dd0c2005b/low.mp4	           147	  2008-09-23T00:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
7	                      https://www.wired.com/video/watch/original-wargames-trailer	                      http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1464291813/wired_original-wargames-trailer.jpg	                        Original WarGames Trailer	                                                                                                                  Original WarGames Trailer	                                      http://dp8hsntg6do36.cloudfront.net/5171b427c2b4c00dd0c1fee7/low.mp4	           140	  2008-07-21T04:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
8	                              https://www.wired.com/video/watch/rock-band-trailer	                              http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1464292286/wired_rock-band-trailer.jpg	                                Rock Band Trailer	                                                                                                                          Rock Band Trailer	                                      http://dp8hsntg6do36.cloudfront.net/5171b431c2b4c00dd0c20100/low.mp4	            70	  2007-09-14T04:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
9	                           https://www.wired.com/video/watch/arrival-full-trailer	                           http://dwgyu36up6iuz.cloudfront.net/heru80fdn/image/upload/c_fill,d_placeholder_thescene.jpg,fl_progressive,g_face,h_180,q_80,w_320/v1471366897/wired_arrival-full-trailer.jpg	                         ‘Arrival’ — Full Trailer	  Louise Banks (Amy Adams) must learn to communicate with aliens to save humanity in the new film from ‘Sicario’ director Denis Villeneuve.	  http://dp8hsntg6do36.cloudfront.net/57b344f4fd2e614f99000014/1a74100f-bc1b-4279-b677-5efc301785d9low.mp4	           145	  2003-10-22T04:00:00+00:00	  https://www.wired.com/video/sitemap.xml	  W/4eecc23d353856e29d6dae1ce42b43ba	  2.2617597579956055	  2021-01-16 20:43:37.992796+00:00
[2343 rows x 11 columns]

"""
from gzip import GzipFile
import logging
from concurrent import futures
from xml.etree import ElementTree
from urllib.request import urlopen, Request

from advertools import __version__ as version
import pandas as pd

logging.basicConfig(level=logging.INFO)

headers = {'User-Agent': 'advertools-' + version}


def _sitemaps_from_robotstxt(robots_url):
    sitemaps = []
    robots_page = urlopen(Request(robots_url, headers=headers))
    for line in robots_page.readlines():
        line_split = [s.strip() for s in line.decode().split(':', maxsplit=1)]
        if line_split[0].lower() == 'sitemap':
            sitemaps.append(line_split[1])
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


def sitemap_to_df(sitemap_url, max_workers=8, recursive=True):
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
    :return sitemap_df: A pandas DataFrame containing all URLs, as well as
                        other tags if available (``lastmod``, ``changefreq``,
                        ``priority``, or others found in news, video, or image
                        sitemaps).
    """
    if sitemap_url.endswith('robots.txt'):
        return pd.concat([sitemap_to_df(sitemap, recursive=recursive)
                          for sitemap in _sitemaps_from_robotstxt(sitemap_url)],
                         ignore_index=True)
    if sitemap_url.endswith('xml.gz'):
        xml_text = urlopen(Request(sitemap_url,
                                   headers={'Accept-Encoding': 'gzip',
                                            'User-Agent': 'advertools-' +
                                                          version}))
        resp_headers = xml_text.getheaders()
        xml_text = GzipFile(fileobj=xml_text)
    else:
        xml_text = urlopen(Request(sitemap_url, headers=headers))
        resp_headers = xml_text.getheaders()
    xml_string = xml_text.read()
    root = ElementTree.fromstring(xml_string)

    sitemap_df = pd.DataFrame()

    if (root.tag.split('}')[-1] == 'sitemapindex') and recursive:
        multi_sitemap_df = pd.DataFrame()
        sitemap_url_list = []
        for elem in root:
            for el in elem:
                if 'loc' in el.tag:
                    if el.text == sitemap_url:
                        error_df = pd.DataFrame({
                            'sitemap': [sitemap_url],
                            'errors': ['WARNING: Sitemap contains a link to itself']
                        })
                        multi_sitemap_df = multi_sitemap_df.append(error_df,
                                                                   ignore_index=True)
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
                    multi_sitemap_df = multi_sitemap_df.append(future.result(),
                                                               ignore_index=True)
                except Exception as e:
                    error_df = pd.DataFrame(dict(errors=str(e)),
                                            index=range(1))
                    future_str = hex(id(future))
                    hexes = [hex(id(f)) for f in to_do]
                    index = hexes.index(future_str)
                    error_df['sitemap'] = sitemap_url_list[index]
                    logging.warning(msg=str(e) + ' ' + sitemap_url_list[index])
                    multi_sitemap_df = multi_sitemap_df.append(error_df,
                                                               ignore_index=True)
        return multi_sitemap_df

    else:
        logging.info(msg='Getting ' + sitemap_url)
        elem_df = _parse_sitemap(root)
        sitemap_df = sitemap_df.append(elem_df, ignore_index=True)
        sitemap_df['sitemap'] = [sitemap_url] if sitemap_df.empty else sitemap_url
    if 'lastmod' in sitemap_df:
        try:
            sitemap_df['lastmod'] = pd.to_datetime(sitemap_df['lastmod'], utc=True)
        except Exception as e:
            pass
    if 'priority' in sitemap_df:
        try:
            sitemap_df['priority'] = sitemap_df['priority'].astype(float)
        except Exception as e:
            pass
    etag_lastmod = {header.lower().replace('-', '_'): val.replace('"', '')
                    for header, val in resp_headers
                    if header.lower() in ['etag', 'last-modified']}
    sitemap_df = sitemap_df.assign(**etag_lastmod)
    if 'last_modified' in sitemap_df:
        sitemap_df['sitemap_last_modified'] = pd.to_datetime(sitemap_df['last_modified'])
        del sitemap_df['last_modified']
    sitemap_df['sitemap_size_mb'] = len(xml_string) / 1024 / 1024
    sitemap_df['download_date'] = pd.Timestamp.now(tz='UTC')
    return sitemap_df
