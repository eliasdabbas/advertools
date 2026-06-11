"""
.. _crawl_screenshots:

📸 Screenshot Capturing
==============================

Capture screenshots for a list of URLs and save crawl metadata to a JSON Lines
file.

The :func:`crawl_screenshots` function uses Scrapy together with the optional
``scrapy-playwright`` package. It is designed for list-mode screenshot
capture only: you supply one or more known URLs, screenshots are saved to disk,
and one metadata
row is written per URL.

Installation
------------

Screenshot capturing requires optional browser automation dependencies and
browser binaries. This optional feature requires Python >= 3.10, but the base
``advertools`` install remains unchanged::

    pip install "advertools[screenshots]"
    playwright install chromium

Only ``http://`` and ``https://`` URLs are supported. The metadata output file
is replaced on every run. Screenshots are saved as image files and are not
embedded in the JSON Lines metadata. The capture job obeys robots.txt by default,
and concurrency can be tuned through ``custom_settings``.

Basic Screenshot Capture
------------------------

Capture full-page PNG screenshots for a known list of URLs. This function does
not discover links; feed it URLs from sitemaps, crawls, SERPs, logs, analytics
exports, or your own lists.

.. code-block:: python

    import advertools as adv
    import pandas as pd

    adv.crawl_screenshots(
        ["https://example.com", "https://www.python.org"],
        "screenshots/basic.jl",
        screenshot_dir="screenshots/images",
        timeout=10000,
    )

    screenshot_df = pd.read_json("screenshots/basic.jl", lines=True)
    screenshot_df[
        [
            "url",
            "final_url",
            "status",
            "screenshot_path",
            "screenshot_success",
            "screenshot_size_bytes",
        ]
    ]

JPEG Screenshots
----------------

Use JPEG when smaller files are more important than lossless PNG output.
``quality`` is valid only with ``image_type="jpeg"``.

.. code-block:: python

    adv.crawl_screenshots(
        "https://example.com",
        "screenshots/jpeg.jl",
        screenshot_dir="screenshots/jpeg_images",
        image_type="jpeg",
        quality=80,
    )

Viewport-Only Screenshots
-------------------------

By default, screenshots capture the full scrollable page. Set
``full_page=False`` to capture only the current viewport.

.. code-block:: python

    adv.crawl_screenshots(
        "https://example.com",
        "screenshots/viewport.jl",
        screenshot_dir="screenshots/viewport_images",
        full_page=False,
        context_kwargs={"viewport": {"width": 1440, "height": 900}},
    )

Mobile Rendering
----------------

Use Playwright browser context options to emulate a mobile viewport.

.. code-block:: python

    adv.crawl_screenshots(
        "https://example.com",
        "screenshots/mobile.jl",
        screenshot_dir="screenshots/mobile_images",
        context_kwargs={
            "viewport": {"width": 390, "height": 844},
            "device_scale_factor": 2,
            "is_mobile": True,
        },
    )

Waiting for Dynamic Content
---------------------------

Use ``wait_until`` for the navigation wait condition, ``wait_for_timeout`` for
a fixed post-load delay, and ``timeout`` as a maximum for navigation and
screenshot operations.

.. code-block:: python

    adv.crawl_screenshots(
        "https://example.com",
        "screenshots/waited.jl",
        screenshot_dir="screenshots/waited_images",
        wait_until="networkidle",
        wait_for_timeout=1000,
        timeout=15000,
    )

Cookie Banners, Lazy Loading, and Other Page Actions
----------------------------------------------------

Pass serializable Playwright page methods as ``actions``. The screenshot action
is added automatically, so don't include ``{"method": "screenshot"}``.

.. code-block:: python

    adv.crawl_screenshots(
        "https://example.com",
        "screenshots/actions.jl",
        screenshot_dir="screenshots/actions_images",
        actions=[
            {"method": "click", "args": ["#accept-cookies"], "timeout": 3000},
            {"method": "wait_for_selector", "args": ["main"]},
            {
                "method": "evaluate",
                "args": ["window.scrollTo(0, document.body.scrollHeight)"],
            },
            {"method": "wait_for_timeout", "args": [500]},
        ],
    )

Desktop and Mobile Comparison
-----------------------------

Run separate crawls with the same URL list and different ``run_id`` values.
The ``run_id`` is included in screenshot filenames and metadata.

.. code-block:: python

    urls = ["https://example.com", "https://www.python.org"]

    adv.crawl_screenshots(
        urls,
        "screenshots/desktop_compare.jl",
        screenshot_dir="screenshots/desktop_compare_images",
        run_id="desktop",
        context_kwargs={"viewport": {"width": 1440, "height": 900}},
    )

    adv.crawl_screenshots(
        urls,
        "screenshots/mobile_compare.jl",
        screenshot_dir="screenshots/mobile_compare_images",
        run_id="mobile",
        context_kwargs={
            "viewport": {"width": 390, "height": 844},
            "is_mobile": True,
        },
    )

Feeding URLs from Other advertools Functions
--------------------------------------------

Use screenshot capturing after discovering URLs with :func:`sitemap_to_df` or
:func:`crawl`.

.. code-block:: python

    sitemap_df = adv.sitemap_to_df("https://www.example.com/sitemap.xml")
    urls = sitemap_df["loc"].dropna().head(100)

    adv.crawl_screenshots(
        urls,
        "screenshots/sitemap_urls.jl",
        screenshot_dir="screenshots/sitemap_url_images",
        custom_settings={"CONCURRENT_REQUESTS": 2},
    )

Command Line Examples
---------------------

The CLI mirrors the Python API. JSON options can be inline JSON or ``@file``
references, which is safer for shell quoting.

.. code-block:: console

    advertools screenshots https://example.com https://www.python.org \
        screenshots/basic.jl --screenshot-dir screenshots/images

    advertools screenshots https://example.com screenshots/mobile.jl \
        --screenshot-dir screenshots/mobile_images \
        --context-kwargs-json @screenshots/mobile-context.json

    advertools screenshots https://example.com screenshots/actions.jl \
        --actions-json @screenshots/actions.json --timeout-ms 15000

"""

