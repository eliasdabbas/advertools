
import re
from collections import Counter
from .emoji_dict import emoji_dict
from .emoji_dict import emoji_regexp as EMOJI

HASHTAG = r"(?:^|\W)([＃#]{1}\w+)"
MENTION = r'(?:^|\W)([@＠][A-Za-z0-9_]+)'


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


def extract_words(text_list, words_to_find, full_words_only=False):
    """Return a summary dictionary about ``words_to_find`` in ``text_list``.

    Get a summary of the number of words, their frequency, the top
    ones, and more.

    :param text_list: A list of text strings.
    :param words_to_find: A list of words to find in ``text_list``.
    :param full_words_only: Whether or not to find only complete words
        (as specified by ``words_to_find``) or find any any of the
        words as part of longer strings.
    :returns summary: A dictionary with various stats about the words

    >>> posts = ['there is rain, it is raining', 'there is snow and rain',
                 'there is no rain, it is snowing', 'there is nothing']
    >>> word_summary = extract_words(posts, ['rain', 'snow'], True)
    >>> word_summary.keys()
    dict_keys(['words', 'words_flat', 'word_counts', 'word_freq',
    'top_words', 'overview'])

    >>> word_summary['overview']
    {'num_posts': 4,
     'num_words': 4,
     'words_per_post': 1,
     'unique_words': 2}

    >>> word_summary['words']
    [['rain'], ['snow', 'rain'], ['rain'], []]

    A simple extract of mentions from each of the posts. An empty list if
    none exist

    >>> word_summary['words_flat']
    ['rain', 'snow', 'rain', 'rain']

    All mentions in one flat list.

    >>> word_summary['word_counts']
    [1, 2, 1, 0]

    The count of mentions for each post.

    >>> word_summary['word_freq']
    [(0, 1) (1, 2), (2, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. words
    (number_of_words, count)

    >>> word_summary['top_words']
    [('rain', 3), ('snow', 1)]

    Check the same posts extracting any occurrence of the specified words
    with ``full_words_only=False``:

    >>> word_summary = extract_words(posts, ['rain', 'snow'], False)

    >>> word_summary['overview']
    {'num_posts': 4, # number of posts
     'num_words': 6,
     'words_per_post': 1.5,
     'unique_words': 4}

    >>> word_summary['words']
    [['rain', 'raining'], ['snow', 'rain'], ['rain', 'snowing'], []]

    Note that the extracted words are the complete words so you can see
    where they occurred. In case "training" was mentioned,
    you would see that it is not related to rain for example.

    >>> word_summary['words_flat']
    ['rain', 'raining', 'snow', 'rain', 'rain', 'snowing']

    All mentions in one flat list.

    >>> word_summary['word_counts']
    [2, 2, 2, 0]

    >>> word_summary['word_freq']
    [(0, 1), (2, 3)]

    Shows how many posts had 0, 1, 2, 3, etc. words
    (number_of_words, count)

    >>> word_summary['top_words']
    [('rain', 3), ('raining', 1), ('snow', 1), ('snowing', 1)]
    """
    if isinstance(words_to_find, str):
        words_to_find = [words_to_find]
    words_to_find = [word.lower() for word in words_to_find]
    if full_words_only:
        words = []
        for text in text_list:
            temp = []
            for word in text.lower().split():
                if word in words_to_find:
                    temp.append(word)
            words.append(temp)
    else:
        regex = [r'\S{0,}' + x + r'\S{0,}' for x in words_to_find]
        word_regex = '|'.join(regex)
        words = [re.findall(word_regex, text.lower()) for text in text_list]
    words_flat = [item for sublist in words for item in sublist]
    summary = {
        'words': words,
        'words_flat': words_flat,
        'word_counts': [len(word) for word in words],
        'word_freq': sorted(Counter([len(word)
                                     for word in words]).items(),
                            key=lambda x: x[0]),
        'top_words': sorted(Counter(words_flat).items(),
                            key=lambda x: x[1],
                            reverse=True),
        'overview': {
            'num_posts': len(text_list),
            'num_words': len(words_flat),
            'words_per_post': len(words_flat) / len(text_list),
            'unique_words': len(set(words_flat)),
        }
    }
    return summary
