"""
.. _crawl_strategies:

🕷 SEO Crawling & Scraping: Strategies & Recipes
================================================

Once you have mastered the basics of using the :ref:`crawl <crawl>` function,
you probably want to achieve more with better customization and control.

These are some code strategies that might be useful to customize how you run
your crawls.

Most of these options can be set using the ``custom_settings`` parameter that
the function takes. This can be set by using a dictionary, where the keys
indicate the option you want to set, and the values specify how you want to set
them.

How to crawl a list of pages, and those pages only (list mode)?
***************************************************************

Simply provide that list as the first argument, for the ``url_list`` parameter,
and make sure that ``follow_links=False``, which is the default. This simply
crawls the given pages, and stops when done.

.. code-block:: python

    >>> import advertools as adv
    >>> url_list = ['https://example.com/page_1',
    ...             'https://example.com/page_2',
    ...             'https://example.com/page_3',
    ...             'https://example.com/page_4']

    >>> adv.crawl(url_list,
    ...           output_file='example_crawl_1.jl',
    ...           follow_links=False)



How can I crawl a website including its sub-domains?
****************************************************

The :ref:`crawl <crawl>` function takes an optional ``allowed_domains``
parameter. If not provided, it defaults to the domains of the URLs in
``url_list``. When the crawler goes through the pages of `example.com`, it
follows links to discover pages. If it finds pages on `help.exmaple.com` it
won't crawl them (it's a different domain). The solution, therefore, is to
provide a list of domains to the ``allowed_domains`` parameter. Make sure you
also include the original domain, in this case `example.com`.

.. code-block:: python

    >>> adv.crawl('https://example.com',
    ...           'example_crawl_1.jl',
    ...           follow_links=True
    ...           allowed_domains=['help.example.com', 'example.com', 'community.example.com'])

How can I save a copy of the logs of my crawl for auditing them later?
**********************************************************************

It's usually good to keep a copy of the logs of all your crawls to check for
errors, exceptions, stats, etc.
Pass a path of the file where you want the logs to be saved, in a dictionary to
the ``cutom_settings`` parameter.
A good practice for consistency is to give the same name to the ``output_file``
and log file (with a different extension) for easier retreival. For example:

| ``output_file``: 'website_name_crawl_1.jl'
| ``LOG_FILE``: 'website_name_crawl_1.log' (.txt can also work)
| ``output_file``: 'website_name_crawl_2.jl'
| ``LOG_FILE``: 'website_name_crawl_2.log'

.. code-block:: python

    >>> adv.crawl('https://example.com', 'example_crawl_1.jl',
    ...           custom_settings={'LOG_FILE': 'example_crawl_1.log'})

How can I automatically stop my crawl based on a certain condition?
*******************************************************************

There are a few conditions that you can use to trigger the crawl to stop, and
they mostly have descriptive names:

    * ``CLOSESPIDER_ERRORCOUNT``: You don't want to wait three hours for a
      crawl to finish, only to discover that you had errors all over the place.
      Set a certain number of errors to trigger the crawler to stop, so you can
      investigate the issue.

    * ``CLOSESPIDER_ITEMCOUNT``: Anything scraped from a page is an "item", h1,
      title , meta_desc, etc. Set the crawler to stop after getting a certain
      number of items if you want that.

    * ``CLOSESPIDER_PAGECOUNT``: Stop the crawler after a certain number of
      pages have been crawled. This is useful as an exploratory technique,
      especially with very large websites. It might be good to crawl a few
      thousand pages, get an idea on its structure, and then run a full crawl
      with those insights in mind.

    * ``CLOSESPIDER_TIMEOUT``: Stop the crawler after a certain number of
      seconds.

.. code-block:: python

    >>> adv.crawl('https://example.com', 'example_crawl_1.jl',
    ...           custom_settings={'CLOSESPIDER_PAGECOUNT': 500})

How can I (dis)obey robots.txt rules?
*************************************

The crawler obeys robots.txt rules by default. Sometimes you might want to
check the results of crawls without doing that. You can set the
``ROBOTSTXT_OBEY`` setting under ``custom_settings``:

.. code-block:: python

    >>> adv.crawl('https://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'ROBOTSTXT_OBEY': False})


How do I set my User-agent while crawling?
******************************************

Set this parameter under `custom_settings` dictionary under the key
``USER_AGENT``. The default User-agent can be found by running
`adv.spider.user_agent`

.. code-block:: python

    >>> adv.spider.user_agent # to get the current User-agent
    >>> adv.crawl('http://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'USER_AGENT': 'YOUR_USER_AGENT'})


How can I control the number of concurrent requests while crawling?
*******************************************************************
Some servers are set for high sensitivity to automated and/or concurrent
requests, that you can quickly be blocked/banned. You also want to be polite
and not kill those servers, don't you?

There are several ways to set that under the ``custom_settings`` parameter.
The available keys are the following:

| ``CONCURRENT_ITEMS``: default 100
| ``CONCURRENT_REQUESTS`` : default 16
| ``CONCURRENT_REQUESTS_PER_DOMAIN``: default 8
| ``CONCURRENT_REQUESTS_PER_IP``: default 0

.. code-block:: python

    >>> adv.crawl('https://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'CONCURRENT_REQUESTS_PER_DOMAIN': 1})

How can I slow down the crawling so I don't hit the websites' servers too hard?
*******************************************************************************

Use the ``DOWNLOAD_DELAY`` setting and set the interval to be waited before
downloading consecutive pages from the same website (in seconds).

.. code-block:: python

    >>> adv.crawl('https://example.com', 'example_crawl_1.jl',
    ...           custom_settings={'DOWNLOAD_DELAY': 3}) # wait 3 seconds between pages

How can I set multiple settings to the same crawl job?
******************************************************
Simply add multiple settings to the ``custom_settings`` parameter.

.. code-block:: python

    >>> adv.crawl('http://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'CLOSESPIDER_PAGECOUNT': 400,
    ...                            'CONCURRENT_ITEMS': 75,
    ...                            'LOG_FILE': 'output_file.log'})

I want to crawl a list of pages, follow links from those pages, but only to a certain specified depth
*****************************************************************************************************

Set the ``DEPTH_LIMIT`` setting in the ``custom_settings`` parameter. A setting
of 1 would follow links one level after the provided URLs in ``url_list``

    >>> adv.crawl(
    ...     "http://example.com", "example_crawl_1.jl", custom_settings={"DEPTH_LIMIT": 2}
    ... )  # follow links two levels from the initial URLs, then stop

How do I pause/resume crawling, while making sure I don't crawl the same page twice?
************************************************************************************

There are several reasons why you might want to do this:

* You want to mainly crawl the updates to the site (you already crawled the site).
* The site is very big, and can't be crawled quickly.
* You are not in a hurry, and you also don't want to hit the servers hard, so
  you run your crawl across days for example.
* As an emergency measure (connection lost, battery died, etc.) you can start
  where you left off

Handling this is extremely simple, and all you have to do is simply provide a
path to a new folder. Make sure it is new and empty, and make sure to only use
it for the same crawl job reruns. That's all you have to worry about. The
``JOBDIR`` setting handles this.

.. code-block:: python

    >>> adv.crawl('http://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'JOBDIR': '/Path/to/en/empty/folder'})

The first time you run the above code and then stop it. Stopping can happen by
accident (lost connection, closed computer, etc.), manually (you hit ctrl+C) or
you used a custom setting option to stop the crawl after a certain number of
pages, seconds, etc.

The second time you want to run this, you simply run the exact same command
again. If you check the folder that was created you can see a few files that
manage the process. You don't need to worry about any of it. But make sure that
folder doesn't get changed manually, rerun the same command as many times as
you need, and the crawler should handle de-duplication for you.

How do I use a proxy while crawling?
************************************

This requires the following simple steps:

* Install the 3rd party package `scrapy-rotating-proxies <https://github.com/TeamHG-Memex/scrapy-rotating-proxies>`_. This package handles
  the proxy rotation for you, in addition to retries, so you don't need to
  worry about those details.
* Get a list of proxies and save in a text file, one proxy per line
* Set a few ``custom_settings`` in the crawl function
  (``DOWNLOADER_MIDDLEWARES`` and ``ROTATING_PROXY_LIST_PATH``)

.. code-block:: bash

    $ pip install scrapy-rotating-proxies

Save a list of proxies in a text file with the template:

https://username:password@IPADDRESS:PORT

proxies.txt example file (randome values):

https://user123:password123@12.34.56.78:1111
https://user123:password123@12.34.56.78:1112
https://user123:password123@12.34.56.78:1113
https://user123:password123@12.34.56.78:1114


Then, you need to set a few ``custom_settings`` in the crawl function:


.. code-block:: python

    adv.crawl(
        "https://example.com",
        "output_file.jl",
        follow_links=True,
        custom_settings={
            "DOWNLOADER_MIDDLEWARES": {
                "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
                "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
            },
            "ROTATING_PROXY_LIST_PATH": "proxies.txt",
        },
    )

You can then read the output file normally and see that the proxies are being
used:


.. code-block:: python

    crawldf = pd.read_json("output_file.jl", lines=True)
    crawldf.filter(regex="proxy").head()


====  ============================  =================  =====================================  ===================
  ..  proxy                           _rotating_proxy  request_headers_proxy-authorization      proxy_retry_times
====  ============================  =================  =====================================  ===================
   0  https://123.456.789.101:8893                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   1  https://123.456.789.101:8894                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   2  https://123.456.789.101:8895                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   3  https://123.456.789.101:8896                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   4  https://123.456.789.101:8897                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
====  ============================  =================  =====================================  ===================

How can I change the default request headers?
*********************************************

This is a very common use case, and it is very easy to do. Simply add the
``DEFAULT_REQUEST_HEADERS`` setting as a dictionary to the ``custom_settings``
parameter:

.. code-block:: python

    adv.crawl(
        url_list="https://example.com",
        output_file="output.jl",
        custom_settings={
            "DEFAULT_REQUEST_HEADERS": {
                "Accept-Language": "es",
                "Accept-Encoding": "gzip, deflate",
            }
        },
    )

You can easily check for the actual request headers that were used while
crawling. In the crawl DataFrame, simply use the regex pattern
``request_headers_``:

.. code-block:: python

    crawldf = pd.read_json("output.jl", lines=True)
    crawldf.filter(regex="request_headers_")

====  =================================  =================================  ============================
  ..  request_headers_accept-language    request_headers_accept-encoding    request_headers_user-agent
====  =================================  =================================  ============================
   0  es                                 gzip, deflate                      advertools/0.13.2
====  =================================  =================================  ============================

XPath expressions for custom extraction
***************************************

The following are some expressions you might find useful in your crawling,
whether you use ``advertools`` or not. The first column indicates whether or
not the respective expression is used by default by the ``advertools`` crawler.

====================  ===================  =================================================================  ===============================================================================================================
Used by advertools    Suggested Name       XPath Expression                                                   What it does
====================  ===================  =================================================================  ===============================================================================================================
True                  title                //title/text()                                                     Extract the text of title tags
True                  meta_desc            //meta[@name='description']/@content                               Extract the content attribute of the meta tag which has the name 'description'
True                  viewport             //meta[@name='viewport']/@content                                  Extract the content attribute of the meta tag which has the name 'viewport
True                  charset              //meta[@charset]/@charset                                          Get the meta tag that has the attribute 'charset', extract the charset attribute
True                  h1                   //h1/text()                                                        Get the h1 tags, extract their text
True                  h2                   //h2/text()                                                        Get the h2 tags, extract their text
True                  h3                   //h3/text()                                                        Get the h3 tags, extract their text
True                  h4                   //h4/text()                                                        Get the h4 tags, extract their text
True                  h5                   //h5/text()                                                        Get the h5 tags, extract their text
True                  h6                   //h6/text()                                                        Get the h6 tags, extract their text
True                  canonical            //link[@rel='canonical']/@href                                     Get the link elements with the rel attribute 'canonical', extract their href attributes
True                  alt_href             //link[@rel='alternate']/@href                                     Get the link elements with the rel attribute 'alternate', extract their href attributes
True                  alt_hreflang         //link[@rel='alternate']/@hreflang                                 Get the link elements with the rel attribute 'alternate', extract their hreflang attributes
True                  og_props             //meta[starts-with(@property, 'og:')]/@property                    Extract all properties of meta tags whos property attribute starts with 'og:' (OpenGraph)
True                  og_content           //meta[starts-with(@property, 'og:')]/@content                     Extract the content of meta tags whos property attribute starts with 'og:' (OpenGraph)
True                  twtr_names           //meta[starts-with(@name, 'twitter:')]/@name                       Get meta tags who's name starts with 'twitter:' and extract their name attribute
True                  twtr_content         //meta[starts-with(@name, 'twitter:')]/@content                    Get meta tags who's name starts with 'twitter:' and extract their content attribute
False                 iframe_src           //iframe/@src                                                      Get the iframes, and extract their src attribute
False                 gtm_script           //script[contains(@src, 'googletagmanager.com/gtm.js?id=')]/@src   Get the script where the src attribute contains googletagmanager.com/gtm.js?id= and extract its src attribute
False                 gtm_noscript         //iframe[contains(@src, 'googletagmanager.com/ns.html?id=')]/@src  Get the iframes where the src attribute contains googletagmanager.com/ns.html?id= and extract the src attribute
False                 link_rel_rel         //link[@rel]/@rel                                                  Get all the link elements that have a rel attribute, extract the rel attributes
False                 link_rel_href        //link[@rel]/@href                                                 Get all the link elements that have a rel attribute, extract the href attributes
False                 link_rel_stylesheet  //link[@rel='stylesheet']/@href                                    Get all the link elements that have a stylesheet attribute, extract their href attribute
False                 css_links            //link[contains(@href, '.css')]/@href                              Get the link elements where the href attribute contains .css, extract their href attribute
True                  nav_links_text       //nav//a/text()                                                    From the nav element, extract the anchor text of links
True                  nav_links_href       //nav//a/@href                                                     From the nav element, extract all the links
True                  header_links_text    //header//a/text()                                                 From the header, extract the anchor text of links
True                  header_links_href    //header//a/@href                                                  From the header, extract all the links
True                  footer_links_text    //footer//a/text()                                                 From the footer, extract the anchor text of links
True                  footer_links_href    //footer//a/@href                                                  From the footer, extract all the links
False                 js_script_src        //script[@type='text/javascript']/@src                             From script tags where the type is text/javascript, extract the src of the script(s)
False                 js_script_text       //script[@type='text/javascript']/text()                           From script tags where the type is text/javascript, extract the text of the script(s)
False                 script_src           //script//@src                                                     Get the src attribute of any <script> tag
False                 canonical_parent     name(//link[@rel='canonical']/..)                                  Get the name of the parent of the link element that has a rel attribute 'canonical'
====================  ===================  =================================================================  ===============================================================================================================

User-agent strings for use in crawling
**************************************

A simple collection of some of the popular user-agents in case you need to test while
crawling:

========================================================  =========================================================================================================================================================================
Name                                                      User agent string
========================================================  =========================================================================================================================================================================
Amazon 4K Fire TV                                         Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36
Amazon AFTWMST22                                          Mozilla/5.0 (Linux; Android 9; AFTWMST22 Build/PS7233; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36
Amazon Kindle 3                                           Mozilla/5.0 (Linux; U; en-US) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)
Amazon Kindle 4                                           Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+
Amazon Kindle Fire HDX 7                                  Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36
Apple TV 4th Gen                                          AppleTV5,3/9.1.1
Apple TV 5th Gen 4K                                       AppleTV6,2/11.1
Apple TV 6th Gen 4K                                       AppleTV11,1/11.1
Apple iPhone 11                                           Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1
Apple iPhone 12                                           Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1
Apple iPhone 13 Pro Max                                   Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1
Apple iPhone 6                                            Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3
Apple iPhone 7                                            Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1
Apple iPhone 7 Plus                                       Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1
Apple iPhone 8                                            Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1
Apple iPhone 8 Plus                                       Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1
Apple iPhone SE (3rd generation)                          Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1
Apple iPhone X                                            Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1
Apple iPhone XR (Safari)                                  Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1
Apple iPhone XS (Chrome)                                  Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1
Apple iPhone XS Max (Firefox)                             Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15
Bing bot                                                  Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
Chrome OS-based laptop using Chrome browser (Chromebook)  Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36
Chromecast                                                Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36
Google ADT-2                                              Dalvik/2.1.0 (Linux; U; Android 9; ADT-2 Build/PTT5.181126.002)
Google Nexus Player                                       Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)
Google Pixel                                              Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36
Google Pixel 2                                            Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170811.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36
Google Pixel 3                                            Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36
Google Pixel 4                                            Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36
Google Pixel 5                                            Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36
Google Pixel 6                                            Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36
Google Pixel C                                            Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36
Google bot                                                Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
HTC Desire 21 Pro 5G                                      Mozilla/5.0 (Linux; Android 10; HTC Desire 21 pro 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36
HTC One M9                                                Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3
HTC One X10                                               Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36
HTC U20 5G                                                Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36
LG G Pad 7.0                                              Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36
Lenovo Yoga Tab 11                                        Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
Linux-based PC using a Firefox browser                    Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1
Mac OS X-based computer using a Safari browser            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9
Microsoft Lumia 550                                       Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536
Microsoft Lumia 650                                       Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254
Microsoft Lumia 950                                       Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058
Minix NEO X5                                              Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30
Nexus 6P                                                  Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36
Nintendo 3DS                                              Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU
Nintendo Switch                                           Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, like Gecko) NF/4.0.0.5.10 NintendoBrowser/5.1.0.13343
Nintendo Wii U                                            Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US
Nvidia Shield Tablet K1                                   Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36
Playstation 4                                             Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)
Playstation 5                                             Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15
Playstation Vita                                          Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2
Roku Ultra                                                Roku4640X/DVP-7.70 (297.70E04154A)
Samsung Galaxy S10                                        Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36
Samsung Galaxy S20                                        Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36
Samsung Galaxy S21                                        Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36
Samsung Galaxy S22                                        Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36
Samsung Galaxy S6                                         Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36
Samsung Galaxy S6 Edge Plus                               Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36
Samsung Galaxy S7                                         Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36
Samsung Galaxy S7 Edge                                    Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36
Samsung Galaxy S8                                         Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36
Samsung Galaxy S9                                         Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36
Samsung Galaxy Tab A                                      Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36
Samsung Galaxy Tab S3                                     Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36
Samsung Galaxy Tab S8 Ultra                               Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36
Sony Xperia 1                                             Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36
Sony Xperia XZ                                            Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36
Sony Xperia Z4 Tablet                                     Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36
Sony Xperia Z5                                            Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36
Windows 10-based PC using Edge browser                    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246
Windows 7-based PC using a Chrome browser                 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
Xbox One                                                  Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586
Xbox One S                                                Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393
Xbox Series X                                             Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox Series X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/20.02
Yahoo! bot                                                Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)
Googlebot Smartphone                                      Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
Googlebot Desktop                                         Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36
Googlebot-Image                                           Googlebot-Image/1.0
Googlebot-News                                            Googlebot-News
Googlebot-Video                                           Googlebot-Video/1.0
Storebot-Google Desktop                                   Mozilla/5.0 (X11; Linux x86_64; Storebot-Google/1.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Safari/537.36
Storebot-Google Smartphone                                Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012; Storebot-Google/1.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36
Google-InspectionTool Mobile                              Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Google-InspectionTool/1.0;)
Google-InspectionTool Desktop                             Mozilla/5.0 (compatible; Google-InspectionTool/1.0;)
GoogleOther                                               Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; GoogleOther)
GoogleOther-Image                                         GoogleOther-Image/1.0
GoogleOther-Video                                         GoogleOther-Video/1.0
APIs-Google                                               APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)
AdsBot-Google-Mobile                                      Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)
AdsBot-Google                                             AdsBot-Google (+http://www.google.com/adsbot.html)
Mediapartners-Google                                      Mediapartners-Google
Google-Safety                                             Google-Safety
FeedFetcher-Google                                        FeedFetcher-Google; (+http://www.google.com/feedfetcher.html)
Google Publisher Center                                   GoogleProducer; (+http://goo.gl/7y4SX)
Google Site Verifier                                      Mozilla/5.0 (compatible; Google-Site-Verification/1.0)
========================================================  =========================================================================================================================================================================

"""  # noqa: E501
