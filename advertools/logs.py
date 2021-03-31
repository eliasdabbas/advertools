"""
.. _logs:

Parse and Analyze Crawl Logs in a Dataframe (experimental)
==========================================================

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

>>> import pandas as pd
>>> logs_df = pd.read_csv('example.log')


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
import re

import pandas as pd


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
