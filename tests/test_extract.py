import pytest

from advertools.extract import * # (extract, extract_currency, extract_emoji,
#                                 extract_exclamations, extract_hashtags,
#                                 extract_intense_words, extract_mentions,
#                                 extract_questions, extract_words, extract_urls)
from advertools.emoji import *

number_posts = ['before123,000', '123after', 'comma 123,456', 'dot 123.234.3',
                'skip 123-', 'nothing', 'two 123 456,789']

number_summary = extract_numbers(number_posts)

number_test_keys = ['numbers', 'numbers_flat', 'number_counts',
                     'number_freq', 'top_numbers', 'overview']

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
                   'top_emoji_groups', 'top_emoji_sub_groups', 'overview']

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

exclamation_posts = ['how dare you!', 'no exclamation', 'no! do not do this!',
                     '¡Hola!  ¿cómo estás?', 'مرحبا. لا تذهب!']

exclamation_summary = extract_exclamations(exclamation_posts)

exclamation_test_keys = ['exclamation_marks', 'exclamation_marks_flat',
                         'exclamation_mark_counts', 'exclamation_mark_freq',
                         'top_exclamation_marks', 'overview',
                         'exclamation_mark_names', 'exclamation_text']

url_posts = ['one https://www.a.com', 'two www.a.com www.b.com',
             'nothing', 'long https://example.com/one?a=b#nothing']

url_summary = extract_urls(url_posts)

url_test_keys = ['urls', 'urls_flat', 'url_counts', 'url_freq',
                 'top_urls', 'overview', 'top_domains', 'top_tlds']

test_ids = [
    'currency',
    'emoji',
    'exclamation',
    'hashtag',
    'intense',
    'mention',
    'number',
    'question',
    'word_full',
    'word_not_full',
    'url',
]


summaries_keys = [
    (list(currency_summary.keys()), currency_test_keys),
    (list(emoji_summary.keys()), emoji_test_keys),
    (list(exclamation_summary.keys()), exclamation_test_keys),
    (list(hashtag_summary.keys()), hashtag_test_keys),
    (list(intense_word_summary.keys()), intense_word_test_keys),
    (list(mention_summary.keys()), mention_test_keys),
    (list(number_summary.keys()), number_test_keys),
    (list(question_summary.keys()), question_test_keys),
    (list(word_summary_full.keys()), word_test_keys),
    (list(word_summary_not_full.keys()), word_test_keys),
    (list(url_summary.keys()), url_test_keys),
]


@pytest.mark.parametrize('summary_key, test_key',
                         zip([x[0] for x in summaries_keys],
                             [x[1] for x in summaries_keys]),
                         ids=test_ids)
def test_has_correct_keys(summary_key, test_key):
    assert set(summary_key) == set(test_key)


summaries = {
    'currency': currency_summary,
    'emoji': emoji_summary,
    'exclamation': exclamation_summary,
    'hashtag': hashtag_summary,
    'intense': intense_word_summary,
    'mention': mention_summary,
    'number': number_summary,
    'question': question_summary,
    'word_full': word_summary_full,
    'word_not_full': word_summary_not_full,
    'url': url_summary,
}


summary_counts = {k: [d[key] for key in d if 'count' in key][0]
                  for k, d in summaries.items()}
test_counts = {
    'currency': [1, 1, 1, 2, 5, 0],
    'emoji': [1, 2, 0],
    'exclamation': [1, 0, 2, 2, 1],
    'hashtag': [1, 0, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2],
    'intense': [1, 2, 0, 1, 1, 1],
    'mention': [1, 0, 1, 2, 2, 1, 1, 0, 1, 2, 1, 2],
    'number': [1, 1, 1, 1, 10, 2],
    'question': [1, 0, 1, 2, 1],
    'word_full': [0, 1, 0, 0, 1, 2, 0, 3],
    'word_not_full': [1, 2, 1, 2, 2, 2, 0, 3],
    'url': [1, 2, 0, 1]
}


@pytest.mark.parametrize('summary_count, test_count',
                         zip(sorted(summary_counts.items()),
                             sorted(test_counts.items())),
                         ids=test_ids)
