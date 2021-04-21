"""
.. _robotstxt:

🤖 Analyze and Test robots.txt Files on a Large Scale
=====================================================

Even though they are tiny in size, robots.txt files contain potent instructions
that can block major sections of your site, which is what they are supposed to
do. Only sometimes you might make the mistake of blocking the wrong section.

So it is very important to check if certain pages (or groups of pages) are
blocked for a certain user-agent by a certain robots.txt file. Ideally, you
would want to run the same check for all possible user-agents. Even more
ideally, you want to be able to run the check for a large number of pages with
every possible combination with user-agents!

To get the robots.txt file into an easily readable format, you can use the
:func:`robotstxt_to_df` function to get it in a DataFrame.

>>> robotstxt_to_df('https://www.amazon.com/robots.txt')
      directive    content                                        etag                                robotstxt_last_modified    robotstxt_url                      download_date
   0  User-agent   *                                              "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
   1  Disallow     /exec/obidos/account-access-login              "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
   2  Disallow     /exec/obidos/change-style                      "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
   3  Disallow     /exec/obidos/flex-sign-in                      "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
   4  Disallow     /exec/obidos/handle-buy-box                    "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
 ...    ...                 ...                                                 ...                              ...                           ...                                 ...
 138  Disallow     /gp/help/customer/express/c2c/                 "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
 139  Disallow     /slp/*/b$                                      "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
 140  Disallow     /hz/contact-us/ajax/initiate-trusted-contact/  "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
 141  User-agent   EtaoSpider                                     "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00
 142  Disallow     /                                              "8e5277c97035c645b89ceb97cdb8c619"  2020-10-09 22:39:49+00:00  https://www.amazon.com/robots.txt  2021-04-20 17:18:42.155107+00:00


The returned DataFrame contains columns for directives, their content, the URL
of the robots.txt file, as well as the date it was downloaded.

*  `directive`: The main commands. Allow, Disallow, Sitemap, Crawl-delay,
   User-agent, and so on.
*  `content`: The details of each of the directives
*  `robotstxt_last_modified`: The date when the robots.txt file was last
   modified, if provided.
*  `etag`: The entity tag of the response header, if provided.
*  `robotstxt_url`: The URL of the robots.txt file.
*  `download_date`: The date and time when the file was downloaded.

Alternatively, you can provide a list of robots URLs if you want to download
them all in one go. This might be interesting if:

* You are analyzing an industry and want to keep an eye on many different
  websites.
* You are analyzing a website with many sub-domains, and want to get all the
  robots files together.
* You are trying to understand a company that has many websites under
  different domains and sub-domains.

In this case you simply provide a list of URLs instead of a single one.

An optional parameter ``output_file`` is also available in case you are
requesting hundreds of files. The supported format is `.jl`. This saves the
downloaded files by appending them to the file, so it is also useful if you
think the process is going to take long and might loose your connection for
example.

>>> robotstxt_to_df(['https://example.com/robots.txt',
...                  'https://community.example.com/robots.txt',
...                  'https://shop.example.com/robots.txt'],
...                   output_file='example_robots.jl')

As for testing, the :func:`robotstxt_test` function runs a test for a given
robots.txt file, checking which of the provided user-agents can fetch which of
the provided URLs, paths, or patterns.

>>> robotstxt_test('https://www.example.com/robots.txt',
...                useragents=['Googlebot', 'baiduspider', 'Bingbot']
...                urls=['/', '/hello', '/some-page.html']])

As a result, you get a DataFrame with a row for each combination of
(user-agent, URL) indicating whether or not that particular user-agent can
fetch the given URL.

Some reasons why you might want to do that:

* SEO Audits: Especially for large websites with many URL patterns, and many
  rules for different user-agents.
* Developer or site owner about to make large changes
* Interest in strategies of certain companies

User-agents
-----------

In reality there are only two groups of user-agents that you need to worry
about:

* User-agents listed in the robots.txt file: For each one of those you need to
  check whether or not they are blocked from fetching a certain URL
  (or pattern).
* ``*`` all other user-agents: The ``*`` includes all other user-agents, so
  checking the rules that apply to it should take care of the rest.

robots.txt Testing Approach
---------------------------

1. Get the robots.txt file that you are interested in
2. Extract the user-agents from it
3. Specify the URLs you are interested in testing
4. Run the :func:`robotstxt_test` function

>>> fb_robots = robotstxt_to_df('https://www.facebook.com/robots.txt')
      directive    content                                                              robotstxt_url                        download_date
   0  comment      Notice: Collection of data on Facebook through automated means is    https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
   1  comment      prohibited unless you have express written permission from Facebook  https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
   2  comment      and may only be conducted for the limited purpose contained in said  https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
   3  comment      permission.                                                          https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
   4  comment      See: http://www.facebook.com/apps/site_scraping_tos_terms.php        https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
 ...    ...                                ...                                                         ...                                 ...
 480  Allow        /ajax/bootloader-endpoint/                                           https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
 481  Allow        /ajax/pagelet/generic.php/PagePostsSectionPagelet                    https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
 482  Allow        /safetycheck/                                                        https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
 483  User-agent   *                                                                    https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
 484  Disallow     /                                                                    https://www.facebook.com/robots.txt  2021-04-20 17:30:46.571533+00:00
[484 rows x 4 columns]

Now that we have downloaded the file, we can easily extract the list of
user-agents that it contains.

>>> fb_useragents = (fb_robots
...                  [fb_robots['directive']=='User-agent']
...                  ['content'].drop_duplicates()
...                  .tolist())
>>> fb_useragents
['Applebot',
 'baiduspider',
 'Bingbot',
 'Discordbot',
 'facebookexternalhit',
 'Googlebot',
 'Googlebot-Image',
 'ia_archiver',
 'LinkedInBot',
 'msnbot',
 'Naverbot',
 'Pinterestbot',
 'seznambot',
 'Slurp',
 'teoma',
 'TelegramBot',
 'Twitterbot',
 'Yandex',
 'Yeti',
 '*']


Quite a long list!

As a small and quick test, I'm interested in checking the home page, a random
profile page (/bbc), groups and hashtags pages.

>>> urls_to_test = ['/', '/bbc', '/groups', '/hashtag/']
>>> fb_test = robotstxt_test('https://www.facebook.com/robots.txt',
...                          fb_useragents, urls_to_test)
>>> fb_test
                          robotstxt_url user_agent   url_path  can_fetch
0   https://www.facebook.com/robots.txt          *       /bbc      False
1   https://www.facebook.com/robots.txt          *    /groups      False
2   https://www.facebook.com/robots.txt          *          /      False
3   https://www.facebook.com/robots.txt          *  /hashtag/      False
4   https://www.facebook.com/robots.txt   Applebot          /       True
..                                  ...        ...        ...        ...
75  https://www.facebook.com/robots.txt  seznambot    /groups       True
76  https://www.facebook.com/robots.txt      teoma          /       True
77  https://www.facebook.com/robots.txt      teoma  /hashtag/      False
78  https://www.facebook.com/robots.txt      teoma       /bbc       True
79  https://www.facebook.com/robots.txt      teoma    /groups       True
[80 rows x 4 columns]


For twenty user-agents and four URLs each, we received a total of eighty test
results. You can immediately see that all user-agents not listed (denoted by
`*` are not allowed to fetch any of the provided URLs).

Let's see who is and who is not allowed to fetch the home page.

>>> fb_test.query('url_path== "/"')
                          robotstxt_url           user_agent  url_path  can_fetch
2   https://www.facebook.com/robots.txt                    *         /      False
4   https://www.facebook.com/robots.txt             Applebot         /       True
9   https://www.facebook.com/robots.txt              Bingbot         /       True
14  https://www.facebook.com/robots.txt           Discordbot         /      False
18  https://www.facebook.com/robots.txt            Googlebot         /       True
21  https://www.facebook.com/robots.txt      Googlebot-Image         /       True
26  https://www.facebook.com/robots.txt          LinkedInBot         /      False
30  https://www.facebook.com/robots.txt             Naverbot         /       True
35  https://www.facebook.com/robots.txt         Pinterestbot         /      False
39  https://www.facebook.com/robots.txt                Slurp         /       True
43  https://www.facebook.com/robots.txt          TelegramBot         /      False
47  https://www.facebook.com/robots.txt           Twitterbot         /       True
48  https://www.facebook.com/robots.txt               Yandex         /       True
55  https://www.facebook.com/robots.txt                 Yeti         /       True
57  https://www.facebook.com/robots.txt          baiduspider         /       True
60  https://www.facebook.com/robots.txt  facebookexternalhit         /      False
64  https://www.facebook.com/robots.txt          ia_archiver         /      False
68  https://www.facebook.com/robots.txt               msnbot         /       True
74  https://www.facebook.com/robots.txt            seznambot         /       True
76  https://www.facebook.com/robots.txt                teoma         /       True

I'll leave it to you to figure out why LinkedIn and Pinterest are not allowed
to crawl the home page but Google and Apple are, because I have no clue!
"""
__all__ = ['robotstxt_to_df', 'robotstxt_test']