import datetime
from contextlib import suppress
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

from scrapy import Request
from scrapy.spiders import Spider

from advertools import __version__ as adv_version

screenshot_spider_path = os.path.abspath(__file__)

user_agent = f"advertools/{adv_version}"

_ALLOWED_IMAGE_TYPES = {"png", "jpeg"}
_ALLOWED_URL_SCHEMES = {"http", "https"}
_ALLOWED_WAIT_UNTIL = {"load", "domcontentloaded", "networkidle", "commit"}
_DEFAULT_DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
_DEFAULT_TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
_INTERNAL_META_KEYS = {
    "playwright",
    "playwright_page_methods",
    "playwright_page_goto_kwargs",
    "playwright_context",
    "playwright_context_kwargs",
    "screenshot_path",
    "screenshot_type",
    "screenshot_index",
    "run_id",
}


def _now():
    try:
        utc = datetime.UTC
    except AttributeError:
        utc = datetime.timezone.utc
    return datetime.datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S")


def _default_run_id():
    try:
        utc = datetime.UTC
    except AttributeError:
        utc = datetime.timezone.utc
    return datetime.datetime.now(utc).strftime("%Y%m%dT%H%M%S%fZ")


def _safe_filename_part(value, max_length=80):
    value = str(value or "").strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    if not value:
        value = "url"
    return value[:max_length].strip("-._") or "url"


def _url_slug(url, max_length=80):
    parsed = urlparse(url)
    if parsed.netloc:
        raw_slug = parsed.netloc + parsed.path
    elif parsed.path:
        raw_slug = parsed.path
    else:
        raw_slug = url
    return _safe_filename_part(raw_slug.replace("/", "-"), max_length=max_length)


