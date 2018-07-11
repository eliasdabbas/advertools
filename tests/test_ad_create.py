from advertools.ad_create import ad_create

import pytest


def test_raises_error_for_long_input_strings():
    with pytest.raises(ValueError):
        ad_create('short template {}', ['one', 'two', 'three'],
                  'very long fallback string', 20)
    with pytest.raises(ValueError):
        ad_create('very long template string {}', ['one', 'two', 'three'],
                  'short', 20)


def test_all_replacements_used():
    replacements = ['one', 'two', 'three']
    result = ad_create('Hello {}', replacements, 'fallback', capitalize=False)
    assert all([rep in ' '.join(result) for rep in replacements])


def test_fallback_used_if_string_long():
    replacements = ['one', 'two', 'three hundrend thousand']
    result = ad_create('Hello {}', replacements, 'fallback', max_len=20,
                       capitalize=False)
    assert result == ['Hello one', 'Hello two', 'Hello fallback']


def test_final_string_capitalized_or_not():
    capitalized = ad_create('heLLo {}', ['ONE', 'tWo', 'tHree', 'Four'],
                            'fallback', capitalize=True)
    not_capitalized = ad_create('heLLo {}', ['ONE', 'tWo', 'tHree', 'Four'],
                                'fallback', capitalize=False)
    assert capitalized == ['Hello One', 'Hello Two', 'Hello Three',
                           'Hello Four']
    assert not_capitalized == ['heLLo ONE', 'heLLo tWo', 'heLLo tHree',
                               'heLLo Four']
