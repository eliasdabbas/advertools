"""

Image Crawler and Downloader
============================

**Experimental feature - expect changes**

This is a crawler that downloads all images on a given list of URLs. Using
:func:`crawl_images` is straightforward:

>>> import advertools as adv
>>> adv.crawl_images([URL_1, URL_2, URL_3, ...], "output_dir")

This would go to the supplied URLs and download all images found on those URLs, and
place them in ``output_dir``.

You can set a few conditions to modify the behavior:

* ``min_width``: The minimum width in pixels for an image to be downloaded. This is
  mainly to avoid downloading logos, tracking pixels, navigational elemenst as images,
  and so on.
* ``min_height``: The minimum height in pixels for an image to be downloaded
* ``include_img_regex``: A regular expression that the image path needs to match in
  order for it to be downloaded. In some cases, after checking the patterns of images
  for example, you might want to only download images that contain "sports", or any
  other pattern. Or maybe images of interest are under the /economy/ folder and you only
  want those images.
* ``custom_settings``: Just like other crawl functions, you can set any custom settings
  you want to control the crawler's behavior. Some examples include changing the
  User-agent, (dis)obeying robots.txt rules, and so on. More options and code details
  can be found in the :ref:`crawling strategies <crawl_strategies>` page.

To run the :func:`crawl_images` function you need to set an ``output_dir``. This is
where all images will be downloaded. You also get a summary file with details about the
downloaded images. You can read this file through the special function
:func:`summarize_crawled_imgs` to get a few more details about those images.

>>> adv.summarize_crawled_imgs("path/to/output_dir")

====  ==============================================================================================  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
  ..  image_location                                                                                  image_urls
====  ==============================================================================================  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
   0  https://www.buzzfeed.com/hannahdobro/dirty-little-industry-secrets?origin=tuh                   https://img.buzzfeed.com/buzzfeed-static/static/user_images/6r1oxXOpC_large.jpg?downsize=120:&output-format=jpg&output-quality=auto
   0  https://www.buzzfeed.com/hannahdobro/dirty-little-industry-secrets?origin=tuh                   https://img.buzzfeed.com/buzzfeed-static/static/2024-03/18/16/asset/fce856744ed8/sub-buzz-1303-1710779249-1.jpg
   0  https://www.buzzfeed.com/hannahdobro/dirty-little-industry-secrets?origin=tuh                   data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
   0  https://www.buzzfeed.com/hannahdobro/dirty-little-industry-secrets?origin=tuh                   https://img.buzzfeed.com/buzzfeed-static/static/2024-03/18/16/asset/245ecfa321e9/sub-buzz-894-1710779358-1.jpg
   1  https://www.buzzfeed.com/chelseastewart/josh-peck-statement-drake-bell-abuse-claims?origin=tuh  https://img.buzzfeed.com/buzzfeed-static/static/2017-12/12/13/user_images/buzzfeed-prod-web-03/chelseastewart-v2-5590-1513102854-0_large.jpg?downsize=120:&output-format=jpg&output-quality=auto
   1  https://www.buzzfeed.com/chelseastewart/josh-peck-statement-drake-bell-abuse-claims?origin=tuh  https://img.buzzfeed.com/buzzfeed-static/static/2024-03/21/19/asset/ea6298160040/sub-buzz-1093-1711048323-1.jpg?downsize=700%3A%2A&output-quality=auto&output-format=auto
   1  https://www.buzzfeed.com/chelseastewart/josh-peck-statement-drake-bell-abuse-claims?origin=tuh  data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
   1  https://www.buzzfeed.com/chelseastewart/josh-peck-statement-drake-bell-abuse-claims?origin=tuh  data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQAAAA7CAMAAADSF118AAAAP1BMVEUAAADIGxPOHBK5EwDFGhi5Fwi8GRTEGhe7EQDMHR7////vyMfddnm5Hx334+Py8fHdj5DLVVXnq6zJOTzVbG1s8SkwAAAACXRSTlMAv4Eo10JnqA8IHfydAAABJUlEQVRYw93Y64rCMBCG4czk5FSzdav3f63bDaxfV4Qm+AXR96/wMNj0kLhtPib9LcutYA8K+F1rKXqH4KmIPZVIOvwnszEqumFjMVLB3+YsRiv8zRqMWHa1ZNQiBuUV3Jo3cn5FlY3qimY2KitajB3+UmLRxRGovgmqTj4HXc69aN5Hj9PcyYqzfXSavk58tJMNTWgv24pW9kpE0fGbioKlomCZKNgLEUXLhYiiMx+dT+xJ8SxgoCDZ6EJcp7jsPBQLlIbiVmpEwy7aS1poeZ30PvqlAQVJRGeQtLfp1dBLPyb0bdDER+OYL2nHR7E34yUjtjw6ZMc3am/KXlSpoodCHrQWiWbxI85Q6Kc9pneHSCmHJ0VJGPPuAC3LWqO/OURL0aEfg76m8Izrt6EAAAAASUVORK5CYII=
   2  https://www.buzzfeed.com/josephlongo/celebs-wearing-rewearing-same-dress?origin=tuh             https://img.buzzfeed.com/buzzfeed-static/static/2021-06/3/16/user_images/a824550933a9/tomiobaro-v2-2174-1622738336-41_large.jpg?downsize=120:&output-format=jpg&output-quality=auto
   2  https://www.buzzfeed.com/josephlongo/celebs-wearing-rewearing-same-dress?origin=tuh             https://img.buzzfeed.com/buzzfeed-static/static/2024-03/19/13/asset/6634db63f453/sub-buzz-576-1710855734-6.jpg?downsize=700%3A%2A&output-quality=auto&output-format=auto
   2  https://www.buzzfeed.com/josephlongo/celebs-wearing-rewearing-same-dress?origin=tuh             https://img.buzzfeed.com/buzzfeed-static/static/2024-03/19/13/asset/cb8db05df7e7/sub-buzz-1743-1710855790-4.jpg
   2  https://www.buzzfeed.com/josephlongo/celebs-wearing-rewearing-same-dress?origin=tuh             data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
====  ==============================================================================================  ==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

Image file names
----------------

The downloaded images need to be given a name naturally, and the name is taken from the
slug of the image URL, excluding any query parameters or slashes.
The full URLs of those images can be found in the summary file, and you can access them
through :func:`summarize_crawled_imgs`. You also see where those images are located as
you can see in the table above.

"""  # noqa: E501

