import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from advertools.logs import crawllogs_to_df, logs_to_df


def full_local_path(folder, file):
    tests_dir = f"tests/data/{folder}/"
    return os.path.abspath(tests_dir + file)


@pytest.mark.parametrize(
    "logfile",
    [f for f in os.listdir("tests/data/logs_testing") if f.startswith("crawl")],
)
def test_crawllogs_returns_df(logfile):
    result = crawllogs_to_df(full_local_path("logs_testing", logfile))
    assert isinstance(result, pd.core.frame.DataFrame)


def test_logstodf_raises_on_wrong_output_file():
    with pytest.raises(ValueError):
        logs_to_df("logfile.log", "output.wrong", "errors.txt", "common")


def test_logstodf_general_output_correctness():
    logs_to_df(
        full_local_path("logs_testing", "nginx_access.log"),
        "delete_output.parquet",
        "delete_errors.txt",
        "combined",
    )
    result = pd.read_parquet("delete_output.parquet")
    assert "referer" in result
    assert "user_agent" in result
    assert isinstance(result, pd.DataFrame)
    os.remove("delete_output.parquet")
    os.remove("delete_errors.txt")


def test_logs_raises_for_wrong_encoding():
    with pytest.raises(UnicodeDecodeError):
        logs_to_df(
            full_local_path("logs_testing", "combined_latin1_enc.log"),
            "test_output.parquet",
            "test_errors.txt",
            "combined",
            encoding="utf-8",
        )


def test_logs_parses_with_correct_encoding():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "combined_latin1_enc.log"),
            str(path / "test_output.parquet"),
            path / "test_errors.txt",
            "combined",
            encoding="latin1",
        )
        result = pd.read_parquet(path / "test_output.parquet")
        assert isinstance(result, pd.DataFrame)


def test_logs_nginx_error():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "nginx_error.log"),
            str(path / "test_output.parquet"),
            path / "test_errors.txt",
            "nginx_error",
            encoding="latin1",
        )
        result = pd.read_parquet(path / "test_output.parquet")
        assert isinstance(result, pd.DataFrame)


def test_logs_apache_error():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "apache_error.log"),
            str(path / "test_output.parquet"),
            path / "test_errors.txt",
            "nginx_error",
            encoding="latin1",
        )
        result = pd.read_parquet(path / "test_output.parquet")
        assert isinstance(result, pd.DataFrame)


def test_logs_file_without_errors():
    logs_to_df(
        full_local_path("logs_testing", "combined_no_errors.log"),
        "delete_output.parquet",
        "delete_errors.txt",
        "combined",
    )
    assert not os.path.exists("delete_errors.txt")
