import os

import pandas as pd
import pytest
from advertools.logs import crawllogs_to_df, logs_to_df


def full_local_path(folder, file):
    tests_dir = f'tests/data/{folder}/'
    return os.path.abspath(tests_dir + file)


def test_crawllogs_returns_df():
    for logfile in os.listdir('tests/data/logs_testing'):
        result = crawllogs_to_df(full_local_path('logs_testing', logfile))
        assert isinstance(result, pd.core.frame.DataFrame)


def test_logstodf_raises_on_wrong_output_file():
    with pytest.raises(ValueError):
        logs_to_df('logfile.log', 'output.wrong', 'errors.txt', 'common')


with open('delete_me_now.parquet', 'w') as parquetfile:
    parquetfile.write('')


def test_logstodf_raises_on_existing_parquet_file():
    with pytest.raises(ValueError):
        logs_to_df('logfile.log', 'delete_me_now.parquet', 'errors.txt', 'common')
        os.remove('delete_me_now.parquet')


with open('delete_me_now.csv', 'w') as errorfile:
    errorfile.write('')


def test_logstodf_raises_on_existing_error_file():
    with pytest.raises(ValueError):
        logs_to_df('logfile.log', 'output.parquet', 'delete_me_now.csv', 'common')
        os.remove('delete_me_now.csv')

def test_logstodf_general_output_correctness():
    logs_to_df(full_local_path('logs_testing', 'nginx_access.log'),
               'delete_output.parquet',
               'delete_errors.txt',
               'combined')
    result = pd.read_parquet('delete_output.parquet')
    assert 'referer' in result
    assert 'user_agent' in result
    assert isinstance(result, pd.DataFrame)
    os.remove('delete_output.parquet')
    os.remove('delete_errors.txt')
