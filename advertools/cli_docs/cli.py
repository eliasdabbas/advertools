"""
Convert a robots.txt file (or list of file URLs) to a table in a CSV format
=============================================================================

**Usage**
---------

.. code-block:: console

    advertools robots [-h] [url ...]

Convert a robots.txt file (or list of file URLs) to a table in a CSV format.

You can provide a web URL, or a local file URL on your local machine, for example:

``file:///Users/path/to/robots.txt``

**Examples**
------------

Single robots.txt file:

.. code-block:: console

    advertools robots https://www.google.com/robots.txt

Multiple robots.txt files:

.. code-block:: console

    advertools robots https://www.google.com/robots.txt https://www.google.jo/robots.txt https://www.google.es/robots.txt

Save to a CSV file using output redirection:

.. code-block:: console

    advertools robots https://www.google.com/robots.txt > google_robots.csv

Run the function for a long list of robots files saved in a text file (robotslist.txt):

.. code-block:: console

    advertools robots < robotslist.txt > multi_robots.csv

**Arguments**
-------------

**Positional arguments:**

- **url**: A robots.txt URL (or a list of URLs). Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Download, parse, and save an XML sitemap to a table in a CSV file
==================================================================

**Usage**
---------

.. code-block:: console

    advertools sitemaps [-h] [-r {0,1}] [-s SEPARATOR] [sitemap_url]

**Positional arguments:**

- **sitemap_url**: The URL of the XML sitemap (regular or sitemap index). Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-r {0,1}, --recursive {0,1}**: Whether or not to fetch sub-sitemaps if it is a sitemap index file. Default: 1.
- **-s SEPARATOR, --separator SEPARATOR**: The separator with which to separate columns of the output. Default: `,`.

Split a list of URLs into their components: scheme, netloc, path, query, etc.
==============================================================================

**Usage**
---------

.. code-block:: console

    advertools urls [-h] [url_list ...]

**Positional arguments:**

- **url_list**: A list of URLs to parse. Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Crawl a list of known URLs using the HEAD method
=================================================

**Usage**
---------

.. code-block:: console

    advertools headers [-h] [-s [CUSTOM_SETTINGS ...]] [url_list ...] output_file

**Positional arguments:**

- **url_list**: A list of URLs. Default: None.
- **output_file**: Filepath - where to save the output (.jl).

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-s [CUSTOM_SETTINGS ...], --custom-settings [CUSTOM_SETTINGS ...]**: Settings that modify the behavior of the crawler.
  Settings should be separated by spaces, and each setting name and value should be separated by an equal sign `=` without spaces between them.

**Example:**

.. code-block:: console

    advertools headers https://example.com example.jl --custom-settings LOG_FILE=logs.log CLOSESPIDER_TIMEOUT=20

Parse, compress and convert a log file to a DataFrame in the .parquet format
=============================================================================

**Usage**
---------

.. code-block:: console

    advertools logs [-h] [-f [FIELDS ...]] log_file output_file errors_file log_format

**Positional arguments:**

- **log_file**: Filepath - the log file.
- **output_file**: Filepath - where to save the output (.parquet).
- **errors_file**: Filepath - where to save the error lines (.txt).
- **log_format**: The format of the logs. Available defaults are: common, combined, common_with_vhost, nginx_error, apache_error. Supply a special regex instead if you have a different format.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-f [FIELDS ...], --fields [FIELDS ...]**: Provide a list of field names to become column names in the parsed compressed file. Default: None.


Perform a reverse DNS lookup on a list of IP addresses
======================================================

**Usage**
---------

.. code-block:: console

    advertools dns [-h] [ip_list ...]

**Description**
---------------

Perform a reverse DNS lookup on a list of IP addresses.

**Positional arguments:**

- **ip_list**: A list of IP addresses. Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Generate a table of SEM keywords by supplying a list of products and a list of intent words
===========================================================================================

**Usage**
---------

.. code-block:: console

    advertools semkw [-h] [-t [{exact,phrase,modified,broad} ...]] [-l MAX_LEN] [-c {0,1}] [-m {0,1}] [-n CAMPAIGN_NAME] products words

**Description**
---------------

Generate a table of SEM keywords by supplying a list of products and a list of intent words.

**Positional arguments:**

- **products**: A file containing the products that you sell, one per line.
- **words**: A file containing the intent words/phrases that you want to combine with products, one per line.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-t [{exact,phrase,modified,broad} ...]**: Specify match types.
- **-l MAX_LEN, --max-len MAX_LEN**: Number of words to combine with products. Default: 3.
- **-c {0,1}, --capitalize-adgroups {0,1}**: Whether or not to capitalize ad group names in the output file. Default: 1.
- **-m {0,1}, --order-matters {0,1}**: Use combinations and permutations, or just combinations. Default: 1.
- **-n CAMPAIGN_NAME, --campaign-name CAMPAIGN_NAME**: The campaign name.

Get stopwords of the selected language
=======================================

**Usage**
---------

.. code-block:: console

    advertools stopwords [-h] {arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}

**Description**
---------------

Get stopwords of the selected language.

**Positional arguments:**

- **{arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}**: The language to retrieve stopwords for.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Get word counts of a text list optionally weighted by a number list
====================================================================

**Usage**
---------

.. code-block:: console

    advertools wordfreq [-h] [-n NUMBER_LIST] [-r REGEX] [-l PHRASE_LEN] [-s [STOPWORDS ...]] [text_list ...]

**Description**
---------------

Get word counts of a text list optionally weighted by a number list.

**Positional arguments:**

- **text_list**: A text list, one document (sentence, tweet, etc.) per line. Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-n NUMBER_LIST, --number-list NUMBER_LIST**: Filepath for a file containing the number list, one number per line. Default: None.
- **-r REGEX, --regex REGEX**: A regex to tokenize words. Default: None.
- **-l PHRASE_LEN, --phrase-len PHRASE_LEN**: The phrase (token) length to split words (the `n` in n-grams). Default: 1.
- **-s [STOPWORDS ...], --stopwords [STOPWORDS ...]**: A list of stopwords to exclude. Default: None.

Search for emoji using a regex
===============================

**Usage**
---------

.. code-block:: console

    advertools emoji [-h] regex

**Description**
---------------

Search for emoji using a regex.

**Positional arguments:**

- **regex**: Pattern to search for emoji.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Extract structured entities from a text list; emoji, hashtags, mentions
========================================================================

**Usage**
---------

.. code-block:: console

    advertools extract [-h] {emoji,hashtags,mentions} text_list

**Description**
---------------

Extract structured entities from a text list; emoji, hashtags, mentions.

**Positional arguments:**

- **{emoji,hashtags,mentions}**: Entity type to extract.
- **text_list**: Filepath containing the text list, one phrase per line.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.

Tokenize documents (phrases, keywords, tweets, etc.) into tokens of the desired length
======================================================================================

**Usage**
---------

.. code-block:: console

    advertools tokenize [-h] [-l LENGTH] [-s SEPARATOR] [text_list ...]

**Description**
---------------

Tokenize documents (phrases, keywords, tweets, etc.) into tokens of the desired length.

**Positional arguments:**

- **text_list**: Filepath containing the text list, one document (sentence, tweet, etc.) per line. Default: None.

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-l LENGTH, --length LENGTH**: Length of tokens (the `n` in n-grams). Default: 1.
- **-s SEPARATOR, --separator SEPARATOR**: Character to separate the tokens. Default: `,`.

SEO crawler
============

**Usage**
---------

.. code-block:: console

    advertools crawl [-h] [-l FOLLOW_LINKS] [-d [ALLOWED_DOMAINS ...]]
                     [--exclude-url-params [EXCLUDE_URL_PARAMS ...]]
                     [--include-url-params [INCLUDE_URL_PARAMS ...]]
                     [--exclude-url-regex EXCLUDE_URL_REGEX]
                     [--include-url-regex INCLUDE_URL_REGEX]
                     [--css-selectors [CSS_SELECTORS ...]]
                     [--xpath-selectors [XPATH_SELECTORS ...]]
                     [--custom-settings [CUSTOM_SETTINGS ...]]
                     [url_list ...] output_file

**Description**
---------------

SEO crawler to extract and collect information from web pages.

**Positional arguments:**

- **url_list**: One or more URLs to crawl. Default: None.
- **output_file**: Filepath where to save the output (.jl).

**Optional arguments:**

- **-h, --help**: Show this help message and exit.
- **-l FOLLOW_LINKS, --follow-links FOLLOW_LINKS**: Whether or not to follow links encountered on crawled pages. Default: 0.
- **-d [ALLOWED_DOMAINS ...], --allowed-domains [ALLOWED_DOMAINS ...]**: Only follow links on these domains while crawling. Default: None.
- **--exclude-url-params [EXCLUDE_URL_PARAMS ...]**: List of URL parameters to exclude while following links. If a link contains any of these parameters, it will not be followed. Default: None.
- **--include-url-params [INCLUDE_URL_PARAMS ...]**: List of URL parameters to include while following links. If a link contains any of these parameters, it will be followed. Default: None.
- **--exclude-url-regex EXCLUDE_URL_REGEX**: A regular expression pattern to exclude certain URLs from being followed. Default: None.
- **--include-url-regex INCLUDE_URL_REGEX**: A regular expression pattern to include certain URLs to be followed. Default: None.
- **--css-selectors [CSS_SELECTORS ...]**: A dictionary mapping column names to CSS selectors. The selectors will be used to extract the required data/content. Default: None.
- **--xpath-selectors [XPATH_SELECTORS ...]**: A dictionary mapping column names to XPath selectors. The selectors will be used to extract the required data/content. Default: None.
- **--custom-settings [CUSTOM_SETTINGS ...]**: Custom settings to modify the behavior of the crawler. Over 170 settings are available for configuration. See Scrapy documentation for details: https://docs.scrapy.org/en/latest/topics/settings.html. Default: None.

**Examples**
------------

Crawl a website starting from its homepage:

.. code-block:: console

    advertools crawl https://example.com example_output.jl --follow-links 1

Crawl a list of pages in list mode:

.. code-block:: console

    advertools crawl url_1 url_2 url_3 example_output.jl

If you have a long list of URLs in a file (url_list.txt):

.. code-block:: console

    advertools crawl < url_list.txt example_output.jl

Stop crawling after processing 1,000 pages:

.. code-block:: console

    advertools crawl https://example.com example_output.jl --follow-links 1 --custom-settings CLOSESPIDER_PAGECOUNT=1000

"""
