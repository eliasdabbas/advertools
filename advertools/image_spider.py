import json
import re
import subprocess
from urllib.parse import urlsplit

import pandas as pd
from scrapy import Field, Item, Request, Spider
from scrapy.pipelines.images import ImagesPipeline

import advertools as adv

image_spider_path = adv.__path__[0] + '/image_spider.py'

user_agent = f'advertools/{adv.__version__}'


class ImgItem(Item):
    image_urls = Field()
    images = Field()
    image_location = Field()


class AdvImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        img_url = request.url
        return urlsplit(img_url).path.split('/')[-1]


class ImageSpider(Spider):
    name = 'image_spider'
    include_img_regex = None
    custom_settings = {
        'USER_AGENT': user_agent,
        'ROBOTSTXT_OBEY': True,
        'HTTPERROR_ALLOW_ALL': True,
        'ITEM_PIPELINES': {AdvImagesPipeline: 1},
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8,
    }

    def __init__(self, start_urls, include_img_regex=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(start_urls.split(',')))
        if include_img_regex is not None:
            self.include_img_regex = include_img_regex

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        img_item = ImgItem()
        img_src = response.xpath('//img/@src').getall()
        if self.include_img_regex is not None:
            img_src = [response.urljoin(src) for src in img_src
                       if re.findall(self.include_img_regex, src)]
        else:
            img_src = [response.urljoin(src) for src in img_src]
        img_item['image_urls'] = img_src
        img_item['image_location'] = response.request.url
        yield img_item


def crawl_images(
    start_urls,
    output_dir,
    min_width=0,
    min_height=0,
    include_img_regex=None,
    custom_settings=None
):
    """Download all images available on start_urls and save them to output_dir.

    THIS FUNCTION IS STILL EXPERIMENTAL. Expect many changes.

    Parameters
    ----------

    start_urls : list
      A list of URLs from which you want to download available images.
    output_dir : str
      The directory where you want the images to be saved.
    min_width : int
      The minimum width in pixels for an image to be downloaded.
    min_height : int
      The minimum height in pixels for an image to be downloaded.
    include_img_regex : str
      A regular expression to select image src URLs. Use this to restrict image
      files that match this regex.
    custom_settings : dict
      Additional settings to customize the crawling behaviour.
    """
    settings_list = []
    if custom_settings is not None:
        for key, val in custom_settings.items():
            if isinstance(val, dict):
                setting = '='.join([key, json.dumps(val)])
            else:
                setting = '='.join([key, str(val)])
            settings_list.extend(['-s', setting])

    command = [
        'scrapy', 'runspider', image_spider_path,
        '-a', 'start_urls=' + ','.join(start_urls),
        '-s', 'IMAGES_STORE=' + output_dir,
        '-s', 'IMAGES_MIN_HEIGHT=' + str(min_height),
        '-s', 'IMAGES_MIN_WIDTH=' + str(min_width),
        '-o', output_dir + '/image_summary.jl'
        ] + settings_list
    if include_img_regex is not None:
        command += ['-a', 'include_img_regex=' + include_img_regex]
    subprocess.run(command)


def summarize_crawled_imgs(image_dir):
    """Provide a DataFrame of image locations and image URLs resulting from
    crawl_images.

    Running the crawl_images function create a summary CSV file of the
    downloaded images. This function parses that file and provides a two-column
    DataFrame:

    - image_location: The URL from which the images was downloaded from.
    - image_urls: The URL of the image file tha was downloaded.

    Parameters
    ----------
    image_dir : str
      The path to the directory that you provided to crawl_images
    """
    df = pd.read_json(image_dir.rstrip('/') + '/image_summary.jl', lines=True)
    return df[['image_location', 'image_urls']].explode('image_urls')
