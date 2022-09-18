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

    >>> adv.crawl('http://example.com',
    ...           'example_crawl_1.jl',
    ...           custom_settings={'DEPTH_LIMIT': 2}) # follow links two levels from the initial URLs, then stop

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
        'https://example.com', 'output_file.jl', follow_links=True,

        custom_settings={
            'DOWNLOADER_MIDDLEWARES': {
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620
            },
            'ROTATING_PROXY_LIST_PATH': 'proxies.txt',
        }
    )

You can then read the output file normally and see that the proxies are being
used:


.. code-block:: python

    crawldf = pd.read_json('output_file.jl', lines=True)
    crawldf.filter(regex='proxy').head()


====  ============================  =================  =====================================  ===================
  ..  proxy                           _rotating_proxy  request_headers_proxy-authorization      proxy_retry_times
====  ============================  =================  =====================================  ===================
   0  https://123.456.789.101:8893                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   1  https://123.456.789.101:8894                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   2  https://123.456.789.101:8895                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   3  https://123.456.789.101:8896                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
   4  https://123.456.789.101:8897                  1  Basic b3VzY214dHg6ODlld29rMGRsdfgt                     nan
====  ============================  =================  =====================================  ===================


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

"""