import json
import re
import subprocess
from urllib.parse import urlsplit

import pandas as pd
from scrapy import Field, Item, Request, Spider
from scrapy.pipelines.images import ImagesPipeline

import advertools as adv

image_spider_path = adv.__path__[0] + "/image_spider.py"

user_agent = f"advertools/{adv.__version__}"


class ImgItem(Item):
    image_urls = Field()
    images = Field()
    image_location = Field()


class AdvImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        img_url = request.url
        return urlsplit(img_url).path.split("/")[-1]


class ImageSpider(Spider):
    name = "image_spider"
    include_img_regex = None
    custom_settings = {
        "USER_AGENT": user_agent,
        "ROBOTSTXT_OBEY": True,
        "HTTPERROR_ALLOW_ALL": True,
        "ITEM_PIPELINES": {AdvImagesPipeline: 1},
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 8,
    }

    def __init__(self, start_urls, include_img_regex=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(start_urls.split(",")))
        if include_img_regex is not None:
            self.include_img_regex = include_img_regex

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        img_item = ImgItem()
        img_src = response.xpath("//img/@src").getall()
        if self.include_img_regex is not None:
            img_src = [
                response.urljoin(src)
                for src in img_src
                if re.findall(self.include_img_regex, src)
            ]
        else:
            img_src = [response.urljoin(src) for src in img_src]
        img_item["image_urls"] = img_src
        img_item["image_location"] = response.request.url
        yield img_item


def crawl_images(
    start_urls,
    output_dir,
    min_width=0,
    min_height=0,
    include_img_regex=None,
    custom_settings=None,
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
                setting = "=".join([key, json.dumps(val)])
            else:
                setting = "=".join([key, str(val)])
            settings_list.extend(["-s", setting])

    command = [
        "scrapy",
        "runspider",
        image_spider_path,
        "-a",
        "start_urls=" + ",".join(start_urls),
        "-s",
        "IMAGES_STORE=" + output_dir,
        "-s",
        "IMAGES_MIN_HEIGHT=" + str(min_height),
        "-s",
        "IMAGES_MIN_WIDTH=" + str(min_width),
        "-o",
        output_dir + "/image_summary.jl",
    ] + settings_list
    if include_img_regex is not None:
        command += ["-a", "include_img_regex=" + include_img_regex]
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
    df = pd.read_json(image_dir.rstrip("/") + "/image_summary.jl", lines=True)
    return df[["image_location", "image_urls"]].explode("image_urls")
