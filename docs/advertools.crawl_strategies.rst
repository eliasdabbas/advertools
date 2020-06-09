Crawl Strategies and Tips
=========================

Here are some options to consider while running your crawls.


CSS Selectors
-------------
This is a set of selectors that you might be interested in using depending on
what you are crawling.

* **Canonical tags**: This code will crawl example.com, starting from the home
  page, and following links. In addition to the standard columns, it will
  create an additional column called "canonical", the value of which will be
  the `href` attribute of the canonical elements.

.. code-block:: python

   crawl('http://example.com', 'output_file.csv', follow_links=True,
         css_selectors={'canonical': '[rel=canonical]::attr(href)'})


* **Alternate tags**: Similarly, you can get `alternate` tags. Here we extract
  two attributes `href` and `hreflang`, and have each in a separate column, one
  for the link, and the other for the languages indicated in that link.

.. code-block:: python

   crawl('http://example.com', 'output_file.csv', follow_links=True,
         css_selectors={'alt_href': '[rel=alternate]::attr(href)',
                        'alt_hreflang': '[rel=alternate]::attr(hreflang)'})

* **Meta robots**: Some pages include special rules for robots on the page for
  how/to follow, index, etc. Typically, you would have

.. code-block:: html

   <meta name="robots" content="nofollow, noindex">

.. code-block:: python

   crawl('http://example.com', 'output_file.csv', follow_links=True,
         css_selectors={'alt_href': '[rel=alternate]::attr(href)',
                        'alt_hreflang': '[rel=alternate]::attr(hreflang)'})
