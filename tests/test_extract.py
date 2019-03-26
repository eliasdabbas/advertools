import pytest

from advertools.extract import (extract, extract_currency, extract_emoji,
                                extract_hashtags, extract_intense_words,
                                extract_mentions, extract_questions,
                                extract_words)

mention_posts = ['hello @name', 'email@domain.com', '@oneword',
                 'hi @nam-e and @name', '@first @last', 'an @under_score',
                 'a @dot.one', 'non latin @مرحبا', 'other at ＠sign',
                 '@one.@two three', 'number @123text', '@_before @after_']

mention_summary = extract_mentions(mention_posts)

mention_test_keys = ['mentions', 'mentions_flat', 'mention_counts',
                     'mention_freq', 'top_mentions', 'overview']

hashtag_posts = ['hello #name', 'email#domain.com', '#oneword',
                 'hi #nam-e and #name', '#first #last', 'an #under_score',
                 'a #dot.one', 'non latin #مرحبا', 'other hash ＃sign',
                 '#one.#two three', 'number #123text', '#_before #after_']

hashtag_summary = extract_hashtags(hashtag_posts)
hashtag_test_keys = ['hashtags', 'hashtags_flat', 'hashtag_counts',
                     'hashtag_freq', 'top_hashtags', 'overview']

emoji_posts = ['one smiley 😀', 'one smiley 😀 one wink 😉', 'no emoji']
emoji_summary = extract_emoji(emoji_posts)
emoji_test_keys = ['emoji', 'emoji_text', 'emoji_flat', 'emoji_flat_text',
                   'emoji_counts', 'emoji_freq', 'top_emoji', 'top_emoji_text',
                   'overview']

word_posts = ['today it is raining', 'i like rain and raining',
              'today it is snowing', 'now snowing and raining',
              'training is good with snow', 'RaIn and SNoW',
              'none of the words', '@rain, #snow rain']

word_summary_full = extract_words(word_posts, ['rain', 'snow'], True)
word_summary_not_full = extract_words(word_posts, ['rain', 'snow'], False)
word_test_keys = ['words', 'words_flat', 'word_counts',
                  'word_freq', 'top_words', 'overview']


currency_posts = ['$5.0 beginning', 'mid £5.0 price', 'end of str €',
                  'more $ than £ one', 'other symbols ₣ ₤ ₥ ₦ ₧',
                  'no symbols']

currency_summary = extract_currency(currency_posts)

currency_test_keys = ['currency_symbols', 'currency_symbols_flat',
                      'currency_symbol_counts', 'currency_symbol_freq',
                      'top_currency_symbols', 'overview',
                      'currency_symbol_names', 'surrounding_text']


intense_word_posts = ['i looooove this', 'goooood mooorning',
                      'normal text', 'in thhhhhhe middle',
                      'innnnnn the beginning', 'at the end!!!!!!']

intense_word_summary = extract_intense_words(intense_word_posts)

intense_word_test_keys = ['intense_words', 'intense_words_flat',
                          'intense_word_counts', 'intense_word_freq',
                          'top_intense_words', 'overview']


question_posts = ['how are you?', 'no question', 'no! what about you?',
                  'Hola, ¿cómo estás?', 'Πώς είσαι;']

question_summary = extract_questions(question_posts)

question_test_keys = ['question_marks', 'question_marks_flat',
                      'question_mark_counts', 'question_mark_freq',
                      'top_question_marks', 'overview',
                      'question_mark_names', 'question_text']


def test_mention_result_has_correct_keys():
    assert set(mention_summary.keys()) == set(mention_test_keys)


def test_correct_mentions_extracted():
    assert mention_summary['mentions'] == [['@name'], [], ['@oneword'],
                                           ['@nam', '@name'],
                                           ['@first', '@last'],
                                           ['@under_score'], ['@dot'], [],
                                           ['＠sign'], ['@one', '@two'],
                                           ['@123text'],
                                           ['@_before', '@after_']]


def test_correct_flat_mentions():
    assert mention_summary['mentions_flat'] == ['@name', '@oneword', '@nam',
                                                '@name', '@first', '@last',
                                                '@under_score', '@dot',
                                                '＠sign', '@one', '@two',
                                                '@123text', '@_before',
                                                '@after_']


