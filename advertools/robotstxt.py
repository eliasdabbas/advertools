"""
.. _robotstxt:

🤖 robots.txt Tester for Large Scale Testing
============================================

Even though they are tiny in size, robots.txt files contain potent information
that can block major sections of your site, which is what they are supposed to
do. Only sometimes you might make the mistake of blocking the wrong section.

So it is very important to check if certain pages (or groups of pages) are
blocked for a certain user-agent by a certain robots.txt file. Ideally, you
would want to run the same check for all possible user-agents. Even more
ideally, you want to be able to run the check for a large number of pages with
every possible combination with user-agents!

To get the robots.txt file into an easily readable format, you can use the
:func:`robotstxt_to_df` function to get it in a DataFrame.

>>> robotstxt_to_df('https://www.google.com/robots.txt')
      directive                             content                      robotstxt_url                  file_downloaded
0    User-agent                                   *  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
1      Disallow                             /search  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
2         Allow                       /search/about  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
3         Allow                      /search/static  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
4         Allow              /search/howsearchworks  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
..          ...                                 ...                                ...                              ...
277  User-agent                          Twitterbot  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
278       Allow                             /imgres  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
279  User-agent                 facebookexternalhit  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
280       Allow                             /imgres  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
281     Sitemap  https://www.google.com/sitemap.xml  https://www.google.com/robots.txt 2020-06-01 14:05:16.068031+00:00
[282 rows x 4 columns]


The returned DataFrame contains columns for directives, their content, the URL
of the robots.txt file, as well as the date it was downloaded.
Under the `directive` column you can see the main commands; Allow, Disallow,
Sitemap, Crawl-delay, User-agent, and so on. The `content` column contains the
details of each of those directives (the pattern to disallow, the sitemap URL,
etc.)

As for testing, the :func:`robotstxt_test` function runs a test for a given
robots.txt file, checking which of the provided user-agents can fetch which of
the provided URLs, paths, or patterns.

>>> robotstxt_test('https://www.example.com/robots.txt',
...                useragents=['Googlebot', 'baiduspider', 'Bingbot']
...                urls=['/', '/hello', '/some-page.html']])

As a result, you get a DataFrame with a row for each combination of
(user-agent, URL) indicating whether or not that particular user-agen can fetch
the given URL.

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
  check whether or not they are blocked from a fetching a certain URL
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
>>> fb_robots
      directive                                            content                        robotstxt_url                  file_downloaded
0       comment  Notice: Collection of data on Facebook through...  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
1       comment  prohibited unless you have express written per...  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
2       comment  and may only be conducted for the limited purp...  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
3       comment                                        permission.  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
4       comment  See: http://www.facebook.com/apps/site_scrapin...  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
..          ...                                                ...                                  ...                              ...
461       Allow                         /ajax/bootloader-endpoint/  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
462       Allow  /ajax/pagelet/generic.php/PagePostsSectionPagelet  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
463       Allow                                      /safetycheck/  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
464  User-agent                                                  *  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
465    Disallow                                                  /  https://www.facebook.com/robots.txt 2020-05-31 20:12:47.576281+00:00
[466 rows x 4 columns]

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
"*" are not allowed to fetch any of the provided URLs).

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

I'll leave to you to figure out why LinkedIn and Pinterest are not allowed to
crawl the home page but Google and Apple are, because I have no clue!
"""
__all__ = ['robotstxt_to_df', 'robotstxt_test']

import logging
from urllib.request import Request, urlopen
from itertools import product

from protego import Protego
import pandas as pd

from advertools import __version__ as version

headers = {'User-Agent': 'advertools-' + version}

logging.basicConfig(level=logging.INFO)


def robotstxt_to_df(robotstxt_url):
    """Download the contents of ``robotstxt_url`` into a DataFrame

    :param url robotstxt_url: The URL of the robots.txt file
    :returns DataFrame robotstxt_df: A DataFrame containing directives, their
                                     content, the URL and time of download
    """
    logging.info(msg='Getting: ' + robotstxt_url)
    robots_open = urlopen(Request(robotstxt_url, headers=headers))
    robots_text = robots_open.readlines()

    lines = []
    for line in robots_text:
        if line and line.decode().startswith('#'):
            lines.append(['comment', line.decode().replace('#', '').strip()])
        if line and line.decode()[0].isupper():
            split = line.decode().split(':', maxsplit=1)
            lines.append([split[0], split[1].strip()])
    df = pd.DataFrame(lines, columns=['directive', 'content'])
    df['robotstxt_url'] = robotstxt_url
    df['file_downloaded'] = pd.Timestamp.now(tz='UTC')
    return df


def robotstxt_test(robotstxt_url, user_agents, urls):
    """Given a :attr:`robotstxt_url` check which of the :attr:`user_agents` is
    allowed to fetch which of the :attr:`urls`.

    All the combinations of :attr:`user_agents` and :attr:`urls` will be
    checked and the results returned in one DataFrame.

    >>> robotstxt_test('https://facebook.com/robots.txt',
    ...                user_agents=['*', 'Googlebot', 'Applebot'],
    ...                urls=['/', '/bbc', '/groups', '/hashtag/'])
                                  robotstxt_url user_agent   url_path  can_fetch
    0   https://www.facebook.com/robots.txt          *       /bbc      False
    1   https://www.facebook.com/robots.txt          *    /groups      False
    2   https://www.facebook.com/robots.txt          *          /      False
    3   https://www.facebook.com/robots.txt          *  /hashtag/      False
    4   https://www.facebook.com/robots.txt   Applebot          /       True

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

    df = pd.DataFrame()
    for path, agent in product(urls, user_agents):
        d = dict()
        d['user_agent'] = agent
        d['url_path'] = path
        d['can_fetch'] = rp.can_fetch(path, agent)
        df = df.append(pd.DataFrame(d, index=range(1)), ignore_index=True)
    df.insert(0, 'robotstxt_url', robotstxt_url)
    df = df.sort_values('user_agent').reset_index(drop=True)
    return df
