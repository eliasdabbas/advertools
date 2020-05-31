"""
.. _robotstxt:

🤖 Robots.txt Tester for Large Scale Testing
============================================



"""

from urllib.request import Request, urlopen
from itertools import product

from protego import Protego
import pandas as pd

from advertools import __version__ as version

headers = {'User-Agent': 'advertools-' + version}


def robotstxt_test(robotstxt_url, useragents, urls):
    """Given a :attr:`robotstxt_url` check which of the :attr:`useragents` is
    allowed to fetch which of the :attr:`urls`.

    :param url robotstxt_url: The URL of robotx.txt file
    :param str,list useragents: One or more user agents
    :param str, list urls: One or more paths (relative) or URLs (absolute) to
                           check
    :return DataFrame:
    """
    robots_open = urlopen(Request(robotstxt_url, headers=headers))
    robots_bytes = robots_open.readlines()
    robots_text = ''.join(line.decode() for line in robots_bytes)
    rp = Protego.parse(robots_text)

    df = pd.DataFrame()
    for path, agent in product(urls, useragents):
        d = dict()
        d['user_agent'] = agent
        d['url_path'] = path
        d['can_fetch'] = rp.can_fetch(path, agent)
        df = df.append(pd.DataFrame(d, index=range(1)), ignore_index=True)
    df.insert(0, 'robotstxt_url', robotstxt_url)
    df = df.sort_values('user_agent').reset_index(drop=True)
    return df