def test_correct_mention_counts():
    assert mention_summary['mention_counts'] == [1, 0, 1, 2, 2, 1, 1, 0,
                                                 1, 2, 1, 2]


def test_correct_mention_freq():
    assert mention_summary['mention_freq'] == [(0, 2), (1, 6), (2, 4)]


def test_correct_top_mentions():
    assert set(mention_summary['top_mentions']) == {('@name', 2),
                                                    ('@oneword', 1),
                                                    ('@nam', 1), ('@first', 1),
                                                    ('@last', 1),
                                                    ('@under_score', 1),
                                                    ('@dot', 1), ('＠sign', 1),
                                                    ('@one', 1), ('@two', 1),
                                                    ('@123text', 1),
                                                    ('@_before', 1),
                                                    ('@after_', 1)}


def test_correct_mention_overview():
    mention_overview = mention_summary['overview']
    assert mention_overview['num_posts'] == 12
    assert mention_overview['num_mentions'] == 14
    assert mention_overview['mentions_per_post'] == 14/12
    assert mention_overview['unique_mentions'] == 13


def test_hashtag_result_has_correct_keys():
    assert set(hashtag_summary.keys()) == set(hashtag_test_keys)


def test_correct_hashtags_extracted():
    assert hashtag_summary['hashtags'] == [['#name'], [], ['#oneword'],
                                           ['#nam', '#name'],
                                           ['#first', '#last'],
                                           ['#under_score'], ['#dot'],
                                           ['#مرحبا'], ['＃sign'],
                                           ['#one', '#two'], ['#123text'],
                                           ['#_before', '#after_']]


def test_correct_flat_hashtags():
    assert hashtag_summary['hashtags_flat'] == ['#name', '#oneword', '#nam',
                                                '#name', '#first', '#last',
                                                '#under_score', '#dot',
                                                '#مرحبا', '＃sign', '#one',
                                                '#two', '#123text', '#_before',
                                                '#after_']


def test_correct_hashtag_counts():
    assert hashtag_summary['hashtag_counts'] == [1, 0, 1, 2, 2, 1,
                                                 1, 1, 1, 2, 1, 2]


def test_correct_hashtag_freq():
    assert hashtag_summary['hashtag_freq'] == [(0, 1), (1, 7), (2, 4)]


def test_correct_top_hashtags():
    assert set(hashtag_summary['top_hashtags']) == {('#name', 2),
                                                    ('#oneword', 1),
                                                    ('#nam', 1), ('#first', 1),
                                                    ('#last', 1),
                                                    ('#under_score', 1),
                                                    ('#dot', 1), ('＃sign', 1),
                                                    ('#one', 1), ('#two', 1),
                                                    ('#123text', 1),
                                                    ('#مرحبا', 1),
                                                    ('#_before', 1),
                                                    ('#after_', 1)}


def test_correct_hashtag_overview():
    hashtag_overview = hashtag_summary['overview']
    assert hashtag_overview['num_posts'] == 12
    assert hashtag_overview['num_hashtags'] == 15
    assert hashtag_overview['hashtags_per_post'] == 15/12
    assert hashtag_overview['unique_hashtags'] == 14


def test_extract_puts_str_in_list():
    result = extract('#one #two #three', regex=r'#\w+', key_name='hashtag')
    assert result['hashtags'] == ['#one #two #three'.split()]


def test_emoji_result_has_correct_keys():
    assert set(emoji_summary.keys()) == set(emoji_test_keys)


def test_correct_emoji_extracted():
    assert emoji_summary['emoji'] == [['😀'], ['😀', '😉'], []]


def test_correct_flat_emoji():
    assert emoji_summary['emoji_flat'] == ['😀', '😀', '😉']


def test_correct_emoji_counts():
    assert emoji_summary['emoji_counts'] == [1, 2, 0]


def test_correct_emoji_freq():
    assert emoji_summary['emoji_freq'] == [(0, 1), (1, 1), (2, 1)]


def test_correct_top_emoji():
    assert emoji_summary['top_emoji'] == [('😀', 2), ('😉', 1)]


