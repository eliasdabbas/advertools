
import re
from collections import Counter
from .emoji_dict import emoji_dict
from .emoji_dict import emoji_regexp as EMOJI

HASHTAG = '#\w+'
MENTION = '(?:^|\W)([@＠][A-Za-z0-9_]+)'


def extract_mentions(text_list):
    """Return a summary dictionary about mentions in ``text_list``

    Get a summary of the number of mentions, their frequency, the top
    ones, and more.

    :param text_list: A list of text strings.
    :returns summary: A dictionary with various stats about mentions

    >>> posts = ['hello @john and @jenny', 'hi there @john', 'good morning']
    >>> mention_summary = extract_mentions(posts)
    >>> mention_summary.keys()
    dict_keys(['mentions', 'mentions_flat', 'mention_counts', 'mention_freq',
    'top_mentions', 'overview'])

    >>> mention_summary['mentions']
    [['@john', '@jenny'], ['@john'], []]

    A simple extract of mentions from each of the posts. An empty list if
    none exist

    >>> mention_summary['mentions_flat']
    ['@john', '@jenny', '@john']

    All mentions in one flat list.

    >>> mention_summary['mention_counts']
    [2, 1, 0]

    The count of mentions per post.

    >>> mention_summary['mention_freq']
    [(0, 1), (1, 1), (2, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. mentions
    (number_of_mentions, count)

    >>> mention_summary['top_mentions']
    [('@john', 2), ('@jenny', 1)]

    >>> mention_summary['overview']
    {'num_posts': 3, # number of posts
     'num_mentions': 3,
     'mentions_per_post': 1.0,
     'unique_mentions': 2}
    """
    mentions = [re.findall(MENTION, text.lower()) for text in text_list]
    mentions_flat = [item for sublist in mentions for item in sublist]
    summary = {
        'mentions': mentions,
        'mentions_flat': mentions_flat,
        'mention_counts': [len(mention) for mention in mentions],
        'mention_freq': sorted(Counter([len(mention)
                                        for mention in mentions]).items(),
                               key=lambda x: x[0]),
        'top_mentions': sorted(Counter(mentions_flat).items(),
                               key=lambda x: x[1],
                               reverse=True),
        'overview': {
            'num_posts': len(text_list),
            'num_mentions': len(mentions_flat),
            'mentions_per_post': len(mentions_flat) / len(text_list),
            'unique_mentions': len(set(mentions_flat)),
        }
    }
    return summary


def extract_hashtags(text_list):
    """Return a summary dictionary about hashtags in ``text_list``

    Get a summary of the number of hashtags, their frequency, the top
    ones, and more.

    :param text_list: A list of text strings.
    :returns summary: A dictionary with various stats about hashtags

    >>> posts = ['i like #blue', 'i like #green and #blue', 'i like all']
    >>> hashtag_summary = extract_hashtags(posts)
    >>> hashtag_summary.keys()
    dict_keys(['hashtags', 'hashtags_flat', 'hashtag_counts', 'hashtag_freq',
    'top_hashtags', 'overview'])

    >>> hashtag_summary['hashtags']
    [['#blue'], ['#green', '#blue'], []]

    A simple extract of hashtags from each of the posts. An empty list if
    none exist

    >>> hashtag_summary['hashtags_flat']
    ['#blue', '#green', '#blue']

    All hashtags in one flat list.

    >>> hashtag_summary['hashtag_counts']
    [1, 2, 0]

    The count of hashtags per post.

    >>> hashtag_summary['hashtag_freq']
    [(0, 1), (1, 1), (2, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. hashtags
    (number_of_hashtags, count)

    >>> hashtag_summary['top_hashtags']
    [('#blue', 2), ('#green', 1)]

    >>> hashtag_summary['overview']
    {'num_posts': 3,
     'num_hashtags': 3,
     'hashtags_per_post': 1.0,
     'unique_hashtags': 2}
     """
    hashtags = [re.findall(HASHTAG, text.lower()) for text in text_list]
    hashtags_flat = [item for sublist in hashtags for item in sublist]
    summary = {
        'hashtags': hashtags,
        'hashtags_flat': hashtags_flat,
        'hashtag_counts': [len(hashtag) for hashtag in hashtags],
        'hashtag_freq': sorted(Counter([len(hashtag)
                                        for hashtag in hashtags]).items(),
                               key=lambda x: x[0]),
        'top_hashtags': sorted(Counter(hashtags_flat).items(),
                               key=lambda x: x[1],
                               reverse=True),
        'overview': {
            'num_posts': len(text_list),
            'num_hashtags': len(hashtags_flat),
            'hashtags_per_post': len(hashtags_flat) / len(text_list),
            'unique_hashtags': len(set(hashtags_flat)),
        }
    }
    return summary


