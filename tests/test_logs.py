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
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "nginx_access.log"),
            str(path / "delete_output.parquet"),
            path / "delete_errors.txt",
            "combined",
        )
        result = pd.read_parquet(path / "delete_output.parquet")
        assert result.filter(regex="referer|user_agent").columns.tolist() == [
            "referer",
            "user_agent",
        ]


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
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "combined_no_errors.log"),
            str(path / "delete_output.parquet"),
            path / "delete_errors.txt",
            "combined",
        )
        assert not os.path.exists(path / "delete_errors.txt")


def test_logstodf_parses_dates():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "nginx_access.log"),
            str(path / "delete_output.parquet"),
            path / "delete_errors.txt",
            "combined",
        )
        result = pd.read_parquet(path / "delete_output.parquet")
        assert "datetime" in result["datetime"].dtype.name


def test_logstodf_parses_custom_date_fmt():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "nginx_custom_date.log"),
            str(path / "delete_output.parquet"),
            path / "delete_errors.txt",
            "combined",
            date_format="%B %d, %YT%H:%M:%S %z",
        )
        result = pd.read_parquet(path / "delete_output.parquet")
        assert "datetime" in result["datetime"].dtype.name


def test_logstodf_parses_raises_wrong_date_fmt():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        logs_to_df(
            full_local_path("logs_testing", "nginx_custom_date.log"),
            str(path / "delete_output.parquet"),
            path / "delete_errors.txt",
            "combined",
            date_format="%B %, M:%S %z",
        )
        result = pd.read_parquet(path / "delete_output.parquet")
        assert "datetime" not in result["datetime"].dtype.name


def test_logstodf_raises_on_no_fields():
    """Raise an exception if user proivides custom log format without fields."""
    with pytest.raises(ValueError):
        logs_to_df(
            log_file="some_file.txt",
            output_file="output_file.parquet",
            errors_file="errors.txt",
            log_format="custom_regex",
            fields=None,
        )
