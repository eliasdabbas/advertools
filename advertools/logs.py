"""
.. _logs:

Log File Analysis (experimental)
================================

Logs contain very detailed information about events happening on computers.
And the extra details that they provide, come with additional complexity that
we need to handle ourselves. A pageview may contain many log lines, and a
session can consist of several pageviews for example.

Another important characterisitic of log files is that their are usualy not
big.
They are massive.

So, we also need to cater for their large size, as well as rapid changes.

TL;DR

>>> import advertools as adv
>>> import pandas as pd
>>> adv.logs_to_df(log_file='access.log',
...                output_file='access_logs.parquet',
...                errors_file='log_errors.csv',
...                log_format='common',
...                fields=None)
>>> logs_df = pd.read_parquet('access_logs.parquet')

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
  take any one of the pre-defined formats, for example "common", or "extended",
  or a regular expression that you provide. This means that you can parse any
  log format (as long as lines are single lines, and not formatted in JSON).
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
>>> logs_df = adv.crawllogs_to_df('example.log')


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

"""
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

LOG_FORMATS = {
    'common': r'^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)$',
    'combined': r'^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)"$',
    'common_with_vhost': r'^(?P<vhost>\S+) (?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)$',
    'nginx_error': r'^(?P<datetime>\d{4}/\d\d/\d\d \d\d:\d\d:\d\d) \[(?P<level>[^\]]+)\] (?P<pid>\d+)#(?P<tid>\d+): (?P<counter>\*\d+ | )?(?P<message>.*)',
    'apache_error': r'^(?P<datetime>\[[^\]]+\]) (?P<level>\[[^\]]+\]) \[pid (?P<pid>\d+)\] (?P<file>\S+):(?P<status> \S+| ):? \[client (?P<client>\S+)\] (?P<message>.*)',
}

LOG_FIELDS = {
    'common': ['client', 'userid', 'datetime', 'method', 'request', 'status',
               'size'],
    'combined': ['client', 'userid', 'datetime', 'method', 'request', 'status',
                 'size', 'referer', 'user_agent'],
    'common_with_vhost': ['virtual_host', 'client', 'userid', 'datetime',
                          'method', 'request', 'status', 'size'],
    'nginx_error': ['datetime', 'level', 'process_id', 'thread_id', 'counter',
                    'message'],
    'apache_error': ['datetime', 'level', 'process_id', 'file', 'status',
                     'client', 'message'],
}