def _screenshot_filename(url, index, run_id, image_type):
    url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    safe_run_id = _safe_filename_part(run_id, max_length=40)
    slug = _url_slug(url)
    return f"{safe_run_id}-{int(index):05d}-{slug}-{url_hash}.{image_type}"


def _screenshot_path(url, index, screenshot_dir, run_id, image_type):
    filename = _screenshot_filename(url, index, run_id, image_type)
    return os.path.normpath(os.path.join(screenshot_dir, filename))


def _normalize_url_list(url_list):
    if isinstance(url_list, str):
        url_list = [url_list]
    else:
        try:
            url_list = list(url_list)
        except TypeError as e:
            raise TypeError(
                "url_list must be a URL string or an iterable of URLs"
            ) from e
    if not url_list:
        raise ValueError("url_list must contain at least one URL")
    normalized = []
    for index, url in enumerate(url_list):
        if not isinstance(url, str):
            raise TypeError(f"url_list item at index {index} must be a string")
        url = url.strip()
        if not url:
            raise ValueError(f"url_list item at index {index} must not be empty")
        parsed = urlparse(url)
        if parsed.scheme.lower() not in _ALLOWED_URL_SCHEMES or not parsed.netloc:
            raise ValueError(
                "url_list item at index {} must be an http:// or https:// URL; "
                "got {!r}".format(index, url)
            )
        normalized.append(url)
    return normalized


def _validate_output_file(output_file):
    output_file = os.fspath(output_file)
    extension = output_file.rsplit(".", maxsplit=1)[-1]
    if extension not in ["jl", "jsonl"]:
        raise ValueError(
            "Please make sure your output_file ends with '.jl' or '.jsonl'.\n"
            "For example:\n"
            "{}.jl".format(output_file.rsplit(".", maxsplit=1)[0])
        )
    return output_file


def _validate_timeout(timeout, name):
    if timeout is not None:
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout < 0
        ):
            raise ValueError(f"{name} must be a non-negative number")


def _validate_screenshot_options(
    image_type, quality, wait_until, wait_for_timeout, timeout
):
    image_type = str(image_type).lower()
    if image_type not in _ALLOWED_IMAGE_TYPES:
        raise ValueError("image_type must be one of: 'png', 'jpeg'")
    if quality is not None:
        if image_type != "jpeg":
            raise ValueError("quality can only be set when image_type='jpeg'")
        if (
            isinstance(quality, bool)
            or not isinstance(quality, int)
            or not 0 <= quality <= 100
        ):
            raise ValueError("quality must be an integer between 0 and 100")
    if wait_until not in _ALLOWED_WAIT_UNTIL:
        raise ValueError(
            "wait_until must be one of: " + ", ".join(sorted(_ALLOWED_WAIT_UNTIL))
        )
    _validate_timeout(wait_for_timeout, "wait_for_timeout")
    _validate_timeout(timeout, "timeout")
    return image_type


def _probe_writable_dir(directory):
    os.makedirs(directory, exist_ok=True)
    probe_file = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            dir=directory,
            prefix=".advertools_write_probe_",
            encoding="utf-8",
        ) as temp_file:
            probe_file = temp_file.name
            temp_file.write("ok")
    finally:
        if probe_file is not None:
            with suppress(OSError):
                os.unlink(probe_file)


def _prepare_output_paths(output_file, screenshot_dir):
    output_parent = os.path.dirname(os.path.abspath(output_file)) or "."
    os.makedirs(output_parent, exist_ok=True)

    if os.path.exists(screenshot_dir) and not os.path.isdir(screenshot_dir):
        raise ValueError("screenshot_dir exists and is not a directory")
    os.makedirs(screenshot_dir, exist_ok=True)

    if os.path.isdir(output_file):
        raise ValueError("output_file exists and is a directory")

    _probe_writable_dir(output_parent)
    _probe_writable_dir(screenshot_dir)

    if os.path.exists(output_file):
        os.unlink(output_file)