def test_correct_emoji_overview():
    emoji_overview = emoji_summary['overview']
    assert emoji_overview['num_posts'] == 3
    assert emoji_overview['num_emoji'] == 3
    assert emoji_overview['emoji_per_post'] == 1.0
    assert emoji_overview['unique_emoji'] == 2


def test_word_result_has_correct_keys():
    assert set(word_summary_full.keys()) == set(word_test_keys)
    assert set(word_summary_not_full.keys()) == set(word_test_keys)


def test_correct_words_extracted():
    assert word_summary_full['words'] == [[], ['rain'], [], [], ['snow'],
                                          ['rain', 'snow'], [],
                                          ['rain', 'snow', 'rain']]
    assert word_summary_not_full['words'] == [['raining'], ['rain', 'raining'],
                                              ['snowing'],
                                              ['snowing', 'raining'],
                                              ['training', 'snow'],
                                              ['rain', 'snow'], [],
                                              ['@rain,', '#snow', 'rain']]


def test_correct_flat_words():
    assert word_summary_full['words_flat'] == ['rain', 'snow', 'rain', 'snow',
                                               'rain', 'snow', 'rain']
    assert word_summary_not_full['words_flat'] == ['raining', 'rain',
                                                   'raining', 'snowing',
                                                   'snowing', 'raining',
                                                   'training', 'snow', 'rain',
                                                   'snow', '@rain,', '#snow',
                                                   'rain']


def test_correct_word_counts():
    assert word_summary_full['word_counts'] == [0, 1, 0, 0, 1, 2, 0, 3]
    assert word_summary_not_full['word_counts'] == [1, 2, 1, 2, 2, 2, 0, 3]


def test_correct_word_freq():
    assert word_summary_full['word_freq'] == [(0, 4), (1, 2), (2, 1), (3, 1)]
    assert word_summary_not_full['word_freq'] == [(0, 1), (1, 2),
                                                  (2, 4), (3, 1)]


def test_correct_top_words():
    assert set(word_summary_full['top_words']) == {('rain', 4), ('snow', 3)}
    assert set(word_summary_not_full['top_words']) == {('rain', 3),
                                                       ('raining', 3),
                                                       ('snow', 2),
                                                       ('snowing', 2),
                                                       ('#snow', 1),
                                                       ('@rain,', 1),
                                                       ('training', 1)}


def test_correct_word_overview():
    word_overview_full = word_summary_full['overview']
    assert word_overview_full['num_posts'] == 8
    assert word_overview_full['num_words'] == 7
    assert word_overview_full['words_per_post'] == 7/8
    assert word_overview_full['unique_words'] == 2

    word_overview_not_full = word_summary_not_full['overview']
    assert word_overview_not_full['num_posts'] == 8
    assert word_overview_not_full['num_words'] == 13
    assert word_overview_not_full['words_per_post'] == 13 / 8
    assert word_overview_not_full['unique_words'] == 7


def test_extract_words_puts_str_in_list():
    word_summary_str = extract_words(word_posts, 'rain',  True)
    assert word_summary_str['top_words'][0][0] == 'rain'


def test_extract_changes_str_to_compiled_regex():
    result = extract(['text', 'list'], 'list', 'key')
    assert result['top_keys'][0][0] == 'list'


def test_currency_result_has_correct_keys():
    assert set(currency_summary.keys()) == set(currency_test_keys)


def test_correct_currencies_extracted():
    assert currency_summary['currency_symbols'] == [['$'], ['£'], ['€'],
                                                    ['$', '£'],
                                                    ['₣', '₤', '₥', '₦', '₧'],
                                                    []]


def test_correct_flat_currencies():
    assert currency_summary['currency_symbols_flat'] == ['$', '£', '€', '$',
                                                         '£', '₣', '₤', '₥',
                                                         '₦', '₧']


def test_correct_currency_counts():
    assert currency_summary['currency_symbol_counts'] == [1, 1, 1, 2, 5, 0]


def test_correct_currency_freq():
    assert currency_summary['currency_symbol_freq'] == [(0, 1), (1, 3),
                                                        (2, 1), (5, 1)]