import gzip
import logging
from concurrent import futures
from urllib.request import Request, urlopen
from itertools import product

from protego import Protego
import pandas as pd

from advertools import __version__ as version

headers = {'User-Agent': 'advertools-' + version}

gzip_start_bytes = b'\x1f\x8b'

logging.basicConfig(level=logging.INFO)


def robotstxt_to_df(robotstxt_url, output_file=None):
    """Download the contents of ``robotstxt_url`` into a DataFrame

    You can also use it to download multiple robots files by passing a list of
    URLs.

    >>> robotstxt_to_df('https://www.twitter.com/robots.txt')
         directive content   	                 robotstxt_url	                   download_date
    0	User-agent	     *	https://www.twitter.com/robots.txt	2020-09-27 21:57:23.702814+00:00
    1	  Disallow	     /	https://www.twitter.com/robots.txt	2020-09-27 21:57:23.702814+00:00

    >>> robotstxt_to_df(['https://www.google.com/robots.txt',
    ...                  'https://www.twitter.com/robots.txt'])
           directive	                             content	    robotstxt_last_modified	                       robotstxt_url	                     download_date
    0	  User-agent	                                   *	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    1	    Disallow	                             /search	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    2	       Allow	                       /search/about	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    3	       Allow	                      /search/static	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    4	       Allow	              /search/howsearchworks	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    283	  User-agent	                 facebookexternalhit	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    284	       Allow	                             /imgres	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    285	     Sitemap	  https://www.google.com/sitemap.xml	  2021-01-11 21:00:00+00:00	   https://www.google.com/robots.txt	  2021-01-16 14:08:50.087985+00:00
    286	  User-agent	                                   *	                        NaT	  https://www.twitter.com/robots.txt	  2021-01-16 14:08:50.468588+00:00
    287	    Disallow	                                   /	                        NaT	  https://www.twitter.com/robots.txt	  2021-01-16 14:08:50.468588+00:00

    For research purposes and if you want to download more than ~500 files, you
    might want to use ``output_file`` to save results as they are downloaded.
    The file extension should be ".jl", and robots files are appended to that
    file as soon as they are downloaded, in case you lose your connection, or
    maybe your patience!

    >>> robotstxt_to_df(['https://example.com/robots.txt',
    ...                  'https://example.com/robots.txt',
    ...                  'https://example.com/robots.txt'],
    ...                 output_file='robots_output_file.jl')

    To open the file as a DataFrame:

    >>> import pandas as pd
    >>> robotsfiles_df = pd.read_json('robots_output_file.jl', lines=True)

    :param url robotstxt_url: One or more URLs of the robots.txt file(s)
    :param str output_file: Optional file path to save the robots.txt files,
                            mainly useful for downloading > 500 files. The
                            files are appended as soon as they are downloaded.
                            Only ".jl" extensions are supported.

    :returns DataFrame robotstxt_df: A DataFrame containing directives, their
                                     content, the URL and time of download
    """
    if output_file is not None and (not output_file.endswith('.jl')):
        raise ValueError('Please specify a file with a `.jl` extension.')
    if isinstance(robotstxt_url, (list, tuple, set, pd.Series)):
        return _robots_multi(robotstxt_url, output_file)
    else:
        try:
            logging.info(msg='Getting: ' + robotstxt_url)
            robots_open = urlopen(Request(robotstxt_url, headers=headers),
                                  timeout=45)
            robots_read = robots_open.read()
            if robots_read.startswith(gzip_start_bytes):
                data = gzip.decompress(robots_read)
                robots_text = data.decode('utf-8-sig').splitlines()
            else:
                robots_text = robots_read.decode('utf-8-sig').splitlines()
            lines = []
            for line in robots_text:
                if line.strip():
                    if line.strip().startswith('#'):
                        lines.append(['comment',
                                      (line.replace('#', '').strip())])
                    else:
                        split = line.split(':', maxsplit=1)
                        lines.append([split[0].strip(), split[1].strip()])
            df = pd.DataFrame(lines, columns=['directive', 'content'])
            try:
                etag_lastmod = {header.lower().replace('-', '_'): val
                                for header, val in robots_open.getheaders()
                                if header.lower() in ['etag', 'last-modified']}
                df = df.assign(**etag_lastmod)
                if 'last_modified' in df:
                    df['robotstxt_last_modified'] = pd.to_datetime(df['last_modified'])
                    del df['last_modified']
            except AttributeError:
                pass
        except Exception as e:
            df = pd.DataFrame({'errors': [str(e)]})
        try:
            df['robotstxt_url'] = [robots_open.url] if df.empty else robots_open.url
        except UnboundLocalError:
            df['robotstxt_url'] = [robotstxt_url] if df.empty else robotstxt_url
        df['download_date'] = pd.Timestamp.now(tz='UTC')
        if output_file is not None:
            with open(output_file, 'a') as file:
                file.write(df.to_json(orient='records',
                                      lines=True,
                                      date_format='iso'))
                file.write('\n')
        else:
            return df


