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
downloading consecutive page from the same website (in seconds).

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

"""