
from advertools.extract import extract_mentions, extract_hashtags, extract_emoji

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


def test_mention_result_has_correct_keys():
    assert set(mention_summary.keys()) == set(mention_test_keys)


def test_correct_mentions_extracted():
    assert mention_summary['mentions'] == [['@name'], [], ['@oneword'],
                                           ['@nam', '@name'],['@first', '@last'],
                                           ['@under_score'], ['@dot'], [],
                                           ['＠sign'], ['@one', '@two'],
                                           ['@123text'], ['@_before', '@after_']]


def test_correct_flat_mentions():
    assert mention_summary['mentions_flat'] == ['@name', '@oneword', '@nam',
                                                '@name', '@first', '@last',
                                                '@under_score', '@dot', '＠sign',
                                                '@one', '@two', '@123text',
                                                '@_before', '@after_']


def test_correct_mention_counts():
    assert mention_summary['mention_counts'] == [1, 0, 1, 2, 2, 1, 1, 0, 
                                                 1, 2, 1, 2]


def test_correct_mention_freq():
    assert mention_summary['mention_freq'] == [(0, 2), (1, 6), (2, 4)]


def test_correct_top_mentions():
    assert set(mention_summary['top_mentions']) == set([('@name', 2), ('@oneword', 1),
                                               ('@nam', 1), ('@first', 1),
                                               ('@last', 1), ('@under_score', 1),
                                               ('@dot', 1), ('＠sign', 1),
                                               ('@one', 1), ('@two', 1),
                                               ('@123text', 1),
                                               ('@_before', 1), ('@after_', 1)])


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
                                           ['#nam', '#name'],['#first', '#last'],
                                           ['#under_score'], ['#dot'], ['#مرحبا'],
                                           ['＃sign'], ['#one', '#two'],
                                           ['#123text'], ['#_before', '#after_']]



def test_correct_flat_hashtags():
    assert hashtag_summary['hashtags_flat'] == ['#name', '#oneword', '#nam',
                                                '#name', '#first', '#last',
                                                '#under_score', '#dot', '#مرحبا',
                                                '＃sign', '#one', '#two',
                                                '#123text', '#_before', '#after_']


def test_correct_hashtag_counts():
    assert hashtag_summary['hashtag_counts'] == [1, 0, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2]


def test_correct_hashtag_freq():
    assert hashtag_summary['hashtag_freq'] == [(0, 1), (1, 7), (2, 4)]


def test_correct_top_hashtags():
    assert set(hashtag_summary['top_hashtags']) == set([('#name', 2), ('#oneword', 1),
                                               ('#nam', 1), ('#first', 1),
                                               ('#last', 1), ('#under_score', 1),
                                               ('#dot', 1), ('＃sign', 1),
                                               ('#one', 1), ('#two', 1),
                                               ('#123text', 1), ('#مرحبا', 1),
                                               ('#_before', 1), ('#after_', 1)])



def test_correct_hashtag_overview():
    hashtag_overview = hashtag_summary['overview']
    assert hashtag_overview['num_posts'] == 12
    assert hashtag_overview['num_hashtags'] == 15
    assert hashtag_overview['hashtags_per_post'] == 15/12
    assert hashtag_overview['unique_hashtags'] == 14


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
