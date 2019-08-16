import logging
import os
from itertools import product

import pandas as pd
import pytest

from advertools.serp import (serp_goog, serp_youtube, SERP_GOOG_VALID_VALS,
                             SERP_YTUBE_VALID_VALS, youtube_channel_details,
                             youtube_video_details, YOUTUBE_VID_CATEGORY_IDS,
                             YOUTUBE_TOPIC_IDS, _dict_product,
                             set_logging_level)

goog_cse_cx = os.environ.get('GOOG_CSE_CX')
goog_cse_key = os.environ.get('GOOG_CSE_KEY')
youtube_key = os.environ.get('GOOG_CSE_KEY')


def test_dict_product_produces_correct_result():
    d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [10, 20]}
    dp_exp = [
        {'a': 1, 'b': 4, 'c': 10},
        {'a': 1, 'b': 4, 'c': 20},
        {'a': 1, 'b': 5, 'c': 10},
        {'a': 1, 'b': 5, 'c': 20},
        {'a': 1, 'b': 6, 'c': 10},
        {'a': 1, 'b': 6, 'c': 20},
        {'a': 2, 'b': 4, 'c': 10},
        {'a': 2, 'b': 4, 'c': 20},
        {'a': 2, 'b': 5, 'c': 10},
        {'a': 2, 'b': 5, 'c': 20},
        {'a': 2, 'b': 6, 'c': 10},
        {'a': 2, 'b': 6, 'c': 20},
        {'a': 3, 'b': 4, 'c': 10},
        {'a': 3, 'b': 4, 'c': 20},
        {'a': 3, 'b': 5, 'c': 10},
        {'a': 3, 'b': 5, 'c': 20},
        {'a': 3, 'b': 6, 'c': 10},
        {'a': 3, 'b': 6, 'c': 20}
    ]
    dp_res = _dict_product(d)
    for d_res in dp_res:
        assert d_res in dp_exp


def test_dict_product_return_correct_types():
    d = {'a': [1], 'b': [10, 20, 30], 'c': (4, 5, 6)}
    dp = _dict_product(d)
    assert isinstance(dp, list)
    assert [isinstance(x, dict) for x in dp]
    assert len(dp) == len(list(product(*d.values())))


# Google search tests:
def test_serp_goog_raises_error_on_invalid_args():
    with pytest.raises(ValueError):
        for val in SERP_GOOG_VALID_VALS:
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


def test_serp_raises_error_on_wrong_key():
    with pytest.raises(Exception):
        serp_goog(q='test credit cart', cx=goog_cse_cx, key='wrong key')


def test_serp_goog_restult_df_contains_all_provided_params():
    keys_vals_to_test = {k: list(SERP_GOOG_VALID_VALS[k])[0] for k in SERP_GOOG_VALID_VALS}
    for key, val in keys_vals_to_test.items():
        result = serp_goog(cx=goog_cse_cx, key=goog_cse_key, q='fashion', **{key: val})
        if key == 'searchType':
            continue
        assert key in result.columns
        if key == 'filter':
            val = str(val)
        assert result[key].iloc[0] == val


# YouTube search tests:
def test_serp_youtube_raises_error_on_invalid_args():
    with pytest.raises(ValueError):
        for val in SERP_YTUBE_VALID_VALS:
            params = {val: 'WRONG VALUE'}
            serp_youtube(q='q', key='key', **params)


def test_serp_youtube_return_correct_result():
    result = serp_youtube(q=['testing hotels', 'testing computers'],
                          key=youtube_key, order='date')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'title' in result
    assert 'rank' in result
    assert len(result) <= 10


def test_serp_youtube_handles_no_search_results():
    q = 'aquerythatdoesntgetrezultssss'
    result = serp_youtube(q=q, key=youtube_key,
                          relevanceLanguage='ar')
    assert len(result) == 1
    assert result['q'].values[0] == q


def test_serp_youtube_raises_type_video_error():
    with pytest.raises(Exception):
        serp_youtube(key=youtube_key, videoEmbeddable=True)


def test_serp_youtube_raises_response_error():
    with pytest.raises(Exception):
        serp_youtube(key=youtube_key, publishedAfter='wrong date fmt')


def test_correctly_changing_log_levels():
    lvl_names_values = [0, 10, 20, 30, 40, 50]
    for level in lvl_names_values:
        set_logging_level(level)
        assert logging.getLogger().level == level
    with pytest.raises(ValueError):
        set_logging_level('WRONG VALUE')


def test_youtube_video_details_raises_error():
    with pytest.raises(Exception):
        youtube_video_details(key='WRONG KEY',
                              vid_ids='wrong ID')


def test_youtube_channel_details_raises_error():
    with pytest.raises(Exception):
        youtube_channel_details(key='WRONG KEY',
                                channel_ids='wrong ID')
