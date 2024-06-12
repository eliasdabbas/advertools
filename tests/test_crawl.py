import os
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
