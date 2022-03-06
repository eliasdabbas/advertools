import argparse
import platform
import socket
from concurrent import futures
from textwrap import dedent

import pandas as pd

import advertools as adv
from advertools import __version__

pd.options.display.max_columns = None
pd.options.display.width = 200

system = platform.system()

_default_max_workders = 60 if system == 'Darwin' else 600

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
        help='for help select an argument and run: `advertools <argument> -h`')

    # robots --------------------------

    def robots(args):
        if args.url:
            robots_df = adv.robotstxt_to_df(args.url)
        else:
            robots_df = adv.robotstxt_to_df([line.strip() for line in args.file])
        robots_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')

    robots_parser = subparsers.add_parser(
        'robots',
        formatter_class=RawTextDefArgFormatter,
        epilog=epilog,
        description='convert a robots.txt file (or list of file URLs by using the --file argument) to a table in a CSV file')
    robots_group = robots_parser.add_mutually_exclusive_group(required=True)
    robots_group.add_argument(
        '-u', '--url', help='the URL of the robots.txt file')
    robots_group.add_argument(
        '-f', '--file', type=open,
        help='the path to a file containing a list of robots.txt URLs, one per line')
    robots_parser.add_argument(
        'output_file',
        help='filepath - where to save the output (csv)')
    robots_parser.set_defaults(func=robots)

    # sitemaps --------------------------

    def sitemaps(args):
        sitemap_df = adv.sitemap_to_df(args.sitemap_url, recursive=args.recursive)
        sitemap_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')

    sitemaps_parser = subparsers.add_parser(
        'sitemaps', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='download, parse, and save a sitemap to a table in a CSV file')
    sitemaps_parser.add_argument(
        'sitemap_url',
        help='the URL of the XML sitemap (regular or sitemap index)')
    sitemaps_parser.add_argument(
        'output_file',
        help='filepath - where to save the output (csv)')
    sitemaps_parser.add_argument(
        '-r', '--recursive', type=int, choices=[0, 1],
        help='whether to fetch sub-sitemaps if it is a sitemap index file',
        default=1, required=False)

    sitemaps_parser.set_defaults(func=sitemaps)

    # urls --------------------------

    def urls(args):
        url_list = [line.strip() for line in args.url_list.readlines()]
        url_df = adv.url_to_df(url_list)
        url_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')

    urls_parser = subparsers.add_parser(
        'urls', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='split a list of URLs into their components: scheme, netloc, path, query, etc.')
    urls_parser.add_argument(
        'url_list', type=open,
        help='the path to a file containing URLs, one per line.')
    urls_parser.add_argument('output_file',
                             help='filepath - where to save the output (csv)')
    urls_parser.set_defaults(func=urls)

    # headers --------------------------

    def headers(args):
        adv.crawl_headers(url_list=args.url_list,
                          output_file=args.output_file)

    headers_parser = subparsers.add_parser(
        'headers', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='''crawl a list of known URLs using the HEAD method
return status codes and all response headers''')
    headers_parser.add_argument(
        'url_list', type=open,
        help='a file containing a list of URLs, one per line')
    headers_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (.jl)')
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
        '-f', '--fields', type=str, nargs='+',
        help='''in case you have a special log format, provide a list of the fields names
which will become column names in the parsed compressed file''')
    logs_parser.set_defaults(func=logs)

    # dns --------------------------

    def dns(args):
        ip_list = [line.strip() for line in args.ip_list]
        host_df = _cli_reverse_dns_lookup(ip_list=ip_list)
        host_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')

    dns_parser = subparsers.add_parser(
        'dns', epilog=epilog, formatter_class=RawTextDefArgFormatter,
        description='perform a reverse DNS lookup on a list of IP addresses')
    dns_parser.add_argument(
        'ip_list', type=open,
        help='filepath - a file containing a list of IP addresses, one per line')
    dns_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (csv)')
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
        kw_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')
        print()
        print('sample rows:')
        print(kw_df)
        print()

    kwds_parser = subparsers.add_parser(
        'semkw', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='generate a table of SEM keywords by supplying a list of products and a list of intent words')
    kwds_parser.add_argument(
        'products', type=open,
        help='a file containing the products that you sell, one per line')
    kwds_parser.add_argument(
        'words', type=open,
        help='a file containing the intent words that you want to combine with products')
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
    kwds_parser.add_argument(
        'output_file',
        help='filepath - where to save the output (csv)')
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
        text_list = pd.read_csv(args.text_list, header=None)[0]
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
        wordfreq_df.to_csv(args.output_file, index=False)
        print(f'\nsaved to {args.output_file}\n')
        print('first ten rows:\n')
        formatted_df = _format_df(wordfreq_df)
        print(formatted_df)
        print()

    wordfreq_parser = subparsers.add_parser(
        'wordfreq', epilog=epilog, formatter_class=RawTextDefArgFormatter,
        description='''get word counts of a text list optionally weighted by a number list
words (tokens) can be tokenized using any pattern with the --regex option
word/phrase lengths can also be modified using the --phrase-len option''')
    wordfreq_parser.add_argument(
        'text_list', type=str,
        help='filepath - a file containing the text list, one document (sentence, tweet, etc.) per line')
    wordfreq_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (csv)')
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
        emoji_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')
        print()
        print(emoji_df)

    emoji_parser = subparsers.add_parser(
        'emoji', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description='search for emoji using a regex')
    emoji_parser.add_argument('regex', type=str,
                              help='pattern to search for emoji')
    emoji_parser.add_argument(
        'output_file', type=str,
        help='filepath - where to save the output (csv)')
    emoji_parser.set_defaults(func=emoji)

    # extract --------------------------

    def extract(args):
        text_list = pd.read_csv(args.text_list, header=None)[0]
        extracted = adv.extract(
            text_list=text_list, key_name=args.entity.rstrip('s'),
            regex=_entity_dict[args.entity])
        extracted_subset = {key: val for key, val in extracted.items()
                            if len(val) == len(text_list)}
        print()
        print(pd.DataFrame(extracted['overview'], index=['>']))
        print()
        print(f'top 15 {args.entity}:\n')
        top_df = pd.DataFrame(extracted[[k for k in extracted
                                         if k.startswith('top_')][0]],
                              columns=[args.entity, 'count'])
        print(top_df[:15])
        freq_df = pd.DataFrame(extracted[[k for k in extracted
                                          if k.endswith('_freq')][0]])
        freq_df.columns = ['number of ' + args.entity, 'count']
        print(f'\n{args.entity} frequency:\n')
        print(freq_df)
        print(f'\nextracted {args.entity}:\n')
        pd.DataFrame(extracted_subset).to_csv(args.output_file, index=False)
        print(pd.DataFrame(extracted_subset))

    extract_parser = subparsers.add_parser(
        'extract', formatter_class=RawTextDefArgFormatter, epilog=epilog,
        description=f'extract structured entities from a text list; {", ".join(_entity_dict.keys())}')
    extract_parser.add_argument(
        'entity', help='which entity you want to extract',
        choices=_entity_dict.keys())
    extract_parser.add_argument(
        'text_list',
        help='filepath - a file containing the text list, one phrase per line')
    extract_parser.add_argument(
        'output_file',
        help='filepath - where to save the output (csv)')

    extract_parser.set_defaults(func=extract)

    return parser


parser = main()
args = parser.parse_args()
args.func(args)
