import platform
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from advertools.spider import crawl

system = platform.system()

links_columns = {
    "links_url": 14,
    "links_text": 14,
    "links_nofollow": 14,
    "nav_links_url": 3,
    "nav_links_text": 3,
    "header_links_url": 3,
    "header_links_text": 3,
    "footer_links_url": 3,
    "footer_links_text": 3,
}

links_filepath = "tests/data/crawl_testing/test_content.html"
if platform == "Windows":
    links_filepath = links_filepath.replace("/", r"\\")
links_file = Path(links_filepath).absolute()

dup_links_file_path = "tests/data/crawl_testing/duplicate_links.html"
if platform == "Windows":
    dup_links_file_path = dup_links_file_path.replace("/", r"\\")
dup_links_file = Path(dup_links_file_path).absolute()

broken_links_path = "tests/data/crawl_testing/broken_links.html"
if platform == "Windows":
    broken_links_path = links_filepath.replace("/", r"\\")

broken_links_file = Path(broken_links_path).absolute()

with TemporaryDirectory() as links_crawl_tempdir:
    crawl(
        links_file.as_uri(),
        f"{links_crawl_tempdir}/links_crawl.jl",
        custom_settings={"ROBOTSTXT_OBEY": False},
    )
    crawl_df = pd.read_json(f"{links_crawl_tempdir}/links_crawl.jl", lines=True)

    def test_link_columns_all_exist():
        assert set(links_columns).difference(crawl_df.columns.tolist()) == set()

    @pytest.mark.parametrize("colname,count", links_columns.items())
    def test_links_extracted_at_correct_number(colname, count):
        assert crawl_df[colname].str.split("@@").str.len().values[0] == count

    def test_extract_h_tags():
        assert crawl_df["h2"].str.split("@@").str.len().values[0] == 3
        assert crawl_df["h2"].str.split("@@").explode().iloc[1] == ""

    def test_all_links_have_nofollow():
        assert (
            crawl_df.filter(regex="nofollow")
            .apply(lambda s: s.str.contains("True"))
            .all()
            .all()
        )

    def test_image_tags_available():
        assert [
            col in crawl_df for col in ["img_src", "img_alt", "img_height", "img_width"]
        ]

    def test_all_img_attrs_have_same_length():
        assert (
            crawl_df.filter(regex="img_")
            .apply(lambda s: s.str.split("@@").str.len())
            .apply(set, axis=1)[0]
            .__len__()
        ) == 1

    def test_img_src_has_abs_path():
        assert crawl_df["img_src"].str.startswith("http").all()


with TemporaryDirectory() as follow_url_params_tempdir:
    crawl(
        str(links_file.as_uri()),
        f"{follow_url_params_tempdir}/follow_url_params.jl",
        allowed_domains=[str(links_file), "example.com"],
        custom_settings={"ROBOTSTXT_OBEY": False},
        follow_links=True,
    )

    follow_url_params_df = pd.read_json(
        f"{follow_url_params_tempdir}/follow_url_params.jl", lines=True
    )

    def test_follow_url_params_followed():
        assert follow_url_params_df["url"].str.contains("?", regex=False).any()


with TemporaryDirectory() as dont_follow_url_params_tempdir:
    crawl(
        str(links_file.as_uri()),
        f"{dont_follow_url_params_tempdir}/dont_follow_url_params.jl",
        allowed_domains=[str(links_file), "example.com"],
        custom_settings={"ROBOTSTXT_OBEY": False},
        follow_links=True,
        exclude_url_params=True,
    )
    dont_follow_url_params_df = pd.read_json(
        f"{dont_follow_url_params_tempdir}/dont_follow_url_params.jl", lines=True
    )

    def test_dont_follow_url_params_not_followed():
        assert not dont_follow_url_params_df["url"].str.contains("?", regex=False).all()


with TemporaryDirectory() as dup_links_file_tempdir:
    crawl(
        str(dup_links_file.as_uri()),
        f"{dup_links_file_tempdir}/dup_links_crawl.jl",
        custom_settings={"ROBOTSTXT_OBEY": False},
    )
    dup_crawl_df = pd.read_json(
        f"{dup_links_file_tempdir}/dup_links_crawl.jl", lines=True
    )
    dup_links_test = ["https://example_a.com" for i in range(5)] + [
        "https://example.com"
    ]

    dup_text_test = [
        "Link Text A",
        "Link Text A",
        "Link Text A",
        "Link Text B",
        "Link Text C",
        "Link Other",
    ]

    dup_nf_test = ["True"] + ["False" for i in range(5)]

    def test_duplicate_links_counted_propery():
        assert dup_crawl_df["links_url"].str.split("@@")[0] == dup_links_test
        assert dup_crawl_df["links_text"].str.split("@@")[0] == dup_text_test
        assert dup_crawl_df["links_nofollow"].str.split("@@")[0] == dup_nf_test

    def test_non_existent_links_are_NA():
        assert "nav_links_url" not in dup_crawl_df
        assert "nav_links_text" not in dup_crawl_df
        assert "header_links_url" not in dup_crawl_df
        assert "footer_links_url" not in dup_crawl_df


with TemporaryDirectory() as broken_links_tempdir:
    crawl(
        [str(broken_links_file.as_uri()), "wrong_url"],
        f"{broken_links_tempdir}/broken_links_crawl.jl",
        follow_links=True,
    )

    def test_broken_links_are_reported():
        broken_links_df = pd.read_json(
            f"{broken_links_tempdir}/broken_links_crawl.jl", lines=True
        )
        assert "errors" in broken_links_df
        assert "wrong_url" not in broken_links_df["url"]

    def test_crawling_bad_url_directly_is_handled():
        crawl(
            ["wrong_url", "https://example.com"], f"{broken_links_tempdir}/bad_url.jl"
        )
        bad_url_df = pd.read_json(f"{broken_links_tempdir}/bad_url.jl", lines=True)
        assert len(bad_url_df) == 1
        assert bad_url_df["url"][0] == "https://example.com"
