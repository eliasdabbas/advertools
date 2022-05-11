"""
convert a robots.txt file (or list of file URLs) to a table in a CSV format
============================================================================


    usage: ``advertools robots [-h] [url ...]``

    convert a robots.txt file (or list of file URLs) to a table in a CSV format

    you can provide a web URL, or a local file URL on your local machine
    e.g. file:///Users/path/to/robots.txt

    examples:
    ---------

    advertools robots https://www.google.com/robots.txt

    multiple robots files:

    advertools robots https://www.google.com/robots.txt https://www.google.jo/robots.txt  https://www.google.es/robots.txt

    use output redirection ">" to save to a CSV file:

    advertools robots https://www.google.com/robots.txt > google_robots.csv

    run the function for a long list of robots files saved in a text file (robotslist.txt):

    advertools robots < robotslist.txt > multi_robots.csv

    positional arguments:
      url         a robots.txt URL (or a list of URLs) (default: None)

    optional arguments:
      -h, --help  show this help message and exit


download, parse, and save an XML sitemap to a table in a CSV file
==================================================================


    usage: ``advertools sitemaps [-h] [-r {0,1}] [-s SEPARATOR] [sitemap_url]``

    download, parse, and save an XML sitemap to a table in a CSV file

    positional arguments:
      sitemap_url           the URL of the XML sitemap (regular or sitemap index) (default: None)

    optional arguments:
      -h, --help            show this help message and exit
      -r {0,1}, --recursive {0,1}
                            whether or not to fetch sub-sitemaps if it is a sitemap index file (default: 1)
      -s SEPARATOR, --separator SEPARATOR
                            the separator with which to separate columns of the output (default: ,)


split a list of URLs into their components: scheme, netloc, path, query, etc.
==============================================================================


    usage: ``advertools urls [-h] [url_list ...]``

    split a list of URLs into their components: scheme, netloc, path, query, etc.

    positional arguments:
      url_list    a list of URLs to parse (default: None)

    optional arguments:
      -h, --help  show this help message and exit


crawl a list of known URLs using the HEAD method
=================================================


    usage: ``advertools headers [-h] [-s [CUSTOM_SETTINGS ...]] [url_list ...] output_file``

    crawl a list of known URLs using the HEAD method
    return status codes and all available response headers

    positional arguments:
      url_list              a list of URLs (default: None)
      output_file           filepath - where to save the output (.jl)

    optional arguments:
      -h, --help            show this help message and exit
      -s [CUSTOM_SETTINGS ...], --custom-settings [CUSTOM_SETTINGS ...]
                            settings that modify the behavior of the crawler
                            settings should be separated by spaces, and each setting name and value should
                            be separated by an equal sign '=' without spaces between them
                            
                            example:
                            
                            advertools headers https://example.com example.jl --custom-settings LOG_FILE=logs.log CLOSESPIDER_TIMEOUT=20
                             (default: None)


parse, compress and convert a log file to a DataFrame in the .parquet format
=============================================================================


    usage: ``advertools logs [-h] [-f [FIELDS ...]] log_file output_file errors_file log_format``

    parse, compress and convert a log file to a DataFrame in the .parquet format

    positional arguments:
      log_file              filepath - the log file
      output_file           filepath - where to save the output (.parquet)
      errors_file           filepath - where to save the error lines (.txt)
      log_format            the format of the logs, available defaults are:
                                common, combined, common_with_vhost, nginx_error, apache_error
                                supply a special regex instead if you have a different format

    optional arguments:
      -h, --help            show this help message and exit
      -f [FIELDS ...], --fields [FIELDS ...]
                            in case you have a special log format, provide a list of the fields names
                            which will become column names in the parsed compressed file (default: None)


perform a reverse DNS lookup on a list of IP addresses
=======================================================


    usage: ``advertools dns [-h] [ip_list ...]``

    perform a reverse DNS lookup on a list of IP addresses

    positional arguments:
      ip_list     a list of IP addresses (default: None)

    optional arguments:
      -h, --help  show this help message and exit


generate a table of SEM keywords by supplying a list of products and a list of intent words
============================================================================================


    usage: ``advertools semkw [-h] [-t [{exact,phrase,modified,broad} ...]] [-l MAX_LEN] [-c {0,1}] [-m {0,1}] [-n CAMPAIGN_NAME] products words``

    generate a table of SEM keywords by supplying a list of products and a list of intent words

    positional arguments:
      products              a file containing the products that you sell, one per line
      words                 a file containing the intent words/phrases that you want to combine with products, one per line

    optional arguments:
      -h, --help            show this help message and exit
      -t [{exact,phrase,modified,broad} ...], --match-types [{exact,phrase,modified,broad} ...]
      -l MAX_LEN, --max-len MAX_LEN
                            the number of words that should be combined with products (default: 3)
      -c {0,1}, --capitalize-adgroups {0,1}
                            whether or not to capitalize ad group names in the output file (default: 1)
      -m {0,1}, --order-matters {0,1}
                            do you want combinations and permutations, or just combinations?
                            "buy product" and "product buy" or just "buy product"? (default: 1)
      -n CAMPAIGN_NAME, --campaign-name CAMPAIGN_NAME


get stopwords of the selected language
=======================================


    usage: ``advertools stopwords [-h] {arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}``

    get stopwords of the selected language

    positional arguments:
      {arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}

    optional arguments:
      -h, --help            show this help message and exit


get word counts of a text list optionally weighted by a number list
====================================================================


    usage: ``advertools wordfreq [-h] [-n NUMBER_LIST] [-r REGEX] [-l PHRASE_LEN] [-s [STOPWORDS ...]] [text_list ...]``

    get word counts of a text list optionally weighted by a number list

    words (tokens) can be tokenized using any pattern with the --regex option
    word/phrase lengths can also be modified using the --phrase-len option

    positional arguments:
      text_list             a text list, one document (sentence, tweet, etc.) per line (default: None)

    optional arguments:
      -h, --help            show this help message and exit
      -n NUMBER_LIST, --number-list NUMBER_LIST
                            filepath - a file containing the number list, one number per line (default: None)
      -r REGEX, --regex REGEX
                            a regex to tokenize words (default: None)
      -l PHRASE_LEN, --phrase-len PHRASE_LEN
                            the phrase (token) length to split words (the `n` in n-grams) (default: 1)
      -s [STOPWORDS ...], --stopwords [STOPWORDS ...]
                            a list of stopwords to exclude when counting, defaults to English stopwords
                            run `advertools stopwords english` to get the stopwords
                            change the language to get other stopwords (default: None)


search for emoji using a regex
===============================


    usage: ``advertools emoji [-h] regex``

    search for emoji using a regex

    positional arguments:
      regex       pattern to search for emoji

    optional arguments:
      -h, --help  show this help message and exit


extract structured entities from a text list; emoji, hashtags, mentions
========================================================================


    usage: ``advertools extract [-h] {emoji,hashtags,mentions} text_list``

    extract structured entities from a text list; emoji, hashtags, mentions

    positional arguments:
      {emoji,hashtags,mentions}
                            which entity you want to extract
      text_list             filepath - a file containing the text list, one phrase per line

    optional arguments:
      -h, --help            show this help message and exit


tokenize documents (phrases, keywords, tweets, etc) into token of the desired length
=====================================================================================


    usage: ``advertools tokenize [-h] [-l LENGTH] [-s SEPARATOR] [text_list ...]``

    tokenize documents (phrases, keywords, tweets, etc) into token of the desired length

    positional arguments:
      text_list             filepath - a file containing the text list, one document (sentence, tweet, etc.) per line (default: None)

    optional arguments:
      -h, --help            show this help message and exit
      -l LENGTH, --length LENGTH
                            the length of tokens (the n in n-grams) (default: 1)
      -s SEPARATOR, --separator SEPARATOR
                            the character with which to separate the tokens (default: ,)


SEO crawler
============


    usage: advertools crawl [-h] [-l FOLLOW_LINKS] [-d [ALLOWED_DOMAINS ...]]
                            [--exclude-url-params [EXCLUDE_URL_PARAMS ...]]
                            [--include-url-params [INCLUDE_URL_PARAMS ...]]
                            [--exclude-url-regex EXCLUDE_URL_REGEX]
                            [--include-url-regex INCLUDE_URL_REGEX]
                            [--css-selectors [CSS_SELECTORS ...]]
                            [--xpath-selectors [XPATH_SELECTORS ...]]
                            [--custom-settings [CUSTOM_SETTINGS ...]]
                            [url_list ...] output_file

    SEO crawler

    positional arguments:
      url_list              one or more URLs to crawl (default: None)
      output_file           filepath - where to save the output (.jl)

    optional arguments:
      -h, --help            show this help message and exit
      -l FOLLOW_LINKS, --follow-links FOLLOW_LINKS
                            whether or not to follow links encountered on crawled pages (default: 0)
      -d [ALLOWED_DOMAINS ...], --allowed-domains [ALLOWED_DOMAINS ...]
                            while following links, only links on these domains will be followed (default: None)
      --exclude-url-params [EXCLUDE_URL_PARAMS ...]
                            a list of URL parameters to exclude while following links
                            if a link contains any of those parameters, don't follow it
                            setting it to True will exclude links containing any parameter (default: None)
      --include-url-params [INCLUDE_URL_PARAMS ...]
                            a list of URL parameters to include while following links
                            if a link contains any of those parameters, follow it
                            having the same parmeters to include and exclude raises an error (default: None)
      --exclude-url-regex EXCLUDE_URL_REGEX
                            a regular expression of a URL pattern to exclude while following links
                            if a link matches the regex don't follow it (default: None)
      --include-url-regex INCLUDE_URL_REGEX
                            a regular expression of a URL pattern to include while following links
                            if a link matches the regex follow it (default: None)
      --css-selectors [CSS_SELECTORS ...]
                            a dictionary mapping names to CSS selectors
                            the names will become column headers, and the selectors will be used to extract the required data/content (default: None)
      --xpath-selectors [XPATH_SELECTORS ...]
                            a dictionary mapping names to XPath selectors.
                            the names will become column headers, and the selectors will be used to extract the required data/content (default: None)
      --custom-settings [CUSTOM_SETTINGS ...]
                            a dictionary of optional custom settings that you might want to
                            add to the spider's functionality.
                            there are over 170 settings for all kinds of options
                            for details please refer to the spider settings:
                            https://docs.scrapy.org/en/latest/topics/settings.html (default: None)

    Examples:
    ---------

    crawl a website starting from its home page:

    advertools crawl https://examle.com example_output.jl --follow-links 1

    crawl a list of pages (list mode):

    advertools crawl url_1 url_2 url_3 example_output.jl

    OR if you have a long list in a file (url_list.txt):

    advertools crawl < url_list.txt example_output.jl

    stop crawling after having processed 1,000 pages:

    advertools crawl https://examle.com example_output.jl --follow-links 1 --custom-settings CLOSESPIDER_PAGECOUNT=1000

"""
