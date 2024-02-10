import os
import random
from itertools import product
from tempfile import TemporaryDirectory, TemporaryFile

import pandas as pd
import pytest

from advertools import crawlytics

test_filepath = "tests/data/crawl_testing/crawlytics.jl"
crawldf = pd.read_json(test_filepath, lines=True)
redirect_df = crawlytics.redirects(crawldf)
link_df = crawlytics.links(crawldf)
link_df_internal = crawlytics.links(crawldf, internal_url_regex="nytimes.com")
image_df = crawlytics.images(crawldf)
rand_columns = [random.choices(crawldf.columns, k=5) for i in range(10)]
regexes = ["img_", "jsonld", "resp_header", r"h\d$"]


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


def test_links_correct_num_links_preserved():
    index_counts = link_df.index.value_counts().sort_index()
    link_counts = crawldf["links_url"].str.split("@@").str.len().fillna(1)
    assert (index_counts == link_counts).all()


def test_links_same_urls():
    assert set(crawldf["url"]) == set(link_df["url"])


def test_link_urls_same_link_urls():
    assert set(crawldf["links_url"].str.split("@@").explode().dropna()) == set(
        link_df["link"].dropna()
    )


def test_link_text_same_link_text():
    assert set(crawldf["links_text"].str.split("@@").explode().dropna()) == set(
        link_df["text"].dropna()
    )


def test_links_same_nofollows():
    crawl_df_nofollow = [
        eval(str(x)) for x in crawldf["links_nofollow"].str.split("@@").explode()
    ]
    link_df_nofollow = [eval(str(x)) for x in link_df["nofollow"]]
    assert crawl_df_nofollow == link_df_nofollow


def test_links_empty_df_if_no_links_url():
    assert crawlytics.links(crawldf.drop("links_url", axis=1)).empty


def test_links_regex_matches_internal():
    assert (
        link_df_internal["link"]
        .astype(str)
        .str.contains("nytimes.com")
        .eq(link_df_internal["internal"])
        .all()
    )


def test_images_same_num_images():
    crawl_img_counts = (
        crawldf["img_src"].str.split("@@").explode().index.value_counts().sort_index()
    )
    img_df_counts = image_df.index.value_counts().sort_index()
    pd.testing.assert_series_equal(crawl_img_counts, img_df_counts)


def test_links_gets_same_columns():
    assert set(image_df.columns) == set(crawldf.filter(regex="^url$|^img_").columns)


def test_jl_subset_raises_on_no_params():
    with pytest.raises(ValueError):
        crawlytics.jl_subset("filepath.jl")


def test_jl_subset_raises_on_wrong_filepath():
    with pytest.raises(ValueError):
        crawlytics.jl_subset("somewrongfilepath", regex="regex")


@pytest.mark.parametrize("columns", rand_columns)
def test_jl_subset_correct_cols(columns):
    subset_df = crawlytics.jl_subset(test_filepath, columns=columns)
    col_regex = "^" + "$|^".join(columns) + "$"
    assert set(subset_df.columns) == set(subset_df.filter(regex=col_regex).columns)


@pytest.mark.parametrize("regex", regexes)
def test_jl_subset_correct_regex(regex):
    subset_df = crawlytics.jl_subset(test_filepath, regex=regex)
    assert set(subset_df.columns) == set(subset_df.filter(regex=regex).columns)


@pytest.mark.parametrize(["columns", "regex"], product(rand_columns, regexes))
def test_jl_subset_correct_cols_and_regex(columns, regex):
    subset_df = crawlytics.jl_subset(test_filepath, columns=columns, regex=regex)
    col_regex = "^" + "$|^".join(columns) + "$"
    full_regex = "|".join([col_regex, regex])
    assert set(subset_df.columns) == set(subset_df.filter(regex=full_regex).columns)


def test_jl_subset_doesnt_contain_nonexistent_col():
    subset_df = crawlytics.jl_subset(
        test_filepath,
        columns=["title", "url", "doesnt_exist"],
    )
    assert "doesnt_exist" not in subset_df


def test_jl_to_parquet_file_exists():
    with TemporaryDirectory() as tempdir:
        crawlytics.jl_to_parquet(test_filepath, f"{tempdir}/delete.parquet")
        assert os.path.isfile(f"{tempdir}/delete.parquet")


def test_jl_to_parquet_correct_columns():
    with TemporaryDirectory() as tempdir:
        crawlytics.jl_to_parquet(test_filepath, f"{tempdir}/delete.parquet")
        jl_df = pd.read_json(test_filepath, lines=True)
        pq_df = pd.read_parquet(f"{tempdir}/delete.parquet")
        pq_cols = crawlytics.parquet_columns(f"{tempdir}/delete.parquet")
        assert set(jl_df.columns) == set(pq_df.columns)
        assert set(jl_df.columns) == set(pq_cols["column"])
