"""
.. _crawl_headers:

🕷 Python Status Code Checker with Response Headers
===================================================

A mini crawler that only makes ``HEAD`` requests to a known list of URLs. It
uses `Scrapy <https://docs.scrapy.org/en/latest>`_ under the hood, which means
you get all its power in a simplified interface for a simple and specific
use-case.

The :func:`crawl_headers` function can be used to make those requests for
various quality assurance and analysis reasons. Since ``HEAD`` requests don't
download the whole page, this makes the crawling super light on servers, and
makes the process very fast.

The function is straight-forward and easy to use, you basically need a list of
URLs and a file path where you want to save the output (in `.jl` format):

.. thebe-button::
    Run this code


.. code-block::
    :class: thebe, thebe-init

    import advertools as adv
    import pandas as pd

    url_list = ['https://advertools.readthedocs.io', 'https://adver.tools',
                'https://www.dashboardom.com', 'https://povertydata.org']
    adv.crawl_headers(url_list, 'output_file.jl')
    headers_df = pd.read_json('output_file.jl', lines=True)

    headers_df


====  ============================================  ===================  ========  ==================  =========================  ==================  =======  ==========  ======  =============================  =====================  =============================  ===========================  ===============================  ===============================================================  =================================  ============================  =================================  ===================  ================  ==============  =================================  ==================  ============================================================================  ===============================  =============================  ====================================  =======================  ========================  ============================  ============================  ==========================================  ===========================  ===================================  ===================================  ==============================  =================================  ============================================  ==============================  ==================  =============================  ============================  =======================================================================================  =====================  ===========================================  ==================
  ..  url                                           crawl_time             status    download_timeout  download_slot                download_latency    depth  protocol      body    resp_headers_content-length  resp_headers_server    resp_headers_date              resp_headers_content-type    resp_headers_content-encoding    request_headers_accept                                           request_headers_accept-language    request_headers_user-agent    request_headers_accept-encoding    resp_headers_vary      redirect_times    redirect_ttl  redirect_urls                        redirect_reasons  resp_headers_x-amz-id-2                                                       resp_headers_x-amz-request-id    resp_headers_last-modified     resp_headers_etag                     resp_headers_x-served    resp_headers_x-backend    resp_headers_x-rtd-project    resp_headers_x-rtd-version    resp_headers_x-rtd-path                     resp_headers_x-rtd-domain    resp_headers_x-rtd-version-method    resp_headers_x-rtd-project-method    resp_headers_referrer-policy    resp_headers_permissions-policy    resp_headers_strict-transport-security        resp_headers_cf-cache-status      resp_headers_age  resp_headers_expires           resp_headers_cache-control    resp_headers_expect-ct                                                                   resp_headers_cf-ray    resp_headers_alt-svc                         resp_headers_via
====  ============================================  ===================  ========  ==================  =========================  ==================  =======  ==========  ======  =============================  =====================  =============================  ===========================  ===============================  ===============================================================  =================================  ============================  =================================  ===================  ================  ==============  =================================  ==================  ============================================================================  ===============================  =============================  ====================================  =======================  ========================  ============================  ============================  ==========================================  ===========================  ===================================  ===================================  ==============================  =================================  ============================================  ==============================  ==================  =============================  ============================  =======================================================================================  =====================  ===========================================  ==================
   0  https://adver.tools                           2022-02-11 02:32:26       200                 180  adver.tools                         0.0270483        0  HTTP/1.1       nan                              0  nginx/1.18.0 (Ubuntu)  Fri, 11 Feb 2022 02:32:26 GMT  text/html; charset=utf-8     gzip                             text/html,application/xhtml+xml,application/xml;q=0.9,...;q=0.8  en                                 advertools/0.13.0.rc2         gzip, deflate                      nan                               nan             nan  nan                                               nan  nan                                                                           nan                              nan                            nan                                   nan                      nan                       nan                           nan                           nan                                         nan                          nan                                  nan                                  nan                             nan                                nan                                           nan                                            nan  nan                            nan                           nan                                                                                      nan                    nan                                          nan
   1  https://povertydata.org                       2022-02-11 02:32:26       200                 180  povertydata.org                     0.06442          0  HTTP/1.1       nan                          13270  nginx/1.18.0 (Ubuntu)  Fri, 11 Feb 2022 02:32:26 GMT  text/html; charset=utf-8     gzip                             text/html,application/xhtml+xml,application/xml;q=0.9,...;q=0.8  en                                 advertools/0.13.0.rc2         gzip, deflate                      Accept-Encoding                   nan             nan  nan                                               nan  nan                                                                           nan                              nan                            nan                                   nan                      nan                       nan                           nan                           nan                                         nan                          nan                                  nan                                  nan                             nan                                nan                                           nan                                            nan  nan                            nan                           nan                                                                                      nan                    nan                                          nan
   2  https://advertools.readthedocs.io/en/master/  2022-02-11 02:32:26       200                 180  advertools.readthedocs.io           0.0271282        0  HTTP/1.1       nan                              0  cloudflare             Fri, 11 Feb 2022 02:32:26 GMT  text/html                    gzip                             text/html,application/xhtml+xml,application/xml;q=0.9,...;q=0.8  en                                 advertools/0.13.0.rc2         gzip, deflate                      Accept-Encoding                     1              19  https://advertools.readthedocs.io                 302  rNKT7MYjJ7hcnSvbnZg9qdqizeFfTx9YtZ3/gwNLj8M99yumuCgdd6YTm/iBMO9hrZTAi/iYl50=  EE0DJX6Z511TGX88                 Thu, 10 Feb 2022 17:04:27 GMT  W/"14c904a172315a4922f4d28948b916c2"  Nginx-Proxito-Sendfile   web-i-0710e93d610dd8c3e   advertools                    master                        /proxito/html/advertools/master/index.html  advertools.readthedocs.io    path                                 subdomain                            no-referrer-when-downgrade      interest-cohort=()                 max-age=31536000; includeSubDomains; preload  HIT                                           1083  Fri, 11 Feb 2022 04:32:26 GMT  public, max-age=7200          max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"  6dba2aae6b424107-PRG   h3=":443"; ma=86400, h3-29=":443"; ma=86400  nan
   3  https://www.dashboardom.com                   2022-02-11 02:32:26       200                 180  www.dashboardom.com                 0.118614         0  HTTP/1.1       nan                          26837  gunicorn/19.9.0        Fri, 11 Feb 2022 02:32:26 GMT  text/html; charset=utf-8     nan                              text/html,application/xhtml+xml,application/xml;q=0.9,...;q=0.8  en                                 advertools/0.13.0.rc2         gzip, deflate                      nan                               nan             nan  nan                                               nan  nan                                                                           nan                              nan                            nan                                   nan                      nan                       nan                           nan                           nan                                         nan                          nan                                  nan                                  nan                             nan                                nan                                           nan                                            nan  nan                            nan                           nan                                                                                      nan                    nan                                          1.1 vegur
====  ============================================  ===================  ========  ==================  =========================  ==================  =======  ==========  ======  =============================  =====================  =============================  ===========================  ===============================  ===============================================================  =================================  ============================  =================================  ===================  ================  ==============  =================================  ==================  ============================================================================  ===============================  =============================  ====================================  =======================  ========================  ============================  ============================  ==========================================  ===========================  ===================================  ===================================  ==============================  =================================  ============================================  ==============================  ==================  =============================  ============================  =======================================================================================  =====================  ===========================================  ==================



Optionally, you can customize the crawling behavior with the optional
``custom_settings`` parameter. Please check the
`crawl strategies <_crawl_strategies>`_ page for tips on how you can do that.

Here are some of the common reasons for using a ``HEAD`` crawler:

* **Checking status codes:** One of the most important maintenance tasks you
  should be doing continuously. It's very easy to set up an automated script
  the checks status codes for a few hundred or thousand URLs on a periodic
  basis. You can easily build some rules and alerts based on the status codes
  you get.
* **Status codes of page elements:** Yes, your page returns a 200 OK status,
  but what about all the elements/components of the page? Images, links
  (internal and external), hreflang, canonical, URLs in metatags, script URLs,
  URLs in various structured data elements like Twitter, OpenGraph, and
  JSON-LD are some of the most important ones to check as well.
* **Getting search engine directives:** Those directives can be set using meta
  tags as well as response headers. This crawler gets all available response
  headers so you can check for search engine-specific ones, like `noindex` for
  example.
* **Getting image sizes:** You might want to crawl a list of image URLs and get
  their meta data. The response header `Content-Length` contains the length of
  the page in bytes. With images, it contains the size of the image. This can
  be an extremely efficient way of analyzing image sizes (and other meta data)
  without having to download those images, which could consume a lot of
  bandwidth. Lookout for the column ``resp_headers_content-length``.
* **Getting image types:** The ``resp_headers_content-type`` gives you an
  indication on the type of content of the page (or image when crawling image
  URLs); `text/html`, `image/jpeg` and `image/png` are some such content types.


"""  # noqa: E501