def test_has_correct_counts(summary_count, test_count):
    assert summary_count == summary_count


summary_freqs = {k: [d[key] for key in d if 'freq' in key][0]
                 for k, d in summaries.items()}

test_freqs = {
    'currency': [(0, 1), (1, 3), (2, 1), (5, 1)],
    'emoji': [(0, 1), (1, 1), (2, 1)],
    'exclamation': [(0, 1), (1, 2), (2, 2)],
    'hashtag': [(0, 1), (1, 7), (2, 4)],
    'intense': [(0, 1), (1, 4), (2, 1)],
    'mention': [(0, 2), (1, 6), (2, 4)],
    'number': [(0, 1), (1, 5), (2, 1)],
    'question': [(0, 1), (1, 3), (2, 1)],
    'word_full': [(0, 4), (1, 2), (2, 1), (3, 1)],
    'word_not_full': [(0, 1), (1, 2), (2, 4), (3, 1)],
    'url': [(0, 1), (1, 2), (2, 1)],
}


@pytest.mark.parametrize('summary_freq, test_freq',
                         zip(sorted(summary_freqs.items()),
                             sorted(test_freqs.items())),
                         ids=test_ids)
def test_has_correct_freq(summary_freq, test_freq):
    assert summary_freq == summary_freq


summary_flats = {k: [d[key] for key in d if 'flat' in key
                     and 'emoji_flat_text' not in key][0]
                 for k, d in summaries.items()}
test_flats = {
    'currency': ['$', '£', '€', '$', '£', '₣', '₤', '₥', '₦', '₧'],
    'emoji': ['😀', '😀', '😉'],
    'exclamation': ['!', '!', '!', '¡', '!', '!'],
    'hashtag': ['#name', '#oneword', '#nam', '#name', '#first', '#last',
                '#under_score', '#dot', '#مرحبا', '＃sign', '#one',
                '#two', '#123text', '#_before', '#after_'],
    'intense': ['looooove', 'goooood', 'mooorning', 'thhhhhhe',
                'innnnnn', 'end!!!!!!'],
    'mention': ['@name', '@oneword', '@nam', '@name', '@first',
                '@last', '@under_score', '@dot', '＠sign', '@one',
                '@two', '@123text', '@_before', '@after_'],
    'number': ['123,000', '123', '123,456', '123.234.3', '123',
               '123', '456,789'],
    'question': ['?', '?', '¿', '?', ';'],
    'word_full': ['rain', 'snow', 'rain', 'snow', 'rain', 'snow', 'rain'],
    'word_not_full': ['raining', 'rain', 'raining', 'snowing',
                      'snowing', 'raining', 'training', 'snow',
                      'rain', 'snow', '@rain,', '#snow', 'rain'],
    'url': ['https://www.a.com', 'http://www.a.com',
            'http://www.b.com', 'https://example.com/one?a=b#nothing']
}


@pytest.mark.parametrize('summary_flat, test_flat',
                         zip(sorted(summary_flats.items()),
                             sorted(test_flats.items())),
                         ids=test_ids)
def test_has_correct_flat(summary_flat, test_flat):
    assert summary_flat == test_flat


summary_tops = {k: [d[key] for key in d if 'top' in key]
                for k, d in summaries.items()}

summary_tops = {k: d[0] if len(d) == 1 else d
                for k, d in summary_tops.items()}

