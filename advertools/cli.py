import argparse

import pandas as pd

import advertools as adv
from advertools import __version__

pd.options.display.max_columns = None


def main():
    parser = argparse.ArgumentParser(
        prog='advertools',
        epilog="advertools - digital marketing productivity and analysis".center(79, '='))
    parser.add_argument('-v', '--version', action='version',
                        version=f'advertools {__version__}')

    subparsers = parser.add_subparsers(
        help='for help, run: `advertools <command> -h`',
        description='Select a sub-command to run: `advertools <subcommand> options...`')

    # robots --------------------------

    def robots(args):
        if args.url:
            robots_df = adv.robotstxt_to_df(args.url)
        else:
            robots_df = adv.robotstxt_to_df([line.strip() for line in args.file])
        robots_df.to_csv(args.output_file, index=False)

    robots_parser = subparsers.add_parser(
        'robots', description='Convert a robots.txt file to a table in a CSV file')
    robots_group = robots_parser.add_mutually_exclusive_group(required=True)
    robots_group.add_argument('-u', '--url', help='the URL of the robots.txt file')
    robots_group.add_argument('-f', '--file', type=open, help='the location of a text file containing a list of robots.txt URLs')
    robots_parser.add_argument('-o', '--output-file', required=True, help='where to save the file (csv)')
    robots_parser.set_defaults(func=robots)

    # sitemaps --------------------------


    def sitemaps(args):
        sitemap_df = adv.sitemap_to_df(args.url, recursive=args.recursive)
        sitemap_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')


    sitemaps_parser = subparsers.add_parser(
        'sitemaps', description='Download, parse, and save a sitemap to a table in a CSV file.')
    sitemaps_parser.add_argument('-u', '--url', required=True, help='The URL of the sitemap (regular or sitemap index)')
    sitemaps_parser.add_argument('-r', '--recursive', type=int, choices=[0, 1],
                                help='Whether to fetch sub-sitemaps if it is a sitemap index file',
                                default=1, required=False)
    sitemaps_parser.add_argument('-o', '--output-file', required=True)
    sitemaps_parser.set_defaults(func=sitemaps)

    # urls --------------------------


    def urls(args):
        url_list = [line.strip() for line in args.url_list.readlines()]
        url_df = adv.url_to_df(url_list)
        url_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')


    urls_parser = subparsers.add_parser(
        'urls', description='Split a list of URLs into their components: scheme, netloc, path, query, etc.')
    urls_parser.add_argument('-u', '--url-list', type=open, required=True,
                            help='The path to a file containing URLs, one per line.')
    urls_parser.add_argument('-o', '--output-file', required=True,
                            help='Filepath - where to save the output.')
    urls_parser.set_defaults(func=urls)

    # keywords --------------------------


    def keywords(args):
        prod_list = [line.strip() for line in args.products.readlines()]
        word_list = [line.strip() for line in args.words.readlines()]
        kw_df = adv.kw_generate(prod_list, word_list,
                                max_len=args.max_len,
                                match_types=args.match_types,
                                capitalize_adgroups=args.capitalize_adgroups,
                                order_matters=args.order_matters,
                                campaign_name=args.campaign_name)
        kw_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')

    kwds_parser = subparsers.add_parser(
        'keywords',
        description='Generate a table of SEM keywords (and save to csv) by supplying a list of products and intent words.')
    kwds_parser.add_argument('-p', '--products', type=open, required=True)
    kwds_parser.add_argument('-w', '--words', type=open, required=True)
    kwds_parser.add_argument('-t', '--match-types', type=str, nargs='*',
                            default=['exact', 'phrase'],
                            choices=['exact', 'phrase', 'modified', 'broad'])
    kwds_parser.add_argument('-l', '--max-len', type=int, default=3)
    kwds_parser.add_argument('-c', '--capitalize-adgroups', type=bool, default=1, choices=[0, 1])
    kwds_parser.add_argument('-m', '--order-matters', type=bool, default=1, choices=[0, 1])
    kwds_parser.add_argument('-n', '--campaign-name', type=str, default='SEM_campaign')
    kwds_parser.add_argument('-o', '--output-file', required=True)
    kwds_parser.set_defaults(func=keywords)

    # logs --------------------------

    def logs(args):
        adv.logs_to_df(log_file=args.log_file,
                       output_file=args.output_file,
                       errors_file=args.errors_file,
                       log_format=args.log_format,
                       fields=args.fields)
        print(f'saved to {args.output_file}')


    logs_parser = subparsers.add_parser('logs')
    logs_parser.add_argument('-f', '--log-file', type=str, required=True)
    logs_parser.add_argument('-o', '--output-file', type=str, required=True)
    logs_parser.add_argument('-e', '--errors-file', type=str, required=True)
    logs_parser.add_argument('-t', '--log-format', type=str, default='common')
    logs_parser.add_argument('-d', '--fields', type=str, nargs='*')

    logs_parser.set_defaults(func=logs)

    # headers --------------------------

    def headers(args):
        adv.crawl_headers(url_list=args.url_list,
                        output_file=args.output_file)


    headers_parser = subparsers.add_parser('headers')
    headers_parser.add_argument('-u', '--url-list', type=open, required=True)
    headers_parser.add_argument('-o', '--output-file', type=str, required=True)
    headers_parser.set_defaults(func=headers)

    # dns --------------------------


    def dns(args):
        # use threads if actual OS is Darwin
        import platform
        if platform.system == 'Darwin':
            adv.reverse_dns_lookup.__globals__['system'] = 'Linux'
        ip_list = [line.strip() for line in args.ip_list]
        host_df = adv.reverse_dns_lookup(ip_list=ip_list)
        host_df.to_csv(args.output_file, index=False)
        print(f'saved to {args.output_file}')


    dns_parser = subparsers.add_parser('dns')
    dns_parser.add_argument('-p', '--ip-list', type=open, required=True)
    dns_parser.add_argument('-o', '--output-file', type=str, required=True)
    dns_parser.set_defaults(func=dns)

    return parser

parser = main()
args = parser.parse_args()
args.func(args)
