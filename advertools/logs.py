"""
.. _logs:

Log File Analysis
=================

Logs contain very detailed information about events happening on computers.
And the extra details that they provide come with additional complexity that
we need to handle ourselves. A pageview may contain many log lines, and a
session can consist of several pageviews for example.

Another important characterisitic of log files is that their are usualy not
big.
They are massive.

So, we also need to cater for their large size, as well as rapid changes.

TL;DR

>>> import advertools as adv
>>> import pandas as pd
>>> adv.logs_to_df(
...     log_file="access.log",
...     output_file="access_logs.parquet",
...     errors_file="log_errors.csv",
...     log_format="common",
...     fields=None,
... )
>>> logs_df = pd.read_parquet("access_logs.parquet")

How to run the :func:`logs_to_df` function:
-------------------------------------------

* ``log_file``: The path to the log file you are trying to analyze.
* ``output_file``: The path to where you want the parsed and compressed file
  to be saved. Only the `parquet` format is supported.
* ``errors_file``: You will almost certainly have log lines that don't conform
  to the format that you have, so all lines that weren't properly parsed would
  go to this file. This file also contains the error messages, so you know what
  went wrong, and how you might fix it. In some cases, you might simply take
  these "errors" and parse them again. They might not be really errors, but
  lines in a different format, or temporary debug messages.
* ``log_format``: The format in which your logs were formatted. Logs can (and
  are) formatted in many ways, and there is no right or wrong way. However,
  there are defaults, and a few popular formats that most servers use. It is
  likely that your file is in one of the popular formats. This parameter can
  take any one of the pre-defined formats, for example "common", or "combined",
  or a regular expression that you provide. This means that **you can parse any
  log format** (as long as lines are single lines, and not formatted in JSON).
* ``date_format``: The date format string that the log file uses. For the supported
  default formats there are also default date formats. In some cases you might have a
  different date format. You can use standard
  `Python date string formatting. <https://strftime.org/>`_. For example, to parse this
  string "2024-01-01" you can use ``%Y-%m-%d``. If this is the correct pattern the
  output file's datetime column will be saved as a datetime column, otherwise, it will
  be saved as a string.
* ``fields``: If you selected one of the supported formats, then there is no
  need to provide a value for this parameter. You have to provide a list of
  fields in case you provide a custom (regex) format. The fields will become
  the names of the columns of the resulting DataFrame, so you can distinguish
  between them (client, time, status code, response size, etc.)

Supported Log Formats
---------------------

* `common`
* `combined` (a.k.a "extended")
* `common_with_vhost`
* `nginx_error`
* `apache_error`


Log File Analysis - Data Preparation
------------------------------------

We go through an example where we prepare the data for analysis, and here is
the plan:

1. Parse the log file into a DataFrame saved to disk with a `.parquet`
   extension. A side effect is that your log file is also compressed down to
   5% - 15% of its original size. It also makes it super efficient to query and
   analyze once in this format. Function used: ``logs_to_df``.
2. Convert data types as needed (optional): Most importantly converting the
   `datetime` column into a date object helps a lot in querying the data. Other
   possibilities include converting to categorical data types for more
   efficient storage and querying. Function used: ``pandas.to_datetime``.
3. Get the hostnames of the IP addresses of the clients sending requests.
   Function used:  :ref:`reverse_dns_lookup <reverse_dns_lookup>`. We can then
   easily add a ``hostname`` column to the original DataFrame.
4. Parse and split URL columns into their respective components. Typically we
   have ``request`` which is the resource/URL requested, as well as ``referer``
   , which shows us where the request was referred from. Function used:
   :ref:`url_to_df <urlytics>`.
5. Parse user agents if available. This allows us to analyze by user-agent
   family, operating system, bot/non-bot, version, and any other combination we
   want.
6. Combine all data together, and save back to a new `.parquet` file, and start
   analyzing.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    !head data/sample_log.log

.. code-block::

    66.249.73.72 - - [16/Feb/2022:00:18:53 +0000] "GET / HTTP/1.1" 200 1095 "-" "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    109.237.103.118 - - [16/Feb/2022:00:20:39 +0000] "GET /.env HTTP/1.1" 404 209 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    45.12.223.214 - - [16/Feb/2022:00:23:45 +0000] "GET / HTTP/1.0" 200 2240 "http://adver.tools/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    51.68.77.249 - - [16/Feb/2022:00:26:23 +0000] "GET /robots.txt HTTP/1.1" 404 209 "-" "advertools/0.13.0"
    51.68.77.249 - - [16/Feb/2022:00:26:23 +0000] "HEAD / HTTP/1.1" 200 0 "-" "advertools/0.13.0"
    192.241.211.176 - - [16/Feb/2022:00:31:16 +0000] "GET /login HTTP/1.1" 404 209 "-" "Mozilla/5.0 zgrab/0.x"
    66.249.73.69 - - [16/Feb/2022:00:48:56 +0000] "GET /robots.txt HTTP/1.1" 404 209 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    66.249.73.72 - - [16/Feb/2022:00:48:56 +0000] "GET /staging/urlytics/ HTTP/1.1" 200 520 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    66.249.73.75 - - [16/Feb/2022:00:49:38 +0000] "GET /staging/urlytics/_dash-component-suites/dash/html/dash_html_components.v2_0_0m1638886228.min.js HTTP/1.1" 200 154258 "http://www.adver.tools/staging/urlytics/" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/98.0.4758.80 Safari/537.36"
    66.249.73.75 - - [16/Feb/2022:00:49:39 +0000] "GET /staging/urlytics/_dash-layout HTTP/1.1" 200 2547 "http://www.adver.tools/staging/urlytics/" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/98.0.4758.80 Safari/537.36"


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv
    import pandas as pd
    from ua_parser import user_agent_parser
    pd.options.display.max_columns = None

    adv.logs_to_df(log_file='data/sample_log.log',
                   output_file='data/adv_logs.parquet',
                   errors_file='data/adv_errors.txt',
                   log_format='combined')

Read the parquet file into a pandas DataFrame, and convert the ``datetime``
column into a datetime object.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    logs_df = pd.read_parquet('data/adv_logs.parquet')
    logs_df['datetime'] = pd.to_datetime(logs_df['datetime'],
                                         format='%d/%b/%Y:%H:%M:%S %z')

    logs_df


Perform a reverse DNS lookup on the IP addresses in the ``client`` column:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    %%time
    host_df = adv.reverse_dns_lookup(logs_df['client'])
    print(f'Rows, columns: {host_df.shape}')
    host_df.head(15)
    # Rows, columns: (1210, 9)
    # CPU times: user 745 ms, sys: 729 ms, total: 1.47 s
    # Wall time: 21.1 s

====  ===============  =======  ===========  ==========  ==========  ======================================  ===========================  ==============  ======================
  ..  ip_address         count    cum_count        perc    cum_perc  hostname                                aliaslist                    ipaddrlist      errors
====  ===============  =======  ===========  ==========  ==========  ======================================  ===========================  ==============  ======================
   0  143.244.132.225      426          426  0.0701004    0.0701004                                                                                       [Errno 1] Unknown host
   1  45.146.164.110       290          716  0.0477209    0.117821                                                                                        [Errno 1] Unknown host
   2  46.177.196.171       192          908  0.0315945    0.149416   ppp046177196171.access.hol.gr           171.196.177.46.in-addr.arpa  46.177.196.171
   3  185.22.173.83        182         1090  0.029949     0.179365                                                                                        [Errno 1] Unknown host
   4  152.32.226.223       171         1261  0.0281389    0.207504                                                                                        [Errno 1] Unknown host
   5  94.200.35.174        154         1415  0.0253415    0.232845                                                                                        [Errno 1] Unknown host
   6  89.47.44.105         130         1545  0.0213921    0.254237   ppp089047044105.access.hol.gr           105.44.47.89.in-addr.arpa    89.47.44.105
   7  94.200.92.2          119         1664  0.019582     0.273819                                                                                        [Errno 1] Unknown host
   8  143.244.132.234      113         1777  0.0185947    0.292414                                                                                        [Errno 1] Unknown host
   9  217.100.98.101        81         1858  0.0133289    0.305743   d9646265.static.ziggozakelijk.nl        101.98.100.217.in-addr.arpa  217.100.98.101
  10  203.163.243.241       79         1937  0.0129998    0.318743                                                                                        [Errno 1] Unknown host
  11  66.249.73.135         77         2014  0.0126707    0.331414   crawl-66-249-73-135.googlebot.com       135.73.249.66.in-addr.arpa   66.249.73.135
  12  194.163.179.92        60         2074  0.00987329   0.341287   vmi660635.contaboserver.net             92.179.163.194.in-addr.arpa  194.163.179.92
  13  66.249.73.137         58         2132  0.00954418   0.350831   crawl-66-249-73-137.googlebot.com       137.73.249.66.in-addr.arpa   66.249.73.137
  14  109.70.100.30         58         2190  0.00954418   0.360375   tor-exit-anonymizer.appliedprivacy.net  30.100.70.109.in-addr.arpa   109.70.100.30
====  ===============  =======  ===========  ==========  ==========  ======================================  ===========================  ==============  ======================

Add a new ``hostname`` column, by matching IP adresses to their hostnames.


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    ip_host_dict = dict(zip(host_df['ip_address'], host_df['hostname']))
    logs_df['hostname'] = [ip_host_dict[ip] for ip in logs_df['client']]

Split the request URLs into their components.


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    request_url_df = adv.url_to_df(logs_df['request'])
    request_url_df = request_url_df.add_prefix('request_')
    request_url_df.head(10)


====  ================================================================================================  ================  ================  ================================================================================================  ===============  ==================  ==================  ==============  ===============  ===============  ======================  ===============  ===============  =============================================  ===============  ===============  ===============  ================  ================  ================  ================  =============================================  =====================  =================  ====================================  ========================  =======================  =========================  ====================  ===================  =================  =======================  ==================  ======================  ========================  ===================  ===================  ====================  ===================  ====================  ======================  =========================  ==========================  ==================================  ====================  =========================  =======================  ====================  ==================  ===================  =====================  ====================  ====================  ===================  =========================  ==================  ==========================  =================  ===========================  =====================  ====================  =======================  ==================  =====================  =====================  ======================  ==========================  ========================  =========================  ======================  =====================================================  =========================  =====================================  ====================  ======================  ==========================  =====================  =====================  ====================  ======================  =======================  =================  ======================  =================  =====================  ===================  ====================  ====================  =======================  ===================  ========================  =====================  ====================  ===================  ===================  ===================  =======================  =====================  ======================  ===================  =================================  ====================  ========================  ========================
  ..  request_url                                                                                       request_scheme    request_netloc    request_path                                                                                      request_query    request_fragment      request_hostname    request_port  request_dir_1    request_dir_2    request_dir_3           request_dir_4    request_dir_5    request_dir_6                                    request_dir_7    request_dir_8    request_dir_9    request_dir_10    request_dir_11    request_dir_12    request_dir_13  request_last_dir                                 request_query_index    request_query_s    request_query_XDEBUG_SESSION_START    request_query_function    request_query_vars[0]    request_query_vars[1][]    request_query_file    request_query_url    request_query_a    request_query_content    request_query_wt    request_query_action    request_query_username    request_query_psd    request_query_dns    request_query_step    request_query_cmd    request_query_lang    request_query_option    request_query_folderIds    request_query_input_file    request_query_currentsetting.htm    request_query_type    request_query_next_file    request_query_curpath    request_query_page    request_query_id    request_query_img    request_query_panel    request_query_todo    request_query_code    request_query_ref    request_query_scopeName    request_query_op    request_query_controller    request_query_q    request_query_sb_category    request_query_Email    request_query_name    request_query_abspath    request_query_fn    request_query_files    request_query_thumb    request_query_ACTION    request_query_NOCONTINUE    request_query_filepath    request_query_file_link    request_query_myPath    request_query_adaptive-images-settings[source_file]    request_query_aam-media    request_query_cpabc_calendar_update    request_query_term    request_query_Itemid    request_query_search_key    request_query_short    request_query_title    request_query_Type    request_query_format    request_query_findcli    request_query_v    request_query_target    request_query__    request_query_albid    request_query_pic    request_query_path    request_query_mode    request_query_libpath    request_query_srt    request_query_redirect    request_query_order    request_query_item    request_query_gid    request_query_act    request_query_rid    request_query_service    request_query_agent    request_query_typeid    request_query_dir    request_query_stockCodeInternal    request_query_site    request_query_position    request_query_fileName
====  ================================================================================================  ================  ================  ================================================================================================  ===============  ==================  ==================  ==============  ===============  ===============  ======================  ===============  ===============  =============================================  ===============  ===============  ===============  ================  ================  ================  ================  =============================================  =====================  =================  ====================================  ========================  =======================  =========================  ====================  ===================  =================  =======================  ==================  ======================  ========================  ===================  ===================  ====================  ===================  ====================  ======================  =========================  ==========================  ==================================  ====================  =========================  =======================  ====================  ==================  ===================  =====================  ====================  ====================  ===================  =========================  ==================  ==========================  =================  ===========================  =====================  ====================  =======================  ==================  =====================  =====================  ======================  ==========================  ========================  =========================  ======================  =====================================================  =========================  =====================================  ====================  ======================  ==========================  =====================  =====================  ====================  ======================  =======================  =================  ======================  =================  =====================  ===================  ====================  ====================  =======================  ===================  ========================  =====================  ====================  ===================  ===================  ===================  =======================  =====================  ======================  ===================  =================================  ====================  ========================  ========================
   0  /                                                                                                                                     /                                                                                                                                                     nan             nan  nan              nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  nan                                                              nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   1  /.env                                                                                                                                 /.env                                                                                                                                                 nan             nan  .env             nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  .env                                                             nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   2  /                                                                                                                                     /                                                                                                                                                     nan             nan  nan              nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  nan                                                              nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   3  /robots.txt                                                                                                                           /robots.txt                                                                                                                                           nan             nan  robots.txt       nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  robots.txt                                                       nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   4  /                                                                                                                                     /                                                                                                                                                     nan             nan  nan              nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  nan                                                              nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   5  /login                                                                                                                                /login                                                                                                                                                nan             nan  login            nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  login                                                            nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   6  /robots.txt                                                                                                                           /robots.txt                                                                                                                                           nan             nan  robots.txt       nan              nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  robots.txt                                                       nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   7  /staging/urlytics/                                                                                                                    /staging/urlytics/                                                                                                                                    nan             nan  staging          urlytics         nan                     nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  urlytics                                                         nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   8  /staging/urlytics/_dash-component-suites/dash/html/dash_html_components.v2_0_0m1638886228.min.js                                      /staging/urlytics/_dash-component-suites/dash/html/dash_html_components.v2_0_0m1638886228.min.js                                                      nan             nan  staging          urlytics         _dash-component-suites  dash             html             dash_html_components.v2_0_0m1638886228.min.js              nan              nan              nan               nan               nan               nan               nan  dash_html_components.v2_0_0m1638886228.min.js                    nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
   9  /staging/urlytics/_dash-layout                                                                                                        /staging/urlytics/_dash-layout                                                                                                                        nan             nan  staging          urlytics         _dash-layout            nan              nan              nan                                                        nan              nan              nan               nan               nan               nan               nan  _dash-layout                                                     nan                nan                                   nan                       nan                      nan                        nan                   nan                  nan                nan                      nan                 nan                     nan                       nan                  nan                  nan                   nan                  nan                   nan                     nan                        nan                         nan                                 nan                   nan                        nan                      nan                   nan                 nan                  nan                    nan                   nan                   nan                  nan                        nan                 nan                         nan                nan                          nan                    nan                   nan                      nan                 nan                    nan                    nan                     nan                         nan                       nan                        nan                     nan                                                    nan                        nan                                    nan                   nan                     nan                         nan                    nan                    nan                   nan                     nan                      nan                nan                     nan                nan                    nan                  nan                   nan                   nan                      nan                  nan                       nan                    nan                   nan                  nan                  nan                  nan                      nan                    nan                     nan                  nan                                nan                   nan                       nan                       nan
====  ================================================================================================  ================  ================  ================================================================================================  ===============  ==================  ==================  ==============  ===============  ===============  ======================  ===============  ===============  =============================================  ===============  ===============  ===============  ================  ================  ================  ================  =============================================  =====================  =================  ====================================  ========================  =======================  =========================  ====================  ===================  =================  =======================  ==================  ======================  ========================  ===================  ===================  ====================  ===================  ====================  ======================  =========================  ==========================  ==================================  ====================  =========================  =======================  ====================  ==================  ===================  =====================  ====================  ====================  ===================  =========================  ==================  ==========================  =================  ===========================  =====================  ====================  =======================  ==================  =====================  =====================  ======================  ==========================  ========================  =========================  ======================  =====================================================  =========================  =====================================  ====================  ======================  ==========================  =====================  =====================  ====================  ======================  =======================  =================  ======================  =================  =====================  ===================  ====================  ====================  =======================  ===================  ========================  =====================  ====================  ===================  ===================  ===================  =======================  =====================  ======================  ===================  =================================  ====================  ========================  ========================

Do the same for the URLs in the ``referer`` column.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    referer_url_df = adv.url_to_df(logs_df['referer'])
    referer_url_df = referer_url_df.add_prefix('referer_')
    referer_url_df.head(10)

====  ========================================  ================  ================  ==================  ===============  ==================  ==================  ==============  ===============  ===============  ===============  ==================
  ..  referer_url                               referer_scheme    referer_netloc    referer_path        referer_query    referer_fragment      referer_hostname    referer_port  referer_dir_1    referer_dir_2      referer_dir_3  referer_last_dir
====  ========================================  ================  ================  ==================  ===============  ==================  ==================  ==============  ===============  ===============  ===============  ==================
   0  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   1  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   2  http://adver.tools/                       http              adver.tools       /                                                                       nan             nan  nan              nan                          nan  nan
   3  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   4  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   5  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   6  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   7  \-                                                                            \-                                                                      nan             nan  \-               nan                          nan  \-
   8  http://www.adver.tools/staging/urlytics/  http              www.adver.tools   /staging/urlytics/                                                      nan             nan  staging          urlytics                     nan  urlytics
   9  http://www.adver.tools/staging/urlytics/  http              www.adver.tools   /staging/urlytics/                                                      nan             nan  staging          urlytics                     nan  urlytics
====  ========================================  ================  ================  ==================  ===============  ==================  ==================  ==============  ===============  ===============  ===============  ==================

Parse the ``user_agent`` column.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    ua_df = pd.json_normalize([user_agent_parser.Parse(ua) for ua in logs_df['user_agent']])
    ua_df.columns = 'ua_' + ua_df.columns.str.replace('user_agent\.', '', regex=True)
    ua_df.head(10)

====  ======================================================================================================================================================================================================  ===========  ==========  ==========  ==========  ==============  =============  =============  =============  ===================  ==================  =================  =================
  ..  ua_string                                                                                                                                                                                               ua_family      ua_major    ua_minor    ua_patch  ua_os.family      ua_os.major    ua_os.minor    ua_os.patch  ua_os.patch_minor    ua_device.family    ua_device.brand    ua_device.model
====  ======================================================================================================================================================================================================  ===========  ==========  ==========  ==========  ==============  =============  =============  =============  ===================  ==================  =================  =================
   0  Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)  Googlebot             2           1              Android                     6              0              1                       Spider              Spider             Smartphone
   1  Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36                                                                                               Chrome               81           0        4044  Linux                                                                             Other
   2  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36                                                                                      Chrome               90           0        4430  Windows                    10                                                     Other
   3  advertools/0.13.0                                                                                                                                                                                       Other                                            Other                                                                             Other
   4  advertools/0.13.0                                                                                                                                                                                       Other                                            Other                                                                             Other
   5  Mozilla/5.0 zgrab/0.x                                                                                                                                                                                   Other                                            Other                                                                             Other
   6  Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)                                                                                                                                Googlebot             2           1              Other                                                                             Spider              Spider             Desktop
   7  Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)                                                                                                                                Googlebot             2           1              Other                                                                             Spider              Spider             Desktop
   8  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/98.0.4758.80 Safari/537.36                                                        Googlebot             2           1              Other                                                                             Spider              Spider             Desktop
   9  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/98.0.4758.80 Safari/537.36                                                        Googlebot             2           1              Other                                                                             Spider              Spider             Desktop
====  ======================================================================================================================================================================================================  ===========  ==========  ==========  ==========  ==============  =============  =============  =============  ===================  ==================  =================  =================

Combine all data into one DataFrame and save to a new `.parquet` file.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    (pd.concat([logs_df, request_url_df, referer_url_df, ua_df], axis=1)
    .to_parquet('data/adv_logs_final.parquet', index=False, version='2.4'))


Start the analysis.

The advantage of using the parquet format is that the file doens't need to be
loaded into memory, and can be queried from disk, just like querying a
database. This means you only load the columns that you select, and the rows
that satisfy certain conditions. For example we can load the
``ua_device.family`` and ``ua_family`` columns, and only the rows where
``'ua_device.family', '==', 'Spider'``. We then count the values in the
``ua_family`` column, and get the top bots accessing our website.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    top_bots = pd.read_parquet('data/adv_logs_final.parquet',
                    filters=[
                        ('ua_device.family', '==', 'Spider')
                    ],
                    columns=['ua_device.family', 'ua_family'])['ua_family'].value_counts()
    top_bots[:15]

.. code-block::

    Googlebot      499
    PetalBot        46
    AhrefsBot       42
    Chrome          29
    YandexBot       29
    LinkedInBot     23
    Baiduspider     18
    DotBot          17
    Twitterbot      16
    bingbot         12
    MJ12bot         12
    Java            10
    Nutch            8
    masscan          6
    FacebookBot      4
    Name: ua_family, dtype: int64

Happy analyzing!

Parse and Analyze Crawl Logs in a Dataframe
===========================================

While crawling with the :func:`crawl` function, the process produces logs for
every page crawled, scraped, redirected, and even blocked by robots.txt rules.

By default, those logs are can be seen on the command line as their default
destination is stdout.

A good practice is to set a ``LOG_FILE`` so you can save those logs to a text
file, and review them later. There are several reasons why you might want to do
that:

* Blocked URLs: The crawler obeys robots.txt rules by default, and when it
  encounters pages that it shouldn't crawl, it doesn't. However, this is logged
  as an event, and you can easily extract a list of blocked URLs from the logs.
* Crawl errors: You might also get some errors while crawling, and it can be
  interesting to know which URLs generated errors.
* Filtered pages: Those are pages that were discovered but weren't crawled
  because they are not a sub-domain of the provided url_list, or happen to be
  on external domains altogether.

This can simply be done by specifying a file name through the optional
`custom_settings` parameter of ``crawl``:

>>> import advertools as adv
>>> adv.crawl('https://example.com',
              output_file='example.jl',
              follow_links=True,
              custom_settings={'LOG_FILE': 'example.log'})

If you run it this way, all logs will be saved to the file you chose,
`example.log` in this case.

Now, you can use the :func:`crawllogs_to_df` function to open the logs in a
DataFrame:

>>> import advertools as adv
>>> logs_df = adv.crawllogs_to_df("example.log")


The DataFrame might contain the following columns:

* `time`: The timestamp for the process
* `middleware`: The middleware responsible for this process, whether it is the
  core engine, the scraper, error handler and so on.
* `level`: The logging level (DEBUG, INFO, etc.)
* `message`: A single word summarizing what this row represents, "Crawled",
  "Scraped", "Filtered", and so on.
* `domain`: The domain name of filtered (not crawled pages) typically for URLs
  outside the current website.
* `method`: The HTTP method used in this process (GET, PUT, etc.)
* `url`: The URL currently under process.
* `status`: HTTP status code, 200, 404, etc.
* `referer`: The referring URL, where applicable.
* `method_to`: In redirect rows the HTTP method used to crawl the URL going to.
* `redirect_to`: The URL redirected to.
* `method_from`: In redirect rows the HTTP method used to crawl the URL coming
  from.
* `redirect_from`: The URL redirected from.
* `blocked_urls`: The URLs that were not crawled due to robots.txt rules.

"""  # noqa: E501