def logs_to_df(log_file, output_file, errors_file, log_format, fields=None):
    """Parse and compress any log file into a DataFrame format.

    Convert a log file to a `parquet` file in a DataFrame format, and save all
    errors (or lines not conformig to the chosen log format) into a separate
    ``errors_file`` text file. Any non-JSON log format is possible, provided
    you have the right regex for it. A few default ones are provided and can be
    used. Check out ``adv.LOG_FORMATS`` and ``adv.LOG_FIELDS`` for the
    available formats and fields.

    >>> import advertools as adv
    >>> import pandas as pd
    >>> adv.logs_to_df(log_file='access.log',
    ...                output_file='access_logs.parquet',
    ...                errors_file='log_errors.csv',
    ...                log_format='common',
    ...                fields=None)
    >>> logs_df = pd.read_parquet('access_logs.parquet')

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
    :param str fields: A list of fields, which will become the names of columns
                       in ``output_file``. Only required if you provide a
                       custom (regex) ``log_format``.

    """
    if not output_file.endswith('.parquet'):
        raise ValueError("Please provide an `output_file` with a `.parquet` "
                         "extension.")
    for file in [output_file, errors_file]:
        if os.path.exists(file):
            raise ValueError(f"The file '{file}' already exists. "
                             "Please rename it, delete it, or choose another "
                             "file name/path.")

    regex = LOG_FORMATS.get(log_format) or log_format
    columns = fields or LOG_FIELDS[log_format]
    with TemporaryDirectory() as tempdir:
        tempdir_name = Path(tempdir)
        with open(log_file) as source_file:
            linenumber = 0
            parsed_lines = []
            for line in source_file:
                linenumber += 1
                try:
                    log_line = re.findall(regex, line)[0]
                    parsed_lines.append(log_line)
                except Exception as e:
                    with open(errors_file, 'at') as err:
                        err_line = line[:-1] if line.endswith('\n') else line
                        print('@@'.join([str(linenumber), err_line, str(e)]),
                              file=err)
                    pass
                if linenumber % 250_000 == 0:
                    print(f'Parsed {linenumber:>15,} lines.', end='\r')
                    df = pd.DataFrame(parsed_lines, columns=columns)
                    df.to_parquet(tempdir_name / f'file_{linenumber}.parquet')
                    parsed_lines.clear()
            else:
                print(f'Parsed {linenumber:>15,} lines.', end='\r')
                df = pd.DataFrame(parsed_lines, columns=columns)
                df.to_parquet(tempdir_name / f'file_{linenumber}.parquet')
            final_df = pd.read_parquet(tempdir_name)
            try:
                final_df['status'] = final_df['status'].astype('category')
                final_df['method'] = final_df['method'].astype('category')
                final_df['size'] = pd.to_numeric(final_df['size'],
                                                 downcast='signed')
            except KeyError:
                pass
            final_df.to_parquet(output_file)


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
    >>> logs_df = adv.crawl_logs_to_df('example.log')


    :param str logs_file_path: The path to the logs file.

    :returns DataFrame crawl_logs_df: A DataFrame summarizing the logs.
    """
    time_middleware_level = "(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \[(.*?)\] ([A-Z]+): "
    time_middleware_level_error = "(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \[(.*?)\] (ERROR): "

    filtered_regex = time_middleware_level + "(Filtered) offsite request to '(.*?)': <([A-Z]+) (.*?)>" 
    filtered_cols = ['time', 'middleware', 'level', 'message', 'domain', 'method', 'url']

    crawled_regex = time_middleware_level + "(Crawled) \((\d\d\d)\) <([A-Z]+) (.*?)> \(referer: (.*?)\)" 
    crawled_cols = ['time', 'middleware', 'level', 'message', 'status', 'method', 'url', 'referer']

    scraped_regex = time_middleware_level + "(Scraped) from <(\d\d\d) (.*?)>" 
    scraped_cols = ['time', 'middleware', 'level', 'message', 'status', 'url']

    redirect_regex = time_middleware_level + "(Redirect)ing \((\d\d\d)\) to <([A-Z]+) (.*?)> from <([A-Z]+) (.*?)>"
    redirect_cols = ['time', 'middleware', 'level', 'message', 'status', 'method_to', 'redirect_to', 'method_from', 'redirect_from']

    blocked_regex = time_middleware_level + "(Forbidden) by robots\.txt: <([A-Z]+) (.*?)>"
    blocked_cols = ['time', 'middleware', 'level', 'message', 'method', 'blocked_urls']

    error_regex = time_middleware_level + "Spider (error) processing <([A-Z]+) (.*?)> \(referer: (.*?)\)"
    error_cols = ['time', 'middleware', 'level', 'message', 'method', 'url', 'referer']

    error_level_regex = time_middleware_level_error  + '(.*)? (\d\d\d) (http.*)'
    error_level_cols = ['time', 'middleware', 'level', 'message', 'status', 'url']

    filtered_lines = []
    crawled_lines = []
    scraped_lines = []
    redirect_lines = []
    blocked_lines = []
    error_lines = []
    error_lvl_lines = []

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

    final_df = pd.concat([
        pd.DataFrame(filtered_lines, columns=filtered_cols),
        pd.DataFrame(crawled_lines, columns=crawled_cols),
        pd.DataFrame(scraped_lines, columns=scraped_cols),
        pd.DataFrame(redirect_lines, columns=redirect_cols),
        pd.DataFrame(blocked_lines, columns=blocked_cols),
        pd.DataFrame(error_lines, columns=error_cols),
        pd.DataFrame(error_lvl_lines, columns=error_level_cols),
    ])

    final_df['time'] = pd.to_datetime(final_df['time'])
    final_df = final_df.sort_values('time').reset_index(drop=True)

    return final_df
