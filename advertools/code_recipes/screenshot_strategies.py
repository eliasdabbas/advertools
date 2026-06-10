"""
.. _screenshot_strategies:

📸 Screenshot Capturing: Strategies & Recipes
======================================================

The :func:`advertools.crawl_screenshots` function saves page screenshots for a
known list of URLs and writes a JSON Lines metadata file that can be loaded with
pandas. This is useful for visual QA, archiving what a page looked like when it
was crawled, checking JavaScript-rendered pages, or comparing desktop and mobile
rendering.

Screenshot capturing uses the optional ``scrapy-playwright`` integration. Install
it and at least one browser before running these examples::

    pip install "advertools[screenshots]"
    playwright install chromium

Screenshot metadata files in these recipes are written under the local
``screenshots/`` folder next to this recipe module. That folder is ignored by
git and is intended for local experiments. Metadata output files are replaced on
every run.

How do I capture screenshots for a list of URLs?
************************************************

Provide the URLs, the metadata output file, and optionally the screenshot
folder. The output file contains one row per URL with the final URL, status,
screenshot path, headers, and crawl time.

.. code-block:: python

    >>> import advertools as adv
    >>> import pandas as pd

    >>> adv.crawl_screenshots(
    ...     ["https://example.com", "https://www.python.org"],
    ...     "screenshots/basic.jl",
    ...     screenshot_dir="screenshots/images",
    ... )

    >>> screenshot_df = pd.read_json("screenshots/basic.jl", lines=True)
    >>> screenshot_df[["url", "status", "screenshot_path"]]

How can I capture JPEG screenshots instead of PNG?
**************************************************

Use ``image_type="jpeg"`` and optionally set ``quality``. The ``quality``
parameter is only valid for JPEG screenshots.

.. code-block:: python

    >>> adv.crawl_screenshots(
    ...     "https://example.com",
    ...     "screenshots/jpeg.jl",
    ...     screenshot_dir="screenshots/jpeg_images",
    ...     image_type="jpeg",
    ...     quality=80,
    ... )

How can I capture only the viewport?
************************************

By default, screenshots are full-page screenshots. Set ``full_page=False`` to
capture only the browser viewport.

.. code-block:: python

    >>> adv.crawl_screenshots(
    ...     "https://example.com",
    ...     "screenshots/viewport.jl",
    ...     full_page=False,
    ... )

How can I emulate a mobile viewport?
************************************

Pass browser context options with ``context_kwargs``. Playwright supports many
context settings; viewport and device scale factor are common for visual QA.

.. code-block:: python

    >>> adv.crawl_screenshots(
    ...     "https://example.com",
    ...     "screenshots/mobile.jl",
    ...     screenshot_dir="screenshots/mobile_images",
    ...     full_page=True,
    ...     context_kwargs={
    ...         "viewport": {"width": 390, "height": 844},
    ...         "device_scale_factor": 2,
    ...         "is_mobile": True,
    ...     },
    ... )

How can I wait for content before taking the screenshot?
********************************************************

Use ``wait_until`` to control the navigation wait condition and
``wait_for_timeout`` to wait a fixed number of milliseconds after navigation and
actions. This can help with pages that load content after the initial HTML.

.. code-block:: python

    >>> adv.crawl_screenshots(
    ...     "https://example.com",
    ...     "screenshots/waited.jl",
    ...     wait_until="networkidle",
    ...     wait_for_timeout=1000,
    ...     timeout=10000,
    ... )

How can I scroll, click, or wait for selectors before the screenshot?
*********************************************************************

Use ``actions`` to run serializable Playwright page methods before the screenshot
is taken. Each action is a dictionary with a ``method`` and optional ``args`` /
``kwargs``. The screenshot action is added automatically, so don't include it in
``actions``.

.. code-block:: python

    >>> adv.crawl_screenshots(
    ...     "https://example.com",
    ...     "screenshots/actions.jl",
    ...     actions=[
    ...         {"method": "wait_for_selector", "args": ["body"]},
    ...         {
    ...             "method": "evaluate",
    ...             "args": ["window.scrollTo(0, document.body.scrollHeight)"],
    ...         },
    ...         {"method": "wait_for_timeout", "args": [1000]},
    ...     ],
    ... )

How can I compare desktop and mobile screenshots?
*************************************************

Run two screenshot capture jobs with the same URL list and different ``run_id`` and
``context_kwargs`` values. The ``run_id`` is included in screenshot filenames and
metadata, which makes it easy to join or compare results later.

.. code-block:: python

    >>> urls = ["https://example.com", "https://www.python.org"]

    >>> adv.crawl_screenshots(
    ...     urls,
    ...     "screenshots/desktop.jl",
    ...     screenshot_dir="screenshots/desktop_images",
    ...     run_id="desktop",
    ... )

    >>> adv.crawl_screenshots(
    ...     urls,
    ...     "screenshots/mobile_compare.jl",
    ...     screenshot_dir="screenshots/mobile_compare_images",
    ...     run_id="mobile",
    ...     context_kwargs={
    ...         "viewport": {"width": 390, "height": 844},
    ...         "is_mobile": True,
    ...     },
    ... )

How can I use the command line?
*******************************

The ``screenshots`` command mirrors the Python API. It accepts URLs as arguments
or from standard input. JSON flags can be inline JSON or ``@file.json``. Using
JSON files avoids shell quoting issues in fish, zsh, and bash.

.. code-block:: console

    advertools screenshots https://example.com https://www.python.org \
        screenshots/basic.jl --screenshot-dir screenshots/images

    advertools screenshots https://www.python.org screenshots/mobile.jl \
        --screenshot-dir screenshots/mobile_images \
        --context-kwargs-json @screenshots/mobile-context.json

"""