import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

LOG_FORMATS = {
    "common": r'^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)$',  # noqa: E501
    "combined": r'^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)"\s*$',  # noqa: E501
    "common_with_vhost": r'^(?P<vhost>\S+) (?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)$',  # noqa: E501
    "nginx_error": r"^(?P<datetime>\d{4}/\d\d/\d\d \d\d:\d\d:\d\d) \[(?P<level>[^\]]+)\] (?P<pid>\d+)#(?P<tid>\d+): (?P<counter>\*\d+ | )?(?P<message>.*)",  # noqa: E501
    "apache_error": r"^(?P<datetime>\[[^\]]+\]) (?P<level>\[[^\]]+\]) \[pid (?P<pid>\d+)\] (?P<file>\S+):(?P<status> \S+| ):? \[client (?P<client>\S+)\] (?P<message>.*)",  # noqa: E501
}

LOG_FIELDS = {
    "common": ["client", "userid", "datetime", "method", "request", "status", "size"],
    "combined": [
        "client",
        "userid",
        "datetime",
        "method",
        "request",
        "status",
        "size",
        "referer",
        "user_agent",
    ],
    "common_with_vhost": [
        "virtual_host",
        "client",
        "userid",
        "datetime",
        "method",
        "request",
        "status",
        "size",
    ],
    "nginx_error": [
        "datetime",
        "level",
        "process_id",
        "thread_id",
        "counter",
        "message",
    ],
    "apache_error": [
        "datetime",
        "level",
        "process_id",
        "file",
        "status",
        "client",
        "message",
    ],
}

