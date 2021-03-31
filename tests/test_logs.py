import os
import pandas as pd
from advertools.logs import crawllogs_to_df


def full_local_path(folder, file):
    tests_dir = f'tests/data/{folder}/'
    return os.path.abspath(tests_dir + file)


def test_crawllogs_returns_df():
    for logfile in os.listdir('tests/data/logs_testing'):
        result = crawllogs_to_df(full_local_path('logs_testing', logfile))
        assert isinstance(result, pd.core.frame.DataFrame)
