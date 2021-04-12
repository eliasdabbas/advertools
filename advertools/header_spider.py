import datetime
from scrapy import Spider, Request
import pandas as pd

from advertools import __version__ as adv_version

user_agent = f'advertools/{adv_version}'


start_urls = [
    'https://www.google.com',
    'https://www.media-supermarket.com',
    'https://povertydata.org',
    'https://www.linkedin.com',
    'https://www.cnn.com',
    'https://nytimes.com',
    'https://www.python.org',
]

start_urls = pd.read_csv('/Users/me/Desktop/temp/mjstc100k.csv')['Domain'][:1000]


class HeadersSpider(Spider):
    name = 'headers_spider'
    custom_settings = {
        'USER_AGENT': user_agent,
        'ROBOTSTXT_OBEY': False,
        'HTTPERROR_ALLOW_ALL': True,
    }

    def start_requests(self):
        for url in start_urls:
            yield Request(url, callback=self.parse, method='HEAD')

    def parse(self, response):
        yield {
            'url': response.url,
            'crawl_time': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'status': response.status,
            'download_latency': response.meat['download_latency'],
            # **{k: '@@'.join(str(val) for val in v) if isinstance(v, list)
            #    else v for k, v in response.meta.items()},
            # **{'resp_headers_' + k: v
            #    for k, v in response.headers.to_unicode_dict().items()},
            # **{'request_headers_' + k: v
            #    for k, v in response.request.headers.to_unicode_dict().items()},

        }