LOG_DATE_FORMATS = {
    "common": "%d/%b/%Y:%H:%M:%S %z",
    "combined": "%d/%b/%Y:%H:%M:%S %z",
    "common_with_vhost": "%d/%b/%Y:%H:%M:%S %z",
    "nginx_error": "%Y/%m/%d %H:%M:%S",
    "apache_error": "%a %b %d %H:%M:%S.%f %Y",
}


def logs_to_df(
    log_file,
    output_file,
    errors_file,
    log_format,
    date_format=None,
    fields=None,
    encoding="utf-8",
):
    """Parse and compress any log file into a DataFrame format.

    Convert a log file to a `parquet` file in a DataFrame format, and save all
    errors (or lines not conformig to the chosen log format) into a separate
    ``errors_file`` text file. Any non-JSON log format is possible, provided
    you have the right regex for it. A few default ones are provided and can be
    used. Check out ``adv.LOG_FORMATS`` and ``adv.LOG_FIELDS`` for the
    available formats and fields.

    Parameters
    ----------
    log_file : str
      The path to the log file.
    output_file : str
      The path to the desired output file. Must have a ".parquet" extension, and must
      not have the same path as an existing file.
    errors_file : str
      The path where the parsing errors are stored. Any text format works, CSV is
      recommended to easily open it with any CSV reader with the separator as "@@".
    log_format : str
      The name of one of the supported log formats, or a regex of your own format.
    fields : list
      A list of fields, which will become the names of columns in ``output_file``. Only
      required if you provide a custom (regex) ``log_format``.
    encoding : str
      The encoding of the log file. It defaults to utf-8, but you might need to try
      others in case of errors (latin-1, utf-16, etc.)

    Examples
    --------
    >>> import advertools as adv
    >>> import pandas as pd
    >>> adv.logs_to_df(
    ...     log_file="access.log",
    ...     output_file="access_logs.parquet",
    ...     errors_file="log_errors.csv",
    ...     log_format="common",
    ...     fields=None,
    ... )
    >>> logs_df = pd.read_parquet("access_logs.parquet")

    You can now analyze ``logs_df`` as a normal pandas DataFrame.

    :param str log_file: The path to the log file.
    :param str output_file: The path to the desired output file. Must have a
                            ".parquet" extension, and must not have the same
                            path as an existing file.
    :param str errors_file: The path where the parsing errors are stored. Any
                            text format works, CSV is recommended to easily
                            open it with any CSV reader with the separator as
                            "@@".
    :param str log_format: Either the name of one of the supported log formats,
                           or a regex of your own format.
    :param str date_format: The date format in strftime format, in case you have a
                                a different one from the default.
    :param str fields: A list of fields, which will become the names of columns
                       in ``output_file``. Only required if you provide a
                       custom (regex) ``log_format``.
    :param str encoding: The encoding of the log file. It defaults to utf-8, but
                         you might need to try others in case of errors
                         (latin-1, utf-16, etc.)
    """
    if not output_file.endswith(".parquet"):
        raise ValueError(
            "Please provide an `output_file` with a `.parquet` " "extension."
        )
    if not LOG_DATE_FORMATS.get(log_format) and fields is None:
        raise ValueError(
            "Please supply a value for the `fields` parameter when you provide a custom"
            "log format."
        )
    regex = LOG_FORMATS.get(log_format) or log_format
    date_fmt = date_format or LOG_DATE_FORMATS.get(log_format)
    columns = fields or LOG_FIELDS[log_format]
    with TemporaryDirectory() as tempdir:
        tempdir_name = Path(tempdir)
        with open(log_file, encoding=encoding) as source_file:
            parsed_lines = []
            for i, line in enumerate(source_file):
                try:
                    log_line = re.findall(regex, str(line))[0]
                    parsed_lines.append(log_line)
                except Exception as e:
                    with open(tempdir_name / "errors.txt", "at") as err:
                        print("@@".join([str(i), line.rstrip(), str(e)]), file=err)
                    pass
                if i % 250_000 == 0:
                    print(f"Parsed {i:>15,} lines.", end="\r")
                    df = pd.DataFrame(parsed_lines, columns=columns)
                    df.to_parquet(tempdir_name / f"file_{i}.parquet")
                    parsed_lines.clear()
            else:
                print(f"Parsed {i:>15,} lines.")
                try:
                    with open(tempdir_name / "errors.txt", "rt") as err_final:
                        err_content = err_final.read()
                        with open(errors_file, "wt") as errout:
                            errout.write(err_content)
                    os.remove(tempdir_name / "errors.txt")
                except FileNotFoundError:
                    pass
                df = pd.DataFrame(parsed_lines, columns=columns)
                df.to_parquet(tempdir_name / f"file_{i}.parquet")
            final_df = pd.read_parquet(tempdir_name)
            if "datetime" in final_df:
                try:
                    final_df["datetime"] = pd.to_datetime(
                        final_df["datetime"], format=date_fmt
                    )
                except Exception as e:
                    pass
            try:
                final_df["status"] = final_df["status"].astype("category")
                final_df["method"] = final_df["method"].astype("category")
                final_df["size"] = pd.to_numeric(
                    final_df["size"].replace("-", np.nan), downcast="signed"
                )
            except KeyError:
                pass
            final_df.to_parquet(output_file, index=False, version="2.6")


