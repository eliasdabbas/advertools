from urllib.parse import urlsplit, parse_qs, unquote

import pandas as pd


def url_to_df(urls, decode=True):
    """Split the given URLs into their components to a DataFrame.

    Each column will have its own component, and query parameters and
    directories will also be parsed and given special columns each.

    :param url urls: A list of URLs to split into components
    :param bool decode: Whether or not to decode the given URLs
    :return DataFrame split: A DataFrame with a column for each component
    """
    if isinstance(urls, str):
        urls = [urls]
    decode = unquote if decode else lambda x: x
    split_list = []
    for url in urls:
        split = urlsplit(decode(url))
        port = split.port
        hostname = split.hostname if split.hostname != split.netloc else None
        split = split._asdict()
        if hostname:
            split['hostname'] = hostname
        if port:
            split['port'] = port
        parsed_query = parse_qs(split['query'])
        parsed_query = {'query_' + key: '@@'.join(val)
                        for key, val in parsed_query.items()}
        split.update(**parsed_query)
        dirs = split['path'].strip('/').split('/')
        if dirs[0]:
            dir_cols = {'dir_{}'.format(n): d for n,d in enumerate(dirs, 1)}
            split.update(**dir_cols)
        split_list.append(split)
    df = pd.DataFrame(split_list)

    query_df = df.filter(regex='query_')
    if not query_df.empty:
        df = df.drop(query_df.columns, axis=1)
    dirs_df = df.filter(regex='dir_')
    if not dirs_df.empty:
        df = df.drop(dirs_df.columns, axis=1)
    df = pd.concat([df, dirs_df, query_df], axis=1)
    df.insert(0, 'url', [decode(url) for url in urls])
    return df