def _write_temp_json(data, prefix):
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        encoding="utf-8",
        prefix=prefix,
        suffix=".json",
    ) as temp_file:
        json.dump(data, temp_file)
        return temp_file.name


def _normalize_actions(actions):
    """Return JSON-serializable Playwright action specs.

    Each action must be a dictionary with a string ``method`` key. Optional
    ``args`` must be a list/tuple, optional ``kwargs`` must be a dictionary.
    Extra dictionary keys are treated as keyword arguments for convenience.
    """
    if actions is None:
        return []
    if not isinstance(actions, (list, tuple)):
        raise TypeError("actions must be a list of dictionaries")

    normalized = []
    for action in actions:
        if not isinstance(action, dict):
            raise TypeError("each action must be a dictionary")
        if "method" not in action or not isinstance(action["method"], str):
            raise ValueError("each action must include a string 'method' key")
        if action["method"] == "screenshot":
            raise ValueError(
                "actions should not include a screenshot action; "
                "crawl_screenshots adds it automatically"
            )
        args = action.get("args", [])
        kwargs = action.get("kwargs", {})
        if not isinstance(args, (list, tuple)):
            raise TypeError("action 'args' must be a list or tuple")
        if not isinstance(kwargs, dict):
            raise TypeError("action 'kwargs' must be a dictionary")
        extra_kwargs = {
            key: val
            for key, val in action.items()
            if key not in {"method", "args", "kwargs"}
        }
        merged_kwargs = dict(kwargs)
        merged_kwargs.update(extra_kwargs)
        normalized.append(
            {
                "method": action["method"],
                "args": list(args),
                "kwargs": merged_kwargs,
            }
        )
    # Verify JSON serializability early, before launching a subprocess.
    json.dumps(normalized)
    return normalized


def _load_page_method():
    module = importlib.import_module("scrapy_playwright.page")
    return module.PageMethod


def _check_screenshot_dependencies():
    if sys.version_info < (3, 10):
        raise ImportError(
            "Screenshot capturing requires Python >= 3.10 because "
            "scrapy-playwright requires Python >= 3.10."
        )
    try:
        _load_page_method()
    except ImportError as exc:
        raise ImportError(
            "Screenshot capturing requires optional dependencies. Install them with:\n"
            "    pip install 'advertools[screenshots]'\n"
            "Then install browser binaries, for example:\n"
            "    playwright install chromium"
        ) from exc


def _settings_to_cli_args(settings):
    settings_list = []
    for key, val in settings.items():
        if isinstance(val, (dict, list, set, tuple)):
            setting = "=".join([key, json.dumps(val)])
        else:
            setting = "=".join([key, str(val)])
        settings_list.extend(["-s", setting])
    return settings_list


def _default_screenshot_settings(browser_type, launch_options):
    launch_options = {"headless": True, **(launch_options or {})}
    return {
        "DOWNLOAD_HANDLERS": _DEFAULT_DOWNLOAD_HANDLERS,
        "TWISTED_REACTOR": _DEFAULT_TWISTED_REACTOR,
        "PLAYWRIGHT_BROWSER_TYPE": browser_type,
        "PLAYWRIGHT_LAUNCH_OPTIONS": launch_options,
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 4,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
    }


def _build_screenshot_command(
    output_file,
    settings_list,
    start_index=0,
    url_list=None,
    url_list_file=None,
    screenshot_options=None,
    screenshot_options_file=None,
):
    if url_list_file is None:
        url_list_arg = "url_list=" + json.dumps(url_list)
    else:
        url_list_arg = "url_list_file=" + url_list_file
    if screenshot_options_file is None:
        screenshot_options_arg = "screenshot_options=" + json.dumps(
            screenshot_options
        )
    else:
        screenshot_options_arg = "screenshot_options_file=" + screenshot_options_file
    return [
        sys.executable,
        "-m",
        "scrapy",
        "runspider",
        screenshot_spider_path,
        "-a",
        url_list_arg,
        "-a",
        screenshot_options_arg,
        "-a",
        "start_index=" + str(start_index),
        "-o",
        output_file,
    ] + settings_list


