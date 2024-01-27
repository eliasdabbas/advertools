import pandas as pd


def redirects(crawldf):
    """Create a tidy DataFrame for redirects with the columns:

    url: All the URLs in the redirect chain.
    status: The status code of each URL.
    type: "requested", "inermediate", or "crawled".
    order: 1, 2, 3... up to the number of urls in the redirect chain.
    redirect_times: The number of redirects in the chain (URLs in the chain minus one).

    Parameters:
    -----------
    crawldf : pandas.DataFrame
      A DataFrame of an advertools crawl file
    """
    if "redirect_urls" not in crawldf.columns:
        return pd.DataFrame()
    if "redirect_urls" in crawldf:
        if crawldf["redirect_urls"].isna().all():
            return pd.DataFrame()
    redirect_df = crawldf[
        ["url", "status", "redirect_urls", "redirect_reasons"]
    ].dropna(subset=["redirect_urls", "redirect_reasons"])
    redirect_df["redirect_urls"] = (
        redirect_df["redirect_urls"].astype(str).str.split("@@")
    )
    redirect_df["redirect_reasons"] = (
        redirect_df["redirect_reasons"].astype(str).str.split("@@")
    )
    for url, redirect_urls in redirect_df[["url", "redirect_urls"]].values:
        redirect_urls.append(url)
    for status, redirect_reasons in redirect_df[["status", "redirect_reasons"]].values:
        redirect_reasons.append(status)
    redirect_df["order"] = [
        list(range(1, len(x) + 1)) for x in redirect_df["redirect_reasons"]
    ]
    redirect_df["type"] = [
        [
            "requested"
            if o == min(order)
            else "crawled"
            if o == max(order)
            else "intermediate"
            for o in order
        ]
        for order in redirect_df["order"]
    ]
    redirect_df.columns = ["NA1", "NA2", "url", "status", "order", "type"]
    exploded = redirect_df[["url", "status", "order", "type"]].apply(pd.Series.explode)
    final_df = pd.merge(
        exploded,
        crawldf[["download_latency", "redirect_times"]],
        left_index=True,
        right_index=True,
    )
    final_df["redirect_times"] = final_df["redirect_times"].astype(int)
    return final_df
