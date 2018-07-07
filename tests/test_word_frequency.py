from advertools.word_frequency import word_frequency
import advertools as adv
import pandas as pd

import pytest

sep_list = [None, ' ', '-', '_']

text_list = [
    'one two',
    'one two  three',
    'one-two-three',
    'one_two_three',
    'four five',
    'four five',
    'four six'
]

num_list = [
    100, 
    200,
    300,
    400,
    500,
    600,
    700
]

def test_len_result_one_more_than_len_slots():
    for sep in sep_list:
        result = word_frequency(text_list, num_list, sep=sep)
        if sep is not None:
            assert sep not in result['word']

def test_rm_words_removed():
    result = word_frequency(text_list, num_list, rm_words=['one', 'two'])
    assert 'one' not in result['word']
    assert 'two' not in result['word']