import datetime
import json
import subprocess

from scrapy import Request, Spider
from scrapy.exceptions import IgnoreRequest


import advertools as adv
from advertools import __version__ as adv_version
from advertools.spider import MAX_CMD_LENGTH, _split_long_urllist

header_spider_path = adv.__path__[0] + "/header_spider.py"

user_agent = f"advertools/{adv_version}"


class HeadersSpider(Spider):
    name = "headers_spider"
    custom_settings = {
        "USER_AGENT": user_agent,
        "ROBOTSTXT_OBEY": True,
        "HTTPERROR_ALLOW_ALL": True,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 8,
    }

    def __init__(self, url_list=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = json.loads(json.dumps(url_list.split(",")))

    def start_requests(self):
        for url in self.start_urls:
            try:
                yield Request(
                    url, callback=self.parse, errback=self.errback, method="HEAD"
                )
            except Exception as e:
                self.logger.error(repr(e))

    def errback(self, failure):
        if not failure.check(IgnoreRequest):
            self.logger.error(repr(failure))
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            yield {
                "url": failure.request.url,
                "crawl_time": now,
                "errors": repr(failure),
            }

    def parse(self, response):
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        yield {
            "url": response.url,
            "crawl_time": now,
            "status": response.status,
            **{
                k: "@@".join(str(val) for val in v) if isinstance(v, list) else v
                for k, v in response.meta.items()
            },
            "protocol": response.protocol,
            "body": response.text or None,
            **{
                "resp_headers_" + k: v
                for k, v in response.headers.to_unicode_dict().items()
            },
            **{
                "request_headers_" + k: v
                for k, v in response.request.headers.to_unicode_dict().items()
            },
        }


def crawl_headers(url_list, output_file, custom_settings=None):
    """Crawl a list of URLs using the HEAD method.

    This function helps in analyzing a set of URLs by getting status codes,
    download latency, all response headers and a few other meta data about the
    crawled URLs.

    Sine the full page is not downloaded, these requests are very light on
    servers and it is super-fast. You can modify the speed of course through
    various settings.

    Typically status code checking is an on-going task that needs to be done
    and managed. Automated alerts can be easily created based on certain status
    codes. Another interesting piece of the information is the `Content-Length`
    response header. This gives you the size of the response body without
    having to download the whole page. It can also be very interesting with
    image URLs. Downloading all images can really be expensive and time
    consuming. Being able to get image sizes without having to download them
    can help a lot in making decisions about optimizing those images.
    Several other data can be interesting to analyze, depending on what
    response headers you get.

    Parameters
    ----------
    url_list : str, list
      One or more URLs to crawl.
    output_file : str
      The path to the output of the crawl. Jsonlines only is supported to allow for
      dynamic values. Make sure your file ends with ".jl", e.g. `output_file.jl`.
    custom_settings : dict
      A dictionary of optional custom settings that you might want to add to the
      spider's functionality. There are over 170 settings for all kinds of options. For
      details please refer to the `spider settings <https://docs.scrapy.org/en/latest/topics/settings.html>`_
      documentation.

    Examples
    --------

    >>> import advertools as adv
    >>> url_list = ['https://exmaple.com/A', 'https://exmaple.com/B',
    ...             'https://exmaple.com/C', 'https://exmaple.com/D',
    ...             'https://exmaple.com/E']

    >>> adv.crawl_headers(url_list, 'output_file.jl')
    >>> import pandas as pd
    >>> crawl_df = pd.read_json('output_file.jl', lines=True)
    """
    if isinstance(url_list, str):
        url_list = [url_list]
    if output_file.rsplit(".")[-1] != "jl":
        raise ValueError(
            "Please make sure your output_file ends with '.jl'.\n"
            "For example:\n"
            f"{output_file.rsplit('.', maxsplit=1)[0]}.jl"
        )
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
        header_spider_path,
        "-a",
        "url_list=" + ",".join(url_list),
        "-o",
        output_file,
    ] + settings_list
    if len(",".join(url_list)) > MAX_CMD_LENGTH:
        split_urls = _split_long_urllist(url_list)
        for u_list in split_urls:
            command[4] = "url_list=" + ",".join(u_list)
            subprocess.run(command)
    else:
        subprocess.run(command)
