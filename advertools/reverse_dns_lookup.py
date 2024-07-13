"""
.. _reverse_dns_lookup:

.. raw:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"></script>

Getting the host name of a list of IP addresses can be useful in verifying
the authenticity of those IP addresses. You typically want to do this as part
of a :ref:`log file analysis <logs>` pipeline. In this case you have requests
made to your server claiming to be of a certain user agent/bot name. Performing
a :func:`reverse_dns_lookup` on those IP addresses, will get you the actual
host name that they belong to.

What the :func:`reverse_dns_lookup` function does, is simply like running the
`host` command from the command line, but on a massive scale:

.. code-block:: bash

    $ host 66.249.80.0
    0.80.249.66.in-addr.arpa domain name pointer google-proxy-66-249-80-0.google.com.


Because you usually have a large number of duplicated IP addresses that you
want to check, this function makes the process practical and efficient, in
comparison to running the command thousands of times from the comand line.

Running the function is very simple, you simply supply a list of the IP
addresses that you have. Make sure to **keep the duplicates**, because the
function handles that for you, as well as provide counts and some statistics on
the frequency of the IPs:

.. container:: thebe

    .. thebe-button::
        Run this code

    .. code-block::
        :class: thebe, thebe-init

        import advertools as adv
        ip_list = ['66.249.66.194', '66.249.66.194', '66.249.66.194',
                '66.249.66.91', '66.249.66.91', '130.185.74.243',
                '31.56.96.51', '5.211.97.39']

        host_df = adv.reverse_dns_lookup(ip_list)
        host_df

====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================
  ..  ip_address        count    cum_count    perc    cum_perc  hostname                           aliaslist                    ipaddrlist      errors
====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================
   0  66.249.66.194         3            3   0.375       0.375  crawl-66-249-66-194.googlebot.com  194.66.249.66.in-addr.arpa   66.249.66.194
   1  66.249.66.91          2            5   0.25        0.625  crawl-66-249-66-91.googlebot.com   91.66.249.66.in-addr.arpa    66.249.66.91
   2  130.185.74.243        1            6   0.125       0.75   mail.garda.ir                      243.74.185.130.in-addr.arpa  130.185.74.243
   3  31.56.96.51           1            7   0.125       0.875  31-56-96-51.shatel.ir              51.96.56.31.in-addr.arpa     31.56.96.51
   4  5.211.97.39           1            8   0.125       1                                                                                      [Errno 1] Unknown host
====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================

As you can see, in addition to getting hostnames, aliaslist, and ipaddrlist for
the IPs you supplied, you also get counts (absolute and cumulative) as well as
percentages (absolute and cumulative). This can give you a good overview of
the relative importance of each IP, and can help focus attention on them as
needed.
"""  # noqa: E501

import platform
import socket
from concurrent import futures

import pandas as pd

system = platform.system()

_default_max_workders = 60 if system == "Darwin" else 600


def _single_request(ip):
    try:
        hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
        return [ip, hostname, "@@".join(aliaslist), "@@".join(ipaddrlist)]
    except Exception as e:
        return [ip, None, None, None, str(e)]


def reverse_dns_lookup(ip_list, max_workers=_default_max_workders):
    """Return the hostname, aliaslist, and ipaddrlist for a list of IP
    addresses.

    This is mainly useful for a long list of typically duplicated IP adresses
    and helps in getting the information very fast. It is basically the
    equivalent of running the `host` command on the command line many times:

    .. code-block:: bash

        $ host advertools.readthedocs.io
        advertools.readthedocs.io has address 104.17.32.82

    Parameters
    ----------
    ip_list : list
      A list of IP addresses.
    max_workers : int
      The maximum number of workers to use for multi processing.


    You also get a simple report about the counts of the IPs to get an overview
    of the top ones.

    Examples
    --------
    >>> import advertools as adv
    >>> ip_list = [
    ...     "66.249.66.194",
    ...     "66.249.66.194",
    ...     "66.249.66.194",
    ...     "66.249.66.91",
    ...     "66.249.66.91",
    ...     "130.185.74.243",
    ...     "31.56.96.51",
    ...     "5.211.97.39",
    ... ]
    >>> adv.reverse_dns_lookup([ip_list])

    ====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================
      ..  ip_address        count    cum_count    perc    cum_perc  hostname                           aliaslist                    ipaddrlist      errors
    ====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================
       0  66.249.66.194         3            3   0.375       0.375  crawl-66-249-66-194.googlebot.com  194.66.249.66.in-addr.arpa   66.249.66.194
       1  66.249.66.91          2            5   0.25        0.625  crawl-66-249-66-91.googlebot.com   91.66.249.66.in-addr.arpa    66.249.66.91
       2  130.185.74.243        1            6   0.125       0.75   mail.garda.ir                      243.74.185.130.in-addr.arpa  130.185.74.243
       3  31.56.96.51           1            7   0.125       0.875  31-56-96-51.shatel.ir              51.96.56.31.in-addr.arpa     31.56.96.51
       4  5.211.97.39           1            8   0.125       1                                                                                      [Errno 1] Unknown host
    ====  ==============  =======  ===========  ======  ==========  =================================  ===========================  ==============  ======================
    """  # noqa: E501
    socket.setdefaulttimeout(8)
    count_df = pd.Series(ip_list).value_counts().reset_index()
    count_df.columns = ["ip_address", "count"]
    count_df["cum_count"] = count_df["count"].cumsum()
    count_df["perc"] = count_df["count"].div(count_df["count"].sum())
    count_df["cum_perc"] = count_df["perc"].cumsum()

    hosts = []
    if system == "Darwin":
        with futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for _ip, host in zip(
                ip_list, executor.map(_single_request, count_df["ip_address"])
            ):
                hosts.append(host)
    else:
        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for host in executor.map(_single_request, count_df["ip_address"]):
                hosts.append(host)
    df = pd.DataFrame(hosts)
    columns = ["ip", "hostname", "aliaslist", "ipaddrlist", "errors"]
    if df.shape[1] == 4:
        columns = columns[:-1]
    df.columns = columns
    final_df = pd.merge(
        count_df, df, left_on="ip_address", right_on="ip", how="left"
    ).drop("ip", axis=1)
    return final_df