def crawllogs_to_df(logs_file_path):
    """Convert a crawl logs file to a DataFrame.

    An interesting option while using the ``crawl`` function, is to specify a
    destination file to save the logs of the crawl process itself. This contains
    additional information about each crawled, scraped, blocked, or redirected
    URL.

    What you would most likely use this for is to get a list of URLs blocked by
    robots.txt rules. These can be found und the column ``blocked_urls``.
    Crawling errors are also interesting, and can be found in rows where
    ``message`` is equal to "error".

    >>> import advertools as adv
    >>> adv.crawl('https://example.com',
                  output_file='example.jl',
                  follow_links=True,
                  custom_settings={'LOG_FILE': 'example.log'})
    >>> logs_df = adv.crawl_logs_to_df("example.log")


    :param str logs_file_path: The path to the logs file.

    :returns DataFrame crawl_logs_df: A DataFrame summarizing the logs.
    """
    time_middleware_level = r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \[(.*?)\] ([A-Z]+): "
    time_middleware_level_error = (
        r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \[(.*?)\] (ERROR): "
    )

    filtered_regex = (
        time_middleware_level
        + "(Filtered) offsite request to '(.*?)': <([A-Z]+) (.*?)>"
    )
    filtered_cols = [
        "time",
        "middleware",
        "level",
        "message",
        "domain",
        "method",
        "url",
    ]

    crawled_regex = (
        time_middleware_level
        + r"(Crawled) \((\d\d\d)\) <([A-Z]+) (.*?)> \(referer: (.*?)\)"
    )
    crawled_cols = [
        "time",
        "middleware",
        "level",
        "message",
        "status",
        "method",
        "url",
        "referer",
    ]

    scraped_regex = time_middleware_level + r"(Scraped) from <(\d\d\d) (.*?)>"
    scraped_cols = ["time", "middleware", "level", "message", "status", "url"]

    redirect_regex = (
        time_middleware_level
        + r"(Redirect)ing \((\d\d\d)\) to <([A-Z]+) (.*?)> from <([A-Z]+) (.*?)>"
    )
    redirect_cols = [
        "time",
        "middleware",
        "level",
        "message",
        "status",
        "method_to",
        "redirect_to",
        "method_from",
        "redirect_from",
    ]

    blocked_regex = (
        time_middleware_level + r"(Forbidden) by robots\.txt: <([A-Z]+) (.*?)>"
    )
    blocked_cols = ["time", "middleware", "level", "message", "method", "blocked_urls"]

    error_regex = (
        time_middleware_level
        + r"Spider (error) processing <([A-Z]+) (.*?)> \(referer: (.*?)\)"
    )
    error_cols = ["time", "middleware", "level", "message", "method", "url", "referer"]

    error_level_regex = time_middleware_level_error + r"(.*)? (\d\d\d) (http.*)"
    error_level_cols = ["time", "middleware", "level", "message", "status", "url"]

    generic_error_regex = time_middleware_level_error + "(.*)"
    generic_error_cols = ["time", "middleware", "level", "message"]

    filtered_lines = []
    crawled_lines = []
    scraped_lines = []
    redirect_lines = []
    blocked_lines = []
    error_lines = []
    error_lvl_lines = []
    generic_error_lines = []

    with open(logs_file_path) as file:
        for line in file:
            if re.findall(filtered_regex, line):
                filtered_lines.append(re.findall(filtered_regex, line)[0])
            if re.findall(crawled_regex, line):
                crawled_lines.append(re.findall(crawled_regex, line)[0])
            if re.findall(scraped_regex, line):
                scraped_lines.append(re.findall(scraped_regex, line)[0])
            if re.findall(redirect_regex, line):
                redirect_lines.append(re.findall(redirect_regex, line)[0])
            if re.findall(blocked_regex, line):
                blocked_lines.append(re.findall(blocked_regex, line)[0])
            if re.findall(error_regex, line):
                error_lines.append(re.findall(error_regex, line)[0])
            if re.findall(error_level_regex, line):
                error_lvl_lines.append(re.findall(error_level_regex, line)[0])
            if re.findall(generic_error_regex, line):
                generic_error_lines.append(re.findall(generic_error_regex, line)[0])

    final_df = pd.concat(
        [
            pd.DataFrame(filtered_lines, columns=filtered_cols),
            pd.DataFrame(crawled_lines, columns=crawled_cols),
            pd.DataFrame(scraped_lines, columns=scraped_cols),
            pd.DataFrame(redirect_lines, columns=redirect_cols),
            pd.DataFrame(blocked_lines, columns=blocked_cols),
            pd.DataFrame(error_lines, columns=error_cols),
            pd.DataFrame(error_lvl_lines, columns=error_level_cols),
            pd.DataFrame(generic_error_lines, columns=generic_error_cols),
        ]
    )

    final_df["time"] = pd.to_datetime(final_df["time"])
    final_df = final_df.sort_values("time").reset_index(drop=True)

    return final_df
