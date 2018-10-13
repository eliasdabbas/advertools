import logging
import os
from itertools import product

import pandas as pd
import pytest

from advertools.serp import (serp_goog, VALID_VALUES,
                             _dict_product, set_logging_level)

goog_cse_cx = os.environ.get('GOOG_CSE_CX')
goog_cse_key = os.environ.get('GOOG_CSE_KEY')


def test_dict_product_produces_correct_result():
    d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [10, 20]}
    dp = _dict_product(d)
    assert (list(product(*d.values())) ==
            [tuple(x.values()) for x in dp])
    assert ([tuple(x.keys()) for x in dp] ==
            [tuple(d.keys()) for x in range(len(dp))])


def test_dict_product_return_correct_types():
    d = {'a': [1], 'b': [10, 20, 30], 'c': (4, 5, 6)}
    dp = _dict_product(d)
    assert isinstance(dp, list)
    assert [isinstance(x, dict) for x in dp]
    assert len(dp) == len(list(product(*d.values())))


def test_serp_goog_raises_error_on_invalid_args():
    with pytest.raises(ValueError):
        for val in VALID_VALUES:
            params = {val: 'WRONG VALUE'}
            serp_goog(q='q', cx='cx', key='key', **params)


def test_serp_goog_return_correct_result():
    result = serp_goog(q='testing hotels', cx=goog_cse_cx,
                       key=goog_cse_key, searchType=['image', None])
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'title' in result
    assert 'image' in result
    assert len(result) == 20


def test_serp_goog_handles_no_search_results():
    q = 'aquerythatdoesntgetrezultssss'
    result = serp_goog(q=q, cx=goog_cse_cx, key=goog_cse_key,
                       cr='countryRU', hl='zh-TW', gl='nf')
    assert len(result) == 1
    assert result['searchTerms'].values[0] == q


def test_correctly_changing_log_levels():
    lvl_names_values = [0, 10, 20, 30, 40, 50]
    for level in lvl_names_values:
        set_logging_level(level)
        assert logging.getLogger().level == level
    with pytest.raises(ValueError):
        set_logging_level('WRONG VALUE')