def _page_methods(actions, wait_for_timeout, screenshot_path, screenshot_options):
    PageMethod = _load_page_method()
    methods = []
    for action in actions:
        methods.append(
            PageMethod(
                action["method"],
                *action.get("args", []),
                **action.get("kwargs", {}),
            )
        )
    if wait_for_timeout is not None:
        methods.append(PageMethod("wait_for_timeout", wait_for_timeout))

    screenshot_kwargs = {
        "path": screenshot_path,
        "full_page": screenshot_options["full_page"],
        "type": screenshot_options["image_type"],
    }
    if screenshot_options["quality"] is not None:
        screenshot_kwargs["quality"] = screenshot_options["quality"]
    if screenshot_options["timeout"] is not None:
        screenshot_kwargs["timeout"] = screenshot_options["timeout"]
    methods.append(PageMethod("screenshot", **screenshot_kwargs))
    return methods


def _screenshot_file_info(screenshot_path):
    exists = bool(screenshot_path) and os.path.exists(screenshot_path)
    size = os.path.getsize(screenshot_path) if exists else 0
    return {
        "screenshot_success": exists and size > 0,
        "screenshot_exists": exists,
        "screenshot_size_bytes": size,
    }


def _exception_error_fields(exception):
    return {
        "errors": repr(exception),
        "error_type": type(exception).__name__,
        "error_message": str(exception),
    }


def _failure_error_fields(failure):
    exception = getattr(failure, "value", None)
    if exception is None:
        return {
            "errors": repr(failure),
            "error_type": type(failure).__name__,
            "error_message": str(failure),
        }
    return {
        "errors": repr(failure),
        "error_type": type(exception).__name__,
        "error_message": str(exception),
    }


def _safe_meta(meta):
    return {
        key: "@@".join(str(val) for val in value)
        if isinstance(value, list)
        else value
        for key, value in meta.items()
        if key not in _INTERNAL_META_KEYS and not key.startswith("playwright_")
    }