def _robots_multi(robots_url_list, output_file=None):
    final_df = pd.DataFrame()
    with futures.ThreadPoolExecutor(max_workers=24) as executor:
        to_do = []
        for robotsurl in robots_url_list:
            future = executor.submit(robotstxt_to_df, robotsurl)
            to_do.append(future)
        done_iter = futures.as_completed(to_do)

        for future in done_iter:
            future_result = future.result()
            if output_file is not None:
                with open(output_file, 'a') as file:
                    file.write(future_result.to_json(orient='records',
                                                     lines=True,
                                                     date_format='iso'))
                    file.write('\n')
            else:
                final_df = final_df.append(future_result, ignore_index=True)
    if output_file is None:
        return final_df


def robotstxt_test(robotstxt_url, user_agents, urls):
    """Given a :attr:`robotstxt_url` check which of the :attr:`user_agents` is
    allowed to fetch which of the :attr:`urls`.

    All the combinations of :attr:`user_agents` and :attr:`urls` will be
    checked and the results returned in one DataFrame.

    >>> robotstxt_test('https://facebook.com/robots.txt',
    ...                user_agents=['*', 'Googlebot', 'Applebot'],
    ...                urls=['/', '/bbc', '/groups', '/hashtag/'])
                          robotstxt_url user_agent   url_path  can_fetch
    0   https://facebook.com/robots.txt          *          /      False
    1   https://facebook.com/robots.txt          *       /bbc      False
    2   https://facebook.com/robots.txt          *    /groups      False
    3   https://facebook.com/robots.txt          *  /hashtag/      False
    4   https://facebook.com/robots.txt   Applebot          /       True
    5   https://facebook.com/robots.txt   Applebot       /bbc       True
    6   https://facebook.com/robots.txt   Applebot    /groups       True
    7   https://facebook.com/robots.txt   Applebot  /hashtag/      False
    8   https://facebook.com/robots.txt  Googlebot          /       True
    9   https://facebook.com/robots.txt  Googlebot       /bbc       True
    10  https://facebook.com/robots.txt  Googlebot    /groups       True
    11  https://facebook.com/robots.txt  Googlebot  /hashtag/      False

    :param url robotstxt_url: The URL of robotx.txt file
    :param str,list user_agents: One or more user agents
    :param str,list urls: One or more paths (relative) or URLs (absolute) to
                           check
    :return DataFrame robotstxt_test_df:
    """
    if not robotstxt_url.endswith('/robots.txt'):
        raise ValueError('Please make sure you enter a valid robots.txt URL')
    if isinstance(user_agents, str):
        user_agents = [user_agents]
    if isinstance(urls, str):
        urls = [urls]
    robots_open = urlopen(Request(robotstxt_url, headers=headers))
    robots_bytes = robots_open.readlines()
    robots_text = ''.join(line.decode() for line in robots_bytes)
    rp = Protego.parse(robots_text)

    test_list = []
    for path, agent in product(urls, user_agents):
        d = dict()
        d['user_agent'] = agent
        d['url_path'] = path
        d['can_fetch'] = rp.can_fetch(path, agent)
        test_list.append(d)
    df = pd.DataFrame(test_list)
    df.insert(0, 'robotstxt_url', robotstxt_url)
    df = df.sort_values(['user_agent', 'url_path']).reset_index(drop=True)
    return df
