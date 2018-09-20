
from advertools.extract import extract_mentions, extract_hashtags

mention_posts = ['hello @name', 'email@domain.com', '@oneword', 'hi @nam-e and @name',
               '@first @last', 'an @under_score', 'a @dot.one', 'non latin @مرحبا',
               'other at ＠sign', '@one.@two three', 'number @123text', '@_before @after_']
mention_summary = extract_mentions(mention_posts)
print(mention_summary['mentions'])
mention_test_keys = ['mentions', 'mentions_flat', 'mention_counts',
                     'mention_freq', 'top_mentions', 'overview']

hashtag_posts = ['i like #blue', 'i like #green and #blue', 'i like all']
hashtag_summary = extract_hashtags(hashtag_posts)
hashtag_test_keys = ['hashtags', 'hashtags_flat', 'hashtag_counts',
                     'hashtag_freq', 'top_hashtags', 'overview']


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
    assert mention_summary['top_mentions'] == [('@name', 2), ('@oneword', 1),
                                               ('@nam', 1), ('@first', 1),
                                               ('@last', 1), ('@under_score', 1),
                                               ('@dot', 1), ('＠sign', 1),
                                               ('@one', 1), ('@two', 1),
                                               ('@123text', 1),
                                               ('@_before', 1), ('@after_', 1)]


def test_correct_mention_overview():
    mention_overview = mention_summary['overview']
    assert mention_overview['num_posts'] == 12
    assert mention_overview['num_mentions'] == 14
    assert mention_overview['mentions_per_post'] == 14/12
    assert mention_overview['unique_mentions'] == 13


def test_hashtag_result_has_correct_keys():
    assert set(hashtag_summary.keys()) == set(hashtag_test_keys)


def test_correct_hashtags_extracted():
    assert hashtag_summary['hashtags'] == [['#blue'], ['#green', '#blue'], []]


def test_correct_flat_hashtags():
    assert hashtag_summary['hashtags_flat'] == ['#blue', '#green', '#blue']


def test_correct_hashtag_counts():
    assert hashtag_summary['hashtag_counts'] == [1, 2, 0]


def test_correct_hashtag_freq():
    assert hashtag_summary['hashtag_freq'] == [(0, 1), (1, 1), (2, 1)]


def test_correct_top_hashtags():
    assert hashtag_summary['top_hashtags'] == [('#blue', 2), ('#green', 1)]


def test_correct_hashtag_overview():
    hashtag_overview = hashtag_summary['overview']
    assert hashtag_overview['num_posts'] == 3
    assert hashtag_overview['num_hashtags'] == 3
    assert hashtag_overview['hashtags_per_post'] == 1.0
    assert hashtag_overview['unique_hashtags'] == 2