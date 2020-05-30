"""

Robots.txt Tester on a Large Scale
==================================


"""

from urllib.request import Request, urlopen
from itertools import product

from protego import Protego
import pandas as pd


headers = {'User-Agent': 'advertools-' + 'v0.10.2'}


def robotstxt_tester(robotstxt_url, urls, useragents=('*',)):
    robots_open = urlopen(Request(robotstxt_url, headers=headers))
    robots_bytes = robots_open.readlines()
    robots_text = ''.join(line.decode() for line in robots_bytes)
    rp = Protego.parse(robots_text)

    df = pd.DataFrame()
    for path, agent in product(urls, useragents):
        d = dict()
        d['robotstxt'] = robotstxt_url
        d['url_path'] = path
        d['user_agent'] = agent
        d['can_fetch'] = rp.can_fetch(path, agent)
        d['crawl_delay'] = rp.crawl_delay(agent)
        request_rate = rp.request_rate(agent)
        if request_rate is not None:
            d['request_rate_requests'] =request_rate.requests
            d['request_rate_seconds'] = request_rate.seconds
            d['request_rate_start_time'] = request_rate.start_time
            d['request_rate_end_time'] = request_rate.end_time
        df = df.append(pd.DataFrame(d, index=range(1)), ignore_index=True)
    return df
