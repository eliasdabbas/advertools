from advertools.word_frequency import word_frequency


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


def test_rm_words_removed():
    result = word_frequency(text_list, num_list, rm_words=['one', 'two'])
    assert not result['word'].eq('one').any()
    assert not result['word'].eq('two').any()


def test_extra_info_not_provided():
    result = word_frequency(text_list, num_list, extra_info=False)
    assert set(result.columns.values) == {'word', 'abs_freq', 'wtd_freq',
                                          'rel_value'}


def test_extra_info_provided():
    result = word_frequency(text_list, num_list, extra_info=True)
    assert set(result.columns.values) == {'word', 'abs_freq', 'abs_perc',
                                          'abs_perc_cum', 'wtd_freq',
                                          'wtd_freq_perc', 'wtd_freq_perc_cum',
                                          'rel_value'}


def test_works_fine_with_only_stopwords_supplied():
    result = word_frequency(['on'], [3])
    assert result.shape == (0, 4)


def test_works_without_numlist_provided():
    result = word_frequency(['Great Text in a List', 'Greater text as well'])
    assert result['word'].eq('text').any()


def test_word_freq_uses_regex():
    result = word_frequency(['pizza burger', 'pizza sandwitch'], regex='pizza')
    assert result['word'][0] == 'pizza'


def test_word_freq_returns_two_cols_if_not_num_list():
    result = word_frequency(['pizza burger', 'pizza sandwitch'])
    assert result.shape[1] == 2