test_tops = {
    'currency': [('$', 2), ('£', 2), ('€', 1), ('₣', 1), ('₤', 1),
                 ('₥', 1), ('₦', 1), ('₧', 1)],
    'emoji': [[('😀', 2), ('😉', 1)],
              [('grinning face', 2), ('winking face', 1)],
              [('Smileys & Emotion', 3)],
              [('face-smiling', 3)]],
    'exclamation': [('!', 5), ('¡', 1)],
    'hashtag': [('#name', 2), ('#oneword', 1), ('#nam', 1),
                ('#first', 1), ('#last', 1), ('#under_score', 1),
                ('#dot', 1), ('#مرحبا', 1), ('＃sign', 1), ('#one', 1),
                ('#two', 1), ('#123text', 1), ('#_before', 1),
                ('#after_', 1)],
    'intense': [('looooove', 1), ('goooood', 1), ('mooorning', 1),
                ('thhhhhhe', 1), ('innnnnn', 1), ('end!!!!!!', 1)],
    'mention': [('@name', 2), ('@oneword', 1), ('@nam', 1), ('@first', 1),
                ('@last', 1), ('@under_score', 1), ('@dot', 1),
                ('＠sign', 1), ('@one', 1), ('@two', 1), ('@123text', 1),
                ('@_before', 1), ('@after_', 1)],
    'number': [('123', 3), ('123,000', 1), ('123,456', 1), ('123.234.3', 1),
               ('456,789', 1)],
    'question': [('?', 3), ('¿', 1), (';', 1)],
    'word_full': [('rain', 4), ('snow', 3)],
    'word_not_full': [('raining', 3), ('rain', 3), ('snowing', 2),
                      ('snow', 2), ('training', 1), ('@rain,', 1),
                      ('#snow', 1)],
    'url': [[('https://www.a.com', 1), ('http://www.a.com', 1),
             ('http://www.b.com', 1),
             ('https://example.com/one?a=b#nothing', 1)],
            [('www.a.com', 2), ('www.b.com', 1), ('example.com', 1)],
            [('com', 4)]]
}


def make_hashable(iterable):
    """Some sub-elements are lists and need to be converted sorted tuples."""
    return tuple(tuple(sorted(x)) if isinstance(x, list)else
                 x for x in iterable)


@pytest.mark.parametrize('summary_top, test_top',
                         zip(sorted(summary_tops.items()),
                             sorted(test_tops.items())),
                         ids=test_ids)
def test_has_correct_top(summary_top, test_top):
    assert (set(make_hashable(summary_top[1])) ==
            set(make_hashable(test_top[1])))


summary_overviews = {k: [d[key] for key in d if 'overview' in key][0]
                     for k, d in summaries.items()}

test_overviews = {
    'currency': [6, 10, 10/6, 8],
    'emoji': [3, 3, 1.0, 2],
    'exclamation': [5, 6, 1.2, 2],
    'hashtag': [12, 15, 1.25, 14],
    'intense': [6, 6, 1.0, 6],
    'mention': [12, 14, 14/12, 13],
    'number': [7, 7, 7/7, 5],
    'question': [5, 5, 1.0, 3],
    'word_full': [8, 7, 7/8, 2],
    'word_not_full': [8, 13, 13/8, 7],
    'url': [4, 4, 1.0, 4],
}


def dict2overview_list(d):
    """Convert an overview dict to a list based on its keys."""
    result = [0, 0, 0, 0]
    for key in d:
        if 'num_posts' in key:
            result[0] = d[key]
        if 'num_' in key and 'post' not in key:
            result[1] = d[key]
        if 'per' in key:
            result[2] = d[key]
        if 'unique' in key:
            result[3] = d[key]
    return result


@pytest.mark.parametrize('summary_overview, test_overview',
                         zip(sorted(summary_overviews.items()),
                             sorted(test_overviews.items())),
                         ids=test_ids)
def test_has_correct_overview(summary_overview, test_overview):
    assert dict2overview_list(summary_overview[1]) == test_overview[1]


def test_extract_puts_str_in_list():
    result = extract('#one #two #three', regex=r'#\w+', key_name='hashtag')
    assert result['hashtags'] == ['#one #two #three'.split()]


def test_extract_words_puts_str_in_list():
    word_summary_str = extract_words(word_posts, 'rain',  True)
    assert word_summary_str['top_words'][0][0] == 'rain'


def test_extract_numbers_works_without_separators():
    result = extract_numbers('123,456 hello ', number_separators=None)
    assert result['numbers'] == [['123', '456']]


def test_extract_numbers_handles_dash_in_the_middle_of_seps():
    result = extract_numbers('123,456-789', number_separators=('.', '-', ','))
    assert result['numbers'] == [['123,456-789']]