def test_correct_top_currencies():
    assert set(currency_summary['top_currency_symbols']) == {('$', 2),
                                                             ('£', 2),
                                                             ('€', 1),
                                                             ('₣', 1),
                                                             ('₤', 1),
                                                             ('₥', 1),
                                                             ('₦', 1),
                                                             ('₧', 1)}


def test_correct_currency_names():
    assert currency_summary['currency_symbol_names'] == [['dollar sign'],
                                                         ['pound sign'],
                                                         ['euro sign'],
                                                         ['dollar sign',
                                                          'pound sign'],
                                                         ['french franc sign',
                                                          'lira sign',
                                                          'mill sign',
                                                          'naira sign',
                                                          'peseta sign'],
                                                         []]


currency_posts = ['$5.0 beginning', 'mid £5.0 price', 'end of str €',
                  'more $ than £ one', 'other symbols ₣ ₤ ₥ ₦ ₧',
                  'no symbols']


def test_correct_currency_surrounding_text():
    assert currency_summary['surrounding_text'] == [['$5.0 beginning'],
                                                    ['mid £5.0 price'],
                                                    ['end of str €'],
                                                    ['more $ than £ one'],
                                                    ['other symbols '
                                                     '₣ ₤ ₥ ₦ ₧'],
                                                    []]


def test_correct_currency_overview():
    currency_overview = currency_summary['overview']
    assert currency_overview['num_posts'] == 6
    assert currency_overview['num_currency_symbols'] == 10
    assert currency_overview['currency_symbols_per_post'] == 10/6
    assert currency_overview['unique_currency_symbols'] == 8


def test_intense_word_result_has_correct_keys():
    assert set(intense_word_summary.keys()) == set(intense_word_test_keys)


def test_correct_intense_words_extracted():
    assert intense_word_summary['intense_words'] == [['looooove'],
                                                     ['goooood', 'mooorning'],
                                                     [], ['thhhhhhe'],
                                                     ['innnnnn'],
                                                     ['end!!!!!!']]


def test_correct_flat_intense_words():
    assert intense_word_summary['intense_words_flat'] == ['looooove',
                                                          'goooood',
                                                          'mooorning',
                                                          'thhhhhhe',
                                                          'innnnnn',
                                                          'end!!!!!!']


def test_correct_intense_word_counts():
    assert intense_word_summary['intense_word_counts'] == [1, 2, 0, 1, 1, 1]


def test_correct_intense_word_freq():
    assert intense_word_summary['intense_word_freq'] == [(0, 1), (1, 4),
                                                         (2, 1)]


def test_correct_top_intense_words():
    assert set(intense_word_summary['top_intense_words']) == {('looooove', 1),
                                                              ('goooood', 1),
                                                              ('mooorning', 1),
                                                              ('thhhhhhe', 1),
                                                              ('innnnnn', 1),
                                                              ('end!!!!!!', 1)}


def test_correct_intense_word_overview():
    intense_word_overview = intense_word_summary['overview']
    assert intense_word_overview['num_posts'] == 6
    assert intense_word_overview['num_intense_words'] == 6
    assert intense_word_overview['intense_words_per_post'] == 1/1
    assert intense_word_overview['unique_intense_words'] == 6


def test_question_result_has_correct_keys():
    assert set(question_summary.keys()) == set(question_test_keys)


def test_correct_questions_extracted():
    assert question_summary['question_marks'] == [['?'], [], ['?'],
                                                  ['¿', '?'], [';']]


def test_correct_flat_question_marks():
    assert question_summary['question_marks_flat'] == ['?', '?', '¿', '?', ';']


def test_correct_question_counts():
    assert question_summary['question_mark_counts'] == [1, 0, 1, 2, 1]


def test_correct_question_freq():
    assert question_summary['question_mark_freq'] == [(0, 1), (1, 3), (2, 1)]


def test_correct_top_question_marks():
    assert set(question_summary['top_question_marks']) == {('¿', 1), ('?', 3),
                                                           (';', 1)}


def test_correct_question_overview():
    question_overview = question_summary['overview']
    assert question_overview['num_posts'] == 5
    assert question_overview['num_question_marks'] == 5
    assert question_overview['question_marks_per_post'] == 1/1
    assert question_overview['unique_question_marks'] == 3
