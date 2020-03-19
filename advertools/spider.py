import datetime
import json
import subprocess


from scrapy.spiders import SitemapSpider
import advertools as adv

spider_path = adv.__path__[0] + '/spider.py'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',


class SEOSitemapSpider(SitemapSpider):
    name = 'seo_sitemap_spider'
    custom_settings = {
        'USER_AGENT': user_agent,
        'ROBOTSTXT_OBEY': True,
        'HTTPERROR_ALLOW_ALL': True,
        'CLOSESPIDER_PAGECOUNT': 20,
        'DOWNLOAD_DELAY': 3,
        'BOT_NAME': 'adverbot'
    }

    def __init__(self, sitemap_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sitemap_urls = json.loads(json.dumps(sitemap_urls.split(',')))

    def parse(self, response):
        yield dict(
            url=response.url,
            title='@@'.join(response.css('title::text').getall()),
            meta_desc=response.xpath("//meta[@name='description']/@content").get(),
            h1='@@'.join(response.css('h1::text').getall()),
            h2='@@'.join(response.css('h2::text').getall()),
            h3='@@'.join(response.css('h3::text').getall()),
            body_text='\n'.join(response.css('p::text').getall()),
            size=len(response.body),
            load_time=response.meta['download_latency'],
            status=response.status,
            links_href='@@'.join([link.attrib.get('href') or '' for link in response.css('a')]),
            links_text='@@'.join([link.attrib.get('title') or '' for link in response.css('a')]),
            img_src='@@'.join([im.attrib.get('src') or '' for im in response.css('img')]),
            img_alt='@@'.join([im.attrib.get('alt') or '' for im in response.css('img')]),
            page_depth=response.meta['depth'],
            crawl_time=datetime.datetime.utcnow(),
        )


def crawl(sitemap_urls, output_file):
    """
    Crawl a website's URLs based on the given :attr:`sitemap_urls`

    :param list sitemap_urls: A list of one or more XML sitemap URLs.
    :param str output_file: The path to the output of the crawl. Supported
    formats ('csv', 'json', 'jsonlines', 'jl', 'xml', 'marshal', 'pickle')
    """
    if isinstance(sitemap_urls, str):
        sitemap_urls = [sitemap_urls]
    command = ['scrapy', 'runspider', spider_path,
               '-a', 'sitemap_urls=' + ','.join(sitemap_urls),
               '-o', output_file]
    subprocess.run(command)
