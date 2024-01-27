import os

import pandas as pd

from advertools import crawlytics

crawldf = pd.read_json("tests/data/crawl_testing/crawlytics.jl", lines=True)
redirect_df = crawlytics.redirects(crawldf)


def test_redirects_empty_df_redir_urls_isna():
    crawldf_no_redirects = crawldf[crawldf["redirect_urls"].isna()]
    redirect_df = crawlytics.redirects(crawldf_no_redirects)
    assert redirect_df.empty


def test_redirects_empty_df_no_redir_urls_col():
    crawldf = pd.DataFrame()
    redirect_df = crawlytics.redirects(crawldf)
    assert redirect_df.empty


def test_redirects_correct_columns():
    assert set(redirect_df.columns) == {
        "url",
        "status",
        "order",
        "type",
        "download_latency",
        "redirect_times",
    }


def test_redirects_num_redirects_matches_crawldf():
    assert redirect_df.index.nunique() == crawldf["redirect_urls"].dropna().shape[0]


def test_redirects_correct_types():
    assert redirect_df["type"].drop_duplicates().sort_values().tolist() == [
        "crawled",
        "intermediate",
        "requested",
    ]


def test_redirects_correct_redir_times():
    index_counts_df = redirect_df.index.value_counts().sort_index().sub(1)
    redirect_times = (
        redirect_df.reset_index()[["index", "redirect_times"]]
        .drop_duplicates(subset=["index"])
        .set_index("index")
        .squeeze()
    )
    assert index_counts_df.eq(redirect_times).all()


def test_redirects_requested_eq_1():
    assert (
        redirect_df[["order", "type"]].query('type=="requested"')["order"].eq(1).all()
    )


def test_redirects_crawl_status_not_3xx():
    assert (
        redirect_df[["status", "type"]]
        .query('type=="crawled"')["status"]
        .astype(str)
        .str[0]
        .ne("3")
        .all()
    )


def test_redirects_order_monotonic_increasing():
    assert (
        redirect_df.reset_index()
        .groupby("index")["order"]
        .is_monotonic_increasing.all()
    )