class ScreenshotSpider(Spider):
    name = "screenshot_spider"
    custom_settings = {
        "USER_AGENT": user_agent,
        "ROBOTSTXT_OBEY": True,
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_HANDLERS": _DEFAULT_DOWNLOAD_HANDLERS,
        "TWISTED_REACTOR": _DEFAULT_TWISTED_REACTOR,
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 4,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
    }

    def __init__(
        self,
        url_list=None,
        url_list_file=None,
        screenshot_options=None,
        screenshot_options_file=None,
        start_index=0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if url_list_file is not None:
            with open(url_list_file, encoding="utf-8") as urls_file:
                self.start_urls = json.load(urls_file)
        else:
            self.start_urls = json.loads(url_list or "[]")
        if screenshot_options_file is not None:
            with open(screenshot_options_file, encoding="utf-8") as options_file:
                self.screenshot_options = json.load(options_file)
        else:
            self.screenshot_options = json.loads(screenshot_options or "{}")
        self.start_index = int(start_index)
        self.context_name = "advertools_screenshots_" + _safe_filename_part(
            self.screenshot_options.get("run_id"), max_length=40
        )

    def _request_meta(self, url, index, screenshot_path):
        screenshot_options = self.screenshot_options
        goto_kwargs = {"wait_until": screenshot_options["wait_until"]}
        if screenshot_options["timeout"] is not None:
            goto_kwargs["timeout"] = screenshot_options["timeout"]
        meta = {
            "playwright": True,
            "playwright_page_goto_kwargs": goto_kwargs,
            "playwright_page_methods": _page_methods(
                screenshot_options["actions"],
                screenshot_options["wait_for_timeout"],
                screenshot_path,
                screenshot_options,
            ),
            "screenshot_path": screenshot_path,
            "screenshot_type": screenshot_options["image_type"],
            "run_id": screenshot_options["run_id"],
            "screenshot_index": index,
        }
        if screenshot_options.get("context_kwargs"):
            meta.update(
                {
                    "playwright_context": self.context_name,
                    "playwright_context_kwargs": screenshot_options["context_kwargs"],
                }
            )
        return meta

    def _start_requests(self):
        for index, url in enumerate(self.start_urls, self.start_index):
            screenshot_path = _screenshot_path(
                url,
                index,
                self.screenshot_options["screenshot_dir"],
                self.screenshot_options["run_id"],
                self.screenshot_options["image_type"],
            )
            try:
                yield Request(
                    url,
                    callback=self.parse,
                    errback=self.errback,
                    meta=self._request_meta(url, index, screenshot_path),
                )
            except Exception as e:
                self.logger.error(repr(e))
                yield {
                    "url": url,
                    "final_url": None,
                    "status": None,
                    "screenshot_path": screenshot_path,
                    "screenshot_type": self.screenshot_options["image_type"],
                    "run_id": self.screenshot_options["run_id"],
                    "screenshot_index": index,
                    "crawl_time": _now(),
                    **_screenshot_file_info(screenshot_path),
                    **_exception_error_fields(e),
                }

    def start_requests(self):
        yield from self._start_requests()

    async def start(self):
        for request in self._start_requests():
            yield request

    def errback(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        screenshot_path = request.meta.get("screenshot_path")
        yield {
            "url": request.url,
            "final_url": None,
            "status": None,
            "screenshot_path": screenshot_path,
            "screenshot_type": request.meta.get("screenshot_type"),
            "run_id": request.meta.get("run_id"),
            "screenshot_index": request.meta.get("screenshot_index"),
            "crawl_time": _now(),
            **_screenshot_file_info(screenshot_path),
            **_failure_error_fields(failure),
        }

    def parse(self, response):
        screenshot_path = response.meta.get("screenshot_path")
        yield {
            "url": response.request.url,
            "final_url": response.url,
            "crawl_time": _now(),
            "status": response.status,
            "screenshot_path": screenshot_path,
            "screenshot_type": response.meta.get("screenshot_type"),
            "run_id": response.meta.get("run_id"),
            "screenshot_index": response.meta.get("screenshot_index"),
            **_screenshot_file_info(screenshot_path),
            "error_type": None,
            "error_message": None,
            "protocol": response.protocol,
            **_safe_meta(response.meta),
            **{
                "resp_headers_" + k: v
                for k, v in response.headers.to_unicode_dict().items()
            },
            **{
                "request_headers_" + k: v
                for k, v in response.request.headers.to_unicode_dict().items()
            },
        }


def crawl_screenshots(
    url_list,
    output_file,
    screenshot_dir=None,
    *,
    full_page=True,
    image_type="png",
    quality=None,
    wait_until="load",
    wait_for_timeout=None,
    actions=None,
    browser_type="chromium",
    launch_options=None,
    context_kwargs=None,
    custom_settings=None,
    timeout=None,
    run_id=None,
):
    """Capture screenshots for a list of URLs.

    Parameters
    ----------
    url_list : str, list
      One or more URLs to capture. This function does not discover or follow links.
    output_file : str
      Path to the JSON Lines metadata output. Must end with ``.jl`` or ``.jsonl``.
      Replaced on every run.
    screenshot_dir : str
      Directory where screenshots are saved. Defaults to
      ``<output_file_stem>_screenshots``.
    full_page : bool
      Whether to capture the full scrollable page.
    image_type : str
      Screenshot format: ``"png"`` or ``"jpeg"``.
    quality : int
      JPEG quality between 0 and 100. Only valid with ``image_type="jpeg"``.
    wait_until : str
      Playwright navigation wait condition: ``load``, ``domcontentloaded``,
      ``networkidle``, or ``commit``.
    wait_for_timeout : int, float
      Optional milliseconds to wait after custom actions and before screenshot.
    actions : list
      Optional serializable Playwright page actions. Each action is a dict with
      ``method`` plus optional ``args`` and ``kwargs``.
    browser_type : str
      Playwright browser type: typically ``chromium``, ``firefox``, or ``webkit``.
    launch_options : dict
      Playwright launch options; merged with ``{"headless": True}``.
    context_kwargs : dict
      Browser context keyword arguments, such as viewport settings.
    custom_settings : dict
      Additional Scrapy settings. These override screenshot capture defaults.
    timeout : int, float
      Optional Playwright timeout in milliseconds for navigation and screenshot
      operations.
    run_id : str
      Identifier included in screenshot filenames and metadata. Defaults to a
      UTC timestamp.

    Returns
    -------
    None
      Writes a JSON Lines metadata file. Successful rows include screenshot
      success fields such as ``screenshot_success``, ``screenshot_exists``, and
      ``screenshot_size_bytes``. Failed rows include ``errors``, ``error_type``,
      and ``error_message``.
    """
    url_list = _normalize_url_list(url_list)
    output_file = _validate_output_file(output_file)
    image_type = _validate_screenshot_options(
        image_type, quality, wait_until, wait_for_timeout, timeout
    )
    actions = _normalize_actions(actions)
    if screenshot_dir is None:
        screenshot_dir = output_file.rsplit(".", maxsplit=1)[0] + "_screenshots"
    else:
        screenshot_dir = os.fspath(screenshot_dir)
    if run_id is None:
        run_id = _default_run_id()
    else:
        run_id = _safe_filename_part(run_id, max_length=40)
    if context_kwargs is None:
        context_kwargs = {}
    if not isinstance(context_kwargs, dict):
        raise TypeError("context_kwargs must be a dictionary")
    if launch_options is not None and not isinstance(launch_options, dict):
        raise TypeError("launch_options must be a dictionary")
    if custom_settings is not None and not isinstance(custom_settings, dict):
        raise TypeError("custom_settings must be a dictionary")
    if browser_type not in {"chromium", "firefox", "webkit"}:
        raise ValueError("browser_type must be one of: chromium, firefox, webkit")

    _check_screenshot_dependencies()
    _prepare_output_paths(output_file, screenshot_dir)

    screenshot_options = {
        "screenshot_dir": screenshot_dir,
        "run_id": run_id,
        "full_page": bool(full_page),
        "image_type": image_type,
        "quality": quality,
        "wait_until": wait_until,
        "wait_for_timeout": wait_for_timeout,
        "timeout": timeout,
        "actions": actions,
        "context_kwargs": context_kwargs,
    }

    settings = _default_screenshot_settings(browser_type, launch_options)
    if custom_settings is not None:
        settings.update(custom_settings)
    settings_list = _settings_to_cli_args(settings)

    temp_files = []

    try:
        url_list_file = _write_temp_json(
            url_list, "advertools_screenshot_urls_"
        )
        screenshot_options_file = _write_temp_json(
            screenshot_options, "advertools_screenshot_options_"
        )
        temp_files.extend([url_list_file, screenshot_options_file])
        command = _build_screenshot_command(
            output_file,
            settings_list,
            url_list_file=url_list_file,
            screenshot_options_file=screenshot_options_file,
        )
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "Screenshot capture failed with exit code {returncode}.\n"
            "Browser type: {browser_type}\n"
            "Output file: {output_file}\n"
            "Screenshot directory: {screenshot_dir}\n"
            "Make sure screenshot dependencies and browser binaries are "
            "installed:\n"
            "    pip install 'advertools[screenshots]'\n"
            "    {python} -m playwright install {browser_type}\n"
            "For Chromium specifically:\n"
            "    {python} -m playwright install chromium".format(
                returncode=e.returncode,
                browser_type=browser_type,
                output_file=output_file,
                screenshot_dir=screenshot_dir,
                python=sys.executable,
            )
        ) from e
    finally:
        for temp_file in temp_files:
            with suppress(OSError):
                os.unlink(temp_file)