def extract_emoji(text_list):
    """Return a summary dictionary about emoji in ``text_list``

    Get a summary of the number of emoji, their frequency, the top
    ones, and more.

    :param text_list: A list of text strings.
    :returns summary: A dictionary with various stats about emoji

    >>> posts = ['I am grinning 😀','A grinning cat 😺',
                 'hello! 😀😀😀 💛💛', 'Just text']

    >>> emoji_summary = extract_emoji(posts)
    >>> emoji_summary.keys()
    dict_keys(['emoji', 'emoji_text', 'emoji_flat', 'emoji_flat_text',
               'emoji_counts', 'emoji_freq', 'top_emoji',
               'top_emoji_text', 'overview'])

    >>> emoji_summary['emoji']
    [['😀'], ['😺'], ['😀', '😀', '😀', '💛', '💛'], []]

    >>> emoji_summary['emoji_text']
    [['grinning face'],
     ['grinning cat face'],
     ['grinning face', 'grinning face', 'grinning face',
      'yellow heart', 'yellow heart'],
     []]

    A simple extract of emoji from each of the posts. An empty
    list if none exist

    >>> emoji_summary['emoji_flat']
    ['😀', '😺', '😀', '😀', '😀', '💛', '💛']

    >>> emoji_summary['emoji_flat_text']
    ['grinning face', 'grinning cat face', 'grinning face', 'grinning face',
     'grinning face', 'yellow heart', 'yellow heart']


    All emoji in one flat list.

    >>> emoji_summary['emoji_counts']
    [1, 1, 5, 0]

    The count of emoji per post.

    >>> emoji_summary['emoji_freq']
    [(0, 1), (1, 2), (5, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. emoji
    (number_of_emoji, count)

    >>> emoji_summary['top_emoji']
    [('😀', 4), ('💛', 2), ('😺', 1)]

    >>> emoji_summary['top_emoji_text']
    [('grinning face', 4), ('yellow heart', 2),
     ('grinning cat face', 1)]

    >>> emoji_summary['overview']
    {'num_posts': 4,
     'num_emoji': 7,
     'emoji_per_post': 1.75,
     'unique_emoji': 3}
    """
    emoji = [re.findall(EMOJI, text.lower()) for text in text_list]
    emoji_flat = [item for sublist in emoji for item in sublist]
    emoji_flat_text = [emoji_dict[em].strip(':').replace('_', ' ')
                       for em in emoji_flat]
    summary = {
        'emoji': emoji,
        'emoji_text': [[emoji_dict[em].strip(':').replace('_', ' ')
                        for em in em_list]
                       for em_list in emoji],
        'emoji_flat': emoji_flat,
        'emoji_flat_text': emoji_flat_text,
        'emoji_counts': [len(em) for em in emoji],
        'emoji_freq': sorted(Counter([len(em) for em in emoji]).items(),
                             key=lambda x: x[0]),
        'top_emoji': sorted(Counter(emoji_flat).items(),
                            key=lambda x: x[1],
                            reverse=True),
        'top_emoji_text': sorted(Counter(emoji_flat_text).items(),
                                 key=lambda x: x[1],
                                 reverse=True),
        'overview': {
            'num_posts': len(text_list),
            'num_emoji': len(emoji_flat),
            'emoji_per_post': len(emoji_flat) / len(text_list),
            'unique_emoji': len(set(emoji_flat)),
        }

    }
    return summary