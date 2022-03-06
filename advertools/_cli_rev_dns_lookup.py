import platform
import socket
from concurrent import futures

import pandas as pd

system = platform.system()

_default_max_workders = 60 if system == 'Darwin' else 600


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
