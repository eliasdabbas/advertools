# ruff: noqa: E501
"""
convert a robots.txt file (or list of file URLs) to a table in a CSV format
============================================================================


    usage: advertools robots [-h] [url ...]
    
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


    usage: advertools sitemaps [-h] [-r {0,1}] [-s SEPARATOR] [sitemap_url]
    
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


    usage: advertools urls [-h] [url_list ...]
    
    split a list of URLs into their components: scheme, netloc, path, query, etc.
    
    positional arguments:
      url_list    a list of URLs to parse (default: None)
    
    optional arguments:
      -h, --help  show this help message and exit
    

crawl a list of known URLs using the HEAD method
=================================================


    usage: advertools headers [-h] [-s [CUSTOM_SETTINGS ...]]
                              [url_list ...] output_file
    
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


    usage: advertools logs [-h] [-f [FIELDS ...]]
                           log_file output_file errors_file log_format
    
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


    usage: advertools dns [-h] [ip_list ...]
    
    perform a reverse DNS lookup on a list of IP addresses
    
    positional arguments:
      ip_list     a list of IP addresses (default: None)
    
    optional arguments:
      -h, --help  show this help message and exit
    

generate a table of SEM keywords by supplying a list of products and a list of intent words
============================================================================================


    usage: advertools semkw [-h] [-t [{exact,phrase,modified,broad} ...]]
                            [-l MAX_LEN] [-c {0,1}] [-m {0,1}] [-n CAMPAIGN_NAME]
                            products words
    
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


    usage: advertools stopwords [-h]
                                {arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}
    
    get stopwords of the selected language
    
    positional arguments:
      {arabic,azerbaijani,bengali,catalan,chinese,croatian,danish,dutch,english,finnish,french,german,greek,hebrew,hindi,hungarian,indonesian,irish,italian,japanese,kazakh,nepali,norwegian,persian,polish,portuguese,romanian,russian,sinhala,spanish,swedish,tagalog,tamil,tatar,telugu,thai,turkish,ukrainian,urdu,vietnamese}
    
    optional arguments:
      -h, --help            show this help message and exit
    

get word counts of a text list optionally weighted by a number list
====================================================================


    usage: advertools wordfreq [-h] [-n NUMBER_LIST] [-r REGEX] [-l PHRASE_LEN]
                               [-s [STOPWORDS ...]]
                               [text_list ...]
    
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


    usage: advertools emoji [-h] regex

    search for emoji using a regex

    positional arguments:
      regex       pattern to search for emoji

    optional arguments:
      -h, --help  show this help message and exit


extract structured entities from a text list; emoji, hashtags, mentions
========================================================================


    usage: advertools extract [-h] {emoji,hashtags,mentions} text_list
    
    extract structured entities from a text list; emoji, hashtags, mentions
    
    positional arguments:
      {emoji,hashtags,mentions}
                            which entity you want to extract
      text_list             filepath - a file containing the text list, one phrase per line
    
    optional arguments:
      -h, --help            show this help message and exit
    

tokenize documents (phrases, keywords, tweets, etc) into token of the desired length
=====================================================================================


    usage: advertools tokenize [-h] [-l LENGTH] [-s SEPARATOR] [text_list ...]
    
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
import argparse
import platform
import socket
import sys
from concurrent import futures
from textwrap import dedent

import pandas as pd

import advertools as adv
from advertools import __version__

system = platform.system()

_max_workers = 60 if system == 'Darwin' else 600

_entity_dict = {
    'emoji': adv.emoji.EMOJI,
    'hashtags': adv.regex.HASHTAG,
    'mentions': adv.regex.MENTION,
}


def _make_headline(text, indent=0):
    len_ = len(text)
    top = '═' * len_
    bottom = '═' * len_
    return '\n'.join([(' ' * indent) + top,
                      (' ' * indent) + text,
                      (' ' * indent) + bottom])


epilog = _make_headline('full documentation at https://bit.ly/adv_docs')


def _split_options(options):
    opsplit = [op.split('=', maxsplit=1) for op in options]
    d = {k: v for k, v in opsplit}
    for k, v in d.items():
        if v == 'True':
            d[k] = True
        if v == 'False':
            d[k] = False
    return d


def _format_df(df, head=10, precision=1):
    for col in df:
        if df[col].dtype == int:
            df[col] = [format(n, ',') for n in df[col]]
        if df[col].dtype == float:
            df[col] = [format(n, f',.{precision}f') for n in df[col]]
    return df.head(head)


def _single_request(ip):
    try:
        hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
        return [ip, hostname, '@@'.join(aliaslist), '@@'.join(ipaddrlist)]
    except Exception as e:
        return [ip, None, None, None, str(e)]



def _cli_reverse_dns_lookup(ip_list, max_workers=600):
    socket.setdefaulttimeout(8)
    count_df = (pd.Series(ip_list)
                .value_counts()
                .reset_index())
    count_df.columns = ['ip_address', 'count']
    count_df['cum_count'] = count_df['count'].cumsum()
    count_df['perc'] = count_df['count'].div(count_df['count'].sum())
    count_df['cum_perc'] = count_df['perc'].cumsum()

    hosts = []
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for host in executor.map(_single_request, count_df['ip_address']):
            hosts.append(host)

    df = pd.DataFrame(hosts)
    columns = ['ip', 'hostname', 'aliaslist', 'ipaddrlist', 'errors']
    if df.shape[1] == 4:
        columns = columns[:-1]
    df.columns = columns

    final_df = pd.merge(count_df, df, left_on='ip_address',
                        right_on='ip', how='left').drop('ip', axis=1)
    return final_df


class RawTextDefArgFormatter(argparse.RawTextHelpFormatter,
                             argparse.ArgumentDefaultsHelpFormatter):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog='advertools',
        formatter_class=RawTextDefArgFormatter,
        epilog=epilog)
    parser.add_argument('-v', '--version', action='version',
                        version=f'advertools {__version__}')

    subparsers = parser.add_subparsers(
        help='for help select a command and run: `advertools <command> --help`')

    # robots --------------------------

    def robots(args):
        if sys.stdin.isatty():
            url = args.url
        else:
            url = [u.strip() for u in sys.stdin.read().split()]
        if not url:
            print("error: please provide a value for url", file=sys.stderr)
            sys.exit(1)
        print(adv.robotstxt_to_df(url).to_csv(index=False))

    robots_parser = subparsers.add_parser(
        'robots',
        formatter_class=RawTextDefArgFormatter,
        epilog=epilog,
        description='''convert a robots.txt file (or list of file URLs) to a table in a CSV format

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
''')
    robots_parser.add_argument(
        'url', nargs='*',
        help='a robots.txt URL (or a list of URLs)')
    robots_parser.set_defaults(func=robots)

    # sitemaps --------------------------

    def sitemaps(args):
        if sys.stdin.isatty():
            sitemap_url = args.sitemap_url
        else:
            sitemap_url = sys.stdin.read().strip()
        if not sitemap_url:
            print("error: please provide a value for sitemap_url",
                  file=sys.stderr)
            sys.exit(1)
        sitemap_df = adv.sitemap_to_df(sitemap_url,
                                       recursive=bool(args.recursive))
        for col in sitemap_df:
            if col in ['news', 'image', 'news_publication']:
                del sitemap_df[col]
        print(sitemap_df.to_csv(sep=args.separator, index=False))

    sitemaps_parser = subparsers.add_parser(
        'sitemaps', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='download, parse, and save an XML sitemap to a table in a CSV file')
    sitemaps_parser.add_argument(
        'sitemap_url', nargs='?',
        help='the URL of the XML sitemap (regular or sitemap index)')
    sitemaps_parser.add_argument(
        '-r', '--recursive', type=int, choices=[0, 1],
        help='whether or not to fetch sub-sitemaps if it is a sitemap index file',
        default=1, required=False)
    sitemaps_parser.add_argument(
        '-s', '--separator', type=str, default=',',
        help='the separator with which to separate columns of the output'
    )

    sitemaps_parser.set_defaults(func=sitemaps)

    # urls --------------------------

    def urls(args):
        if sys.stdin.isatty():
            url_list = args.url_list
        else:
            url_list = [url.strip() for url in sys.stdin.read().split()]
        if not url_list:
            print("error: please provide a value for url_list",
                  file=sys.stderr)
            sys.exit(1)
        print(adv.url_to_df(url_list).to_csv(index=False))

    urls_parser = subparsers.add_parser(
        'urls', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='split a list of URLs into their components: scheme, netloc, path, query, etc.')
    urls_parser.add_argument(
        'url_list',  nargs='*',
        help='a list of URLs to parse')
    urls_parser.set_defaults(func=urls)

    # headers --------------------------

    def headers(args):
        if sys.stdin.isatty():
            url_list = args.url_list
        else:
            url_list = [url.strip() for url in sys.stdin.read().split()]
        if not url_list:
            print("error: please provide a value for url_list",
                  file=sys.stderr)
            sys.exit(1)
        if args.custom_settings:
            args.custom_settings = _split_options(args.custom_settings)
        adv.crawl_headers(url_list=url_list,
                          output_file=args.output_file,
                          custom_settings=args.custom_settings)

    headers_parser = subparsers.add_parser(
        'headers', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='''crawl a list of known URLs using the HEAD method
return status codes and all available response headers''')
    headers_parser.add_argument(
        'url_list', nargs='*',
        help='a list of URLs')
    headers_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (.jl)')
    headers_parser.add_argument(
        '-s', '--custom-settings', nargs='*',
        help='''settings that modify the behavior of the crawler
settings should be separated by spaces, and each setting name and value should
be separated by an equal sign '=' without spaces between them

example:

advertools headers https://example.com example.jl --custom-settings LOG_FILE=logs.log CLOSESPIDER_TIMEOUT=20
''')
    headers_parser.set_defaults(func=headers)

    # logs --------------------------

    def logs(args):
        adv.logs_to_df(log_file=args.log_file,
                       output_file=args.output_file,
                       errors_file=args.errors_file,
                       log_format=args.log_format,
                       fields=args.fields)
        print(f'saved to {args.output_file}')

    logs_parser = subparsers.add_parser(
        'logs', epilog=epilog, formatter_class=RawTextDefArgFormatter,
        description='parse, compress and convert a log file to a DataFrame in the .parquet format')
    logs_parser.add_argument(
        'log_file', type=str, help='filepath - the log file')
    logs_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (.parquet)')
    logs_parser.add_argument(
        'errors_file', type=str,
        help='filepath - where to save the error lines (.txt)')
    logs_parser.add_argument(
        'log_format', type=str, default='common',
        help='''the format of the logs, available defaults are:
    common, combined, common_with_vhost, nginx_error, apache_error
    supply a special regex instead if you have a different format''')
    logs_parser.add_argument(
        '-f', '--fields', type=str, nargs='*',
        help='''in case you have a special log format, provide a list of the fields names
which will become column names in the parsed compressed file''')
    logs_parser.set_defaults(func=logs)

    # dns --------------------------

    def dns(args):
        if sys.stdin.isatty():
            ip_list = args.ip_list
        else:
            ip_list = sys.stdin.read().split()
        if not ip_list:
            print('please provide a value for ip_list', file=sys.stderr)
            sys.exit(1)
        host_df = _cli_reverse_dns_lookup(ip_list)
        print(host_df.to_csv(index=False))

    dns_parser = subparsers.add_parser(
        'dns', epilog=epilog, formatter_class=RawTextDefArgFormatter,
        description='perform a reverse DNS lookup on a list of IP addresses')
    dns_parser.add_argument(
        'ip_list', nargs='*',
        help='a list of IP addresses')
    dns_parser.set_defaults(func=dns)

    # keywords --------------------------

    def semkw(args):
        prod_list = [line.strip() for line in args.products.readlines()]
        word_list = [line.strip() for line in args.words.readlines()]
        kw_df = adv.kw_generate(prod_list, word_list,
                                max_len=args.max_len,
                                match_types=args.match_types,
                                capitalize_adgroups=bool(args.capitalize_adgroups),
                                order_matters=bool(args.order_matters),
                                campaign_name=args.campaign_name)
        print(kw_df.to_csv(index=False))

    kwds_parser = subparsers.add_parser(
        'semkw', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='generate a table of SEM keywords by supplying a list of products and a list of intent words')
    kwds_parser.add_argument(
        'products', type=open,
        help='a file containing the products that you sell, one per line')
    kwds_parser.add_argument(
        'words', type=open,
        help='a file containing the intent words/phrases that you want to combine with products, one per line')
    kwds_parser.add_argument('-t', '--match-types', type=str, nargs='*',
                             default=['exact', 'phrase'],
                             choices=['exact', 'phrase', 'modified', 'broad'])
    kwds_parser.add_argument(
        '-l', '--max-len', type=int, default=3,
        help='the number of words that should be combined with products')
    kwds_parser.add_argument(
        '-c', '--capitalize-adgroups', type=int, default=1, choices=[0, 1],
        help='whether or not to capitalize ad group names in the output file')
    kwds_parser.add_argument(
        '-m', '--order-matters', type=int, default=1, choices=[0, 1],
        help='''\
do you want combinations and permutations, or just combinations?
"buy product" and "product buy" or just "buy product"?''')
    kwds_parser.add_argument('-n', '--campaign-name', type=str,
                             default='SEM_campaign')
    kwds_parser.set_defaults(func=semkw)

    # stopwords --------------------------

    def stopwords(args):
        print(*sorted(adv.stopwords[args.language]), sep='\n')

    stopwords_parser = subparsers.add_parser(
        'stopwords',
        formatter_class=RawTextDefArgFormatter,
        epilog=epilog,
        description='get stopwords of the selected language')
    stopwords_parser.add_argument(
        'language', type=str, choices=adv.stopwords.keys())
    stopwords_parser.set_defaults(func=stopwords)

    # word_freq --------------------------

    def word_freq(args):
        if sys.stdin.isatty():
            text_list = args.text_list
        else:
            text_list = sys.stdin.read().split()
        if not text_list:
            print('please provide a value for text_list', file=sys.stderr)
            sys.exit(1)

        # text_list = pd.read_csv(args.text_list, header=None)[0]
        if args.number_list is not None:
            num_list = pd.read_csv(args.number_list, header=None)[0]
        else:
            num_list = [1 for _ in range(len(text_list))]
        wordfreq_df = adv.word_frequency(
            text_list=text_list,
            num_list=num_list,
            regex=args.regex,
            phrase_len=args.phrase_len,
            rm_words=args.stopwords or adv.stopwords['english'])
        print(wordfreq_df.to_csv(index=False))

    wordfreq_parser = subparsers.add_parser(
        'wordfreq', epilog=epilog, formatter_class=RawTextDefArgFormatter,
        description='''get word counts of a text list optionally weighted by a number list

words (tokens) can be tokenized using any pattern with the --regex option
word/phrase lengths can also be modified using the --phrase-len option''')
    wordfreq_parser.add_argument(
        'text_list', type=str, nargs='*',
        help='a text list, one document (sentence, tweet, etc.) per line')
    wordfreq_parser.add_argument(
        '-n', '--number-list', type=str, required=False,
        help='filepath - a file containing the number list, one number per line')
    wordfreq_parser.add_argument(
        '-r', '--regex', type=str, required=False,
        help='a regex to tokenize words')
    wordfreq_parser.add_argument(
        '-l', '--phrase-len', type=int, required=False, default=1,
        help='the phrase (token) length to split words (the `n` in n-grams)')
    wordfreq_parser.add_argument(
        '-s', '--stopwords', type=str, nargs='*', required=False,
        help=dedent('''\
    a list of stopwords to exclude when counting, defaults to English stopwords
    run `advertools stopwords english` to get the stopwords
    change the language to get other stopwords'''))
    wordfreq_parser.set_defaults(func=word_freq)

    # emoji --------------------------

    def emoji(args):
        emoji_df = adv.emoji_search(args.regex)
        print(emoji_df.to_csv(index=False))

    emoji_parser = subparsers.add_parser(
        'emoji', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='search for emoji using a regex')
    emoji_parser.add_argument('regex', type=str,
                              help='pattern to search for emoji')
    emoji_parser.set_defaults(func=emoji)

    # extract --------------------------

    def extract(args):
        text_list = pd.read_csv(args.text_list, header=None)[0]
        extracted = adv.extract(
            text_list=text_list, key_name=args.entity.rstrip('s'),
            regex=_entity_dict[args.entity])
        extracted_subset = {key: val for key, val in extracted.items()
                            if len(val) == len(text_list)}
        for key, val in extracted_subset.items():
            if isinstance(val[0], list):
                extracted_subset[key] = [', '.join(v) for v in val]
        print(file=sys.stderr)
        print(pd.DataFrame(extracted['overview'], index=['>']), file=sys.stderr)
        print(file=sys.stderr)
        print(f'top 15 {args.entity}:\n', file=sys.stderr)
        top_df = pd.DataFrame(extracted[[k for k in extracted
                                         if k.startswith('top_')][0]],
                              columns=[args.entity, 'count'])
        print(top_df[:15], file=sys.stderr)
        freq_df = pd.DataFrame(extracted[[k for k in extracted
                                          if k.endswith('_freq')][0]])
        freq_df.columns = ['number of ' + args.entity, 'count']
        print(f'\n{args.entity} frequency:\n', file=sys.stderr)
        print(freq_df, file=sys.stderr)
        print(pd.DataFrame(extracted_subset).to_csv(index=False))

    extract_parser = subparsers.add_parser(
        'extract', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description=f'extract structured entities from a text list; {", ".join(_entity_dict.keys())}')
    extract_parser.add_argument(
        'entity', help='which entity you want to extract',
        choices=_entity_dict.keys())
    extract_parser.add_argument(
        'text_list',
        help='filepath - a file containing the text list, one phrase per line')

    extract_parser.set_defaults(func=extract)

    # tokenize --------------------------

    def tokenize(args):
        if sys.stdin.isatty():
            text_list = args.text_list
        else:
            text_list = [text.strip() for text in sys.stdin.readlines()]
        if not text_list:
            print("error: please provide a value for text_list", file=sys.stderr)
            sys.exit(1)
        tokenized = adv.word_tokenize(text_list, args.length)
        print(*[args.separator.join(t) for t in tokenized], sep='\n')

    token_parser = subparsers.add_parser(
        'tokenize', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='tokenize documents (phrases, keywords, tweets, etc) into token of the desired length')
    token_parser.add_argument(
        'text_list', type=str, nargs='*',
        help='filepath - a file containing the text list, one document (sentence, tweet, etc.) per line')
    token_parser.add_argument(
        '-l', '--length', type=int, default=1,
        help='the length of tokens (the n in n-grams)')
    token_parser.add_argument(
        '-s', '--separator', type=str, default=",",
        help='the character with which to separate the tokens')

    token_parser.set_defaults(func=tokenize)

    def crawl(args):
        if sys.stdin.isatty():
            url_list = args.url_list
        else:
            url_list = [url.strip() for url in sys.stdin.read().split()]
        if not url_list:
            print("error: please provide a value for url_list", file=sys.stderr)
            return

        if args.exclude_url_params:
            if args.exclude_url_params in ['True', 1, '1', 'true']:
                exclude_url_params = True
            else:
                exclude_url_params = args.exclude_url_params
        else:
            exclude_url_params = None
        if args.xpath_selectors:
            args.xpath_selectors = _split_options(args.xpath_selectors)
        if args.css_selectors:
            args.css_selectors = _split_options(args.css_selectors)
        if args.custom_settings:
            args.custom_settings = _split_options(args.custom_settings)
        adv.crawl(url_list=url_list,
                  output_file=args.output_file,
                  allowed_domains=args.allowed_domains,
                  css_selectors=args.css_selectors,
                  xpath_selectors=args.xpath_selectors,
                  follow_links=bool(int(args.follow_links)),
                  custom_settings=args.custom_settings,
                  exclude_url_params=exclude_url_params,
                  include_url_params=args.include_url_params,
                  exclude_url_regex=args.exclude_url_regex,
                  include_url_regex=args.include_url_regex)

    crawl_parser = subparsers.add_parser(
        'crawl', formatter_class=RawTextDefArgFormatter,
        epilog="""
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
""" + epilog,
        description='SEO crawler')
    crawl_parser.add_argument(
        'url_list', nargs='*', help='one or more URLs to crawl')
    crawl_parser.add_argument(
        'output_file',
        help='filepath - where to save the output (.jl)')
    crawl_parser.add_argument(
        '-l', '--follow-links', default=0, type=int,
        help='whether or not to follow links encountered on crawled pages')
    crawl_parser.add_argument(
        '-d', '--allowed-domains', type=str, nargs='*',
        help='while following links, only links on these domains will be followed')
    crawl_parser.add_argument(
        '--exclude-url-params', type=str, nargs='*',
        help='''a list of URL parameters to exclude while following links
if a link contains any of those parameters, don't follow it
setting it to True will exclude links containing any parameter''')
    crawl_parser.add_argument(
        '--include-url-params', type=str, nargs='*',
        help='''a list of URL parameters to include while following links
if a link contains any of those parameters, follow it
having the same parmeters to include and exclude raises an error''')
    crawl_parser.add_argument(
        '--exclude-url-regex',  type=str,
        help='''a regular expression of a URL pattern to exclude while following links
if a link matches the regex don't follow it''')
    crawl_parser.add_argument(
        '--include-url-regex', type=str,
        help='''a regular expression of a URL pattern to include while following links
if a link matches the regex follow it''')
    crawl_parser.add_argument(
        '--css-selectors', nargs='*', type=str,
        help='''a dictionary mapping names to CSS selectors
the names will become column headers, and the selectors will be used to extract the required data/content''')
    crawl_parser.add_argument(
        '--xpath-selectors', nargs='*', type=str,
        help='''a dictionary mapping names to XPath selectors.
the names will become column headers, and the selectors will be used to extract the required data/content''')
    crawl_parser.add_argument(
        '--custom-settings', type=str, nargs='*',
        help='''a dictionary of optional custom settings that you might want to
add to the spider's functionality.
there are over 170 settings for all kinds of options
for details please refer to the spider settings:
https://docs.scrapy.org/en/latest/topics/settings.html''')

    crawl_parser.set_defaults(func=crawl)
    return parser


parser = main()
args = parser.parse_args()
args.func(args)
