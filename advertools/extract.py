"""
.. _extract:

Extract structured entities from text lists
===========================================

Structured entities are pattern matches and not inferred entities.
Some example are hashtags, emoji, mentions, questions, and so on. This is
in contrast to entity extraction which are inferred from the context of the
sentence (people, companies, brands and so on).

All functions start with ``extract_`` and have a descriptive name for the type
of entity that they extract.

There is also a generic ``extract`` fucntion which powers all others, and it
can be used for any other pattern not included. It takes a regular expression,
and returns a similar dictionary to the other functions.

Extract Functions
-----------------

======================================     ====================================================================
:func:`extract`                            A generic function that takes a regex to extract any pattern you want
:func:`extract_currency`                   Currency symbols together with surrounding text for context. This does not include currency abbreviations (USD, EUR, JPY, etc.), only symbols ($, £, €, etc).
:func:`advertools.emoji.extract_emoji`     All the emoji database, together with textual names, groups and sub-groups.
:func:`extract_exclamations`               Sentences that end with an excalamation mark!
:func:`extract_hashtags`                   Extract hashtags with descriptive statistics.
:func:`extract_intense_words`              Words that contain three or more repeated characters to express an intense feeling (positive or negative), "I looooooovvvvee this thing".
:func:`extract_mentions`                   User mentions in social media posts. Also useful for network analysis.
:func:`extract_numbers`                    Any numbers that are included the text list. Included a modifiable list of separators to use (",", ".", "-", etc.).
:func:`extract_questions`                  Questions included in the text list.
:func:`extract_urls`                       URls in the text list.
:func:`extract_words`                      Any arbitrary words that you want extracted. Works in two modes, either the word should fully match the pattern, or as part of a longer word, ("rest" can be matched from "restaurant" or not).
======================================     ====================================================================

All functions return a dictionary with the entities extracted, along with
helpful statistics. Since the entities have different meanings, most of them
return additional keys depending on the context.

The recommended way of using:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv

    text_list = ['This is the first #text.', 'Second #sentence is here.',
                 'Hello, how are you?', 'This #sentence is the last #sentence']
    hashtag_summary = adv.extract_hashtags(text_list)
    hashtag_summary.keys()

.. code-block::

    dict_keys(['hashtags', 'hashtags_flat', 'hashtag_counts', 'hashtag_freq',
               'top_hashtags', 'overview'])

Now you can start exploring:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    hashtag_summary

>>> hashtag_summary['overview']
{'num_posts': 4,
 'num_hashtags': 4,
 'hashtags_per_post': 1.0,
 'unique_hashtags': 2}

>>> hashtag_summary['hashtags']
[['#text'], ['#sentence'], [], ['#sentence', '#sentence']]
>>> hashtag_summary['hashtags_flat']
['#text', '#sentence', '#sentence', '#sentence']
>>> hashtag_summary['hashtag_counts']
[1, 1, 0, 2]
>>> hashtag_summary['hashtag_freq']
[(0, 1), (1, 2), (2, 1)]
>>> hashtag_summary['top_hashtags']
[('#sentence', 3), ('#text', 1)]

Let's explore a proper dataset of tweets, which you can generate using one of
the functions in the :ref:`twitter API <twitter>` module.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv
    import pandas as pd

    tweets = pd.read_csv('data/tweets.csv')
    print(tweets.shape)
    tweets.head()

====  ================================================================================================================================================  =================
  ..  tweet_text                                                                                                                                          followers_count
====  ================================================================================================================================================  =================
   0  @AERIALMAGZC @penguinnyyyyy you won't be afraid if I give you a real reason :D                                                                                  157
   1  Vibing in the office to #Metallica when the boss is on a coffee break                                                                                          4687
      #TheOffice https://t.co/U5vdYevvfe
   2  I feel like Ann says she likes coffee and then gets drinks that are 99% sugar and 1% coffee https://t.co/HfuBV4v3aY                                             104
   3  A venti iced coffee with four pumps of white mocha, sweet cream and caramel drizzle might just be my new favorite drink. Shout out to TikTok lol                126
   4  I was never a coffee person until I had kids. ☕️ this cup is a life saver. https://t.co/Zo0CnVuiGj                                                             1595
   5  Who's excited about our next Coffee Chat? We know we are!🥳                                                                                                    5004

      We're also adding Representative John Bradford to this lineup to discuss redistricting in the area. You won't want to miss it!

      RSVP: https://t.co/R3YNJjJCUG
      Join the meeting: https://t.co/Ho4Kx7ZZ24 https://t.co/KfPdR3hupY
   6  he paid for my coffee= husband💗                                                                                                                                165
   7  It's nipply outside, and now I side too :)                                                                                                                        0
      That sounds like blowjob in front of a fire and visit with coffee after :)
      I'm still out of coffee
      I could have green tea instead
      Hahahahahahaha
      I want to spend the morning pampering you ...
   8  Good morning 😃🌞☀️ I hope everyone has a great Tuesday morning. Enjoy your day and coffee ☕️ ♥️❤️💕🥰😘                                                           189
   9  @MarvinMilton2 I nearly choked on my coffee 🤪                                                                                                                 1160
====  ================================================================================================================================================  =================

Extract `#hashtags`
-------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    hashtag_summary = adv.extract_hashtags(tweets['tweet_text'])
    hashtag_summary.keys()

.. code-block::

    dict_keys(['hashtags', 'hashtags_flat', 'hashtag_counts', 'hashtag_freq',
            'top_hashtags', 'overview'])


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    hashtag_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_hashtags': 733,
    'hashtags_per_post': 0.3665,
    'unique_hashtags': 572}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    [h for h in hashtag_summary['hashtags'] if h][:10]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    hashtag_summary['top_hashtags'][:10]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    hashtag_summary['hashtag_freq']


Extract `@mentions`
-------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    mention_summary = adv.extract_mentions(tweets['tweet_text'])
    mention_summary.keys()

.. code-block::

    dict_keys(['mentions', 'mentions_flat', 'mention_counts', 'mention_freq',
               'top_mentions', 'overview'])


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    mention_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_mentions': 1346,
    'mentions_per_post': 0.673,
    'unique_mentions': 1132}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    pd.DataFrame(zip(mention_summary['mentions'],
                    mention_summary['mention_counts']),
                 columns=['mentions', 'count'])

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    [h for h in mention_summary['mentions'] if h][:10]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    mention_summary['top_mentions'][:10]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    mention_summary['mention_freq']

.. thebe-button::
    Run this code


Extract Currency  `$ ¢ £ ¤ ¥ ֏ ؋ ₲ ₵ ₸ ₹﹩ ￠ ￡ ￥ ￦ ₺ ₻ ₼ ₽ ₾ ₿ ﷼`
---------------------------------------------------------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    currency_summary = adv.extract_currency(tweets['tweet_text'])
    currency_summary.keys()

.. code-block::

    dict_keys(['currency_symbols', 'currency_symbols_flat',
               'currency_symbol_counts', 'currency_symbol_freq',
               'top_currency_symbols', 'overview', 'currency_symbol_names',
               'surrounding_text'])


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    currency_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_currency_symbols': 37,
    'currency_symbols_per_post': 0.0185,
    'unique_currency_symbols': 4}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    currency_summary['top_currency_symbols']

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    [text for text in currency_summary['surrounding_text'] if text][:10]


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    [sym for sym in currency_summary['currency_symbol_names'] if sym][:10]


Extract numbers `1234567890٠١٢٣٤٥٦٧٨٩㊺𑁛𐄍𐢪⓲𑁣𐄨𐤛`
--------------------------------------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    number_summary = adv.extract_numbers(tweets['tweet_text'])
    number_summary.keys()

.. code-block::

    dict_keys(['numbers', 'numbers_flat', 'number_counts', 'number_freq',
               'top_numbers', 'overview'])


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    number_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_numbers': 1727,
    'numbers_per_post': 0.8635,
    'unique_numbers': 257}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    number_summary['number_freq']

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    pd.DataFrame({
        'numbers': number_summary['numbers'],
        'counts': number_summary['number_counts'],
    }).head(20)


Extract questions `? ¿ ; ՞ ؟ ፧ ᥅ ⁇ ⁈ ⁉ ⳺ ⳻ ⸮ ꘏ ꛷ ︖ ﹖ ？ 𑅃 𞥟 ʔ ‽`
------------------------------------------------------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    question_summary = adv.extract_questions(tweets['tweet_text'])
    question_summary.keys()

.. code-block::

    dict_keys(['question_marks', 'question_marks_flat', 'question_mark_counts',
               'question_mark_freq', 'top_question_marks', 'overview',
               'question_mark_names', 'question_text'])

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    question_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_question_marks': 321,
    'question_marks_per_post': 0.1605,
    'unique_question_marks': 1}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    question_summary['question_text'][:25]

.. code-block::

    [[],
     [],
     [],
     [],
     [],
     ["Who's excited about our next Coffee Chat?"],
     [],
     [],
     [],
     [],
     ['@ckaiserjr @perry_ron @LILGUYISBACK Is it okay if the hot water is flavored with coffee?'],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     ["You think if you do that you'll loose your followers ???"],
     [],
     [],
     ['maybe more coffee will help?'],
     []]


Extract Exclamations `! ¡ ՜ ߹ ᥄ ‼ ⁈ ⁉ ︕ ﹗ ！ 𞥞`
-------------------------------------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    exclamation_summary = adv.extract_exclamations(tweets['tweet_text'])
    exclamation_summary.keys()

.. code-block::

    dict_keys(['exclamation_marks', 'exclamation_marks_flat',
               'exclamation_mark_counts', 'exclamation_mark_freq',
               'top_exclamation_marks', 'overview', 'exclamation_mark_names',
               'exclamation_text'])

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    exclamation_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_exclamation_marks': 563,
    'exclamation_marks_per_post': 0.2815,
    'unique_exclamation_marks': 2}


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    exclamation_summary['top_exclamation_marks']

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    exclamation_summary['exclamation_text'][:15]


Extract Emoji 😂😭🥺🤣❤️✨🙏😍
------------------------------

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary = adv.extract_emoji(tweets['tweet_text'])
    emoji_summary.keys()

.. code-block::

    dict_keys(['emoji', 'emoji_text', 'emoji_flat', 'emoji_flat_text',
               'emoji_counts', 'emoji_freq', 'top_emoji', 'top_emoji_text',
               'top_emoji_groups', 'top_emoji_sub_groups', 'overview'])

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary['overview']

.. code-block::

    {'num_posts': 2000,
    'num_emoji': 1149,
    'emoji_per_post': 0.5745,
    'unique_emoji': 279}

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    pd.DataFrame({
        'emoji': emoji_summary['emoji'],
        'emoji_name': emoji_summary['emoji_text']
    })[:20]


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary['top_emoji'][:20]

.. code-block::

    [('☕', 159),
     ('😭', 72),
     ('😂', 64),
     ('🤣', 49),
     ('🔥', 32),
     ('⬛', 21),
     ('🟩', 16),
     ('🥰', 15),
     ('😍', 15),
     ('❤️', 14),
     ('🍩', 14),
     ('😋', 13),
     ('🥺', 13),
     ('🤔', 13),
     ('🥲', 13),
     ('🙏', 12),
     ('😅', 11),
     ('💖', 11),
     ('💜', 11),
     ('😊', 10)]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary['top_emoji_text'][:20]


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary['top_emoji_groups']

.. code-block::

    [('Smileys & Emotion', 601),
    ('Food & Drink', 210),
    ('People & Body', 97),
    ('Symbols', 75),
    ('Travel & Places', 67),
    ('Animals & Nature', 33),
    ('Objects', 29),
    ('Activities', 26),
    ('Flags', 11)]

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    emoji_summary['top_emoji_sub_groups']

"""  # noqa: E501

__all__ = [
    "extract",
    "extract_currency",
    "extract_exclamations",
    "extract_hashtags",
    "extract_intense_words",
    "extract_mentions",
    "extract_numbers",
    "extract_questions",
    "extract_words",
    "extract_urls",
]

import re
from collections import Counter
from unicodedata import name
from urllib.parse import urlparse

# from .emoji import EMOJI, EMOJI_ENTRIES
from .regex import (
    CURRENCY,
    CURRENCY_RAW,
    EXCLAMATION,
    EXCLAMATION_MARK,
    HASHTAG,
    MENTION,
    QUESTION,
    QUESTION_MARK,
    URL,
)


def extract(text_list, regex, key_name, extracted=None, **kwargs):
    """Return a summary dictionary about arbitrary matches in ``text_list``.

    This function is used by other specialized functions to extract
    certain elements (hashtags, mentions, emojis, etc.).
    It can be used for other arbitrary elements/matches. You only need to
    provide your own regex.

    :param list text_list: Any list of strings (social posts, page titles, etc.)
    :param str regex: The regex pattern to use for extraction.
    :param str key_name: The name of the object extracted in singular form
        (hashtag, mention, etc.)
    :param list(list) extracted: List of lists, optional. If the regex is not
        straightforward, and matches need to be made with special code,
        provide the extracted words/matches as a list for each element
        of :attr:`text_list`.
    :param mapping kwargs: Other kwargs that might be needed.
    :return summary: A dictionary summarizing the extracted data.
    """
    if isinstance(regex, str):
        regex = re.compile(regex)
    if isinstance(text_list, str):
        text_list = [text_list]
    if not extracted:
        extracted = [regex.findall(text.lower()) for text in text_list]
    flat = [item for sublist in extracted for item in sublist]

    summary = {
        key_name + "s": extracted,
        key_name + "s" + "_flat": flat,
        key_name + "_counts": [len(x) for x in extracted],
        key_name + "_freq": sorted(
            Counter([len(i) for i in extracted]).items(), key=lambda x: x[0]
        ),
        "top_" + key_name + "s": sorted(
            Counter(flat).items(), key=lambda x: x[1], reverse=True
        ),
        "overview": {
            "num_posts": len(text_list),
            "num_" + key_name + "s": len(flat),
            key_name + "s" + "_per_post": len(flat) / len(text_list),
            "unique_" + key_name + "s": len(set(flat)),
        },
    }
    return summary


def extract_currency(text_list, left_chars=20, right_chars=20):
    """Return a summary dictionary about currency symbols in ``text_list``

    Get a summary of the number of currency symbols, their frequency,
    the top ones, and more.

    Parameters
    ----------
    text_list : list
      A list of text strings.
    left_chars : int
      The number of characters to extract, to the left of the symbol when getting
      :attr:`surrounding_text`
    right_chars : int
      The number of characters to extract, to the left of the symbol when getting
      :attr:`surrounding_text`

    Returns
    -------

    summary : dict
      A dictionary with various stats about currencies.

    Examples
    --------
    >>> posts = ['today ₿1 is around $4k', 'and ₿ in £ & €?', 'no idea']
    >>> currency_summary = extract_currency(posts)
    >>> currency_summary.keys()
    dict_keys(['currency_symbols', 'currency_symbols_flat',
    'currency_symbol_counts', 'currency_symbol_freq',
    'top_currency_symbols', 'overview', 'currency_symbol_names'])

    >>> currency_summary['currency_symbols']
    [['₿', '$'], ['₿', '£', '€'], []]

    A simple extract of currencies from each of the posts. An empty list if
    none exist

    >>> currency_summary['currency_symbols_flat']
    ['₿', '$', '₿', '£', '€']

    All currency symbols in one flat list.

    >>> currency_summary['currency_symbol_counts']
    [2, 3, 0]

    The count of currency symbols per post.

    >>> currency_summary['currency_symbol_freq']
    [(0, 1), (2, 1), (3, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. currency symbols
    (number_of_symbols, count)

    >>> currency_summary['top_currency_symbols']
    [('₿', 2), ('$', 1), ('£', 1), ('€', 1)]

    >>> currency_summary['currency_symbol_names']
    [['bitcoin sign', 'dollar sign'], ['bitcoin sign', 'pound sign',
    'euro sign'], []]

    >>> currency_summary['surrounding_text']
    [['today ₿1 is around $4k'], ['and ₿ in £ & €?'], []]

    >>> extract_currency(posts, 5, 5)['surrounding_text']
    [['oday ₿1 is ', 'ound $4k'], ['and ₿ in £', ' & €?'], []]

    >>> extract_currency(posts, 0, 3)['surrounding_text']
    [['₿1 i', '$4k'], ['₿ in', '£ & ', '€?'], []]

    >>> currency_summary['overview']
    {'num_posts': 3,
    'num_currency_symbols': 5,
    'currency_symbols_per_post': 1.6666666666666667,
    'unique_currency_symbols': 4}
    """
    summary = extract(text_list, CURRENCY, "currency_symbol")
    summary["currency_symbol_names"] = [
        [name(c).lower() for c in x] if x else [] for x in summary["currency_symbols"]
    ]
    surrounding_text_regex = re.compile(
        r".{0,"
        + str(left_chars)
        + "}"
        + CURRENCY_RAW
        + r".{0,"
        + str(right_chars)
        + "}"
    )
    summary["surrounding_text"] = [
        surrounding_text_regex.findall(text) for text in text_list
    ]
    return summary


def extract_exclamations(text_list):
    """Return a summary dictionary about exclamation (mark)s in ``text_list``

    Get a summary of the number of exclamation marks, their frequency,
    the top ones, as well the exclamations written/said.

    text_list : list
      A list of text strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about exclamations.

    Examples
    --------
    >>> posts = ['Who are you!', 'What is this!', 'No exclamation here?']
    >>> exclamation_summary = extract_exclamations(posts)
    >>> exclamation_summary.keys()
    dict_keys(['exclamation_marks', 'exclamation_marks_flat',
    'exclamation_mark_counts', 'exclamation_mark_freq',
    'top_exclamation_marks', 'overview', 'exclamation_mark_names',
    'exclamation_text'])

    >>> exclamation_summary['exclamation_marks']
    [['!'], ['!'], []]

    A simple extract of exclamation marks from each of the posts. An empty
    list if none exist

    >>> exclamation_summary['exclamation_marks_flat']
    ['!', '!']

    All exclamation marks in one flat list.

    >>> exclamation_summary['exclamation_mark_counts']
    [1, 1, 0]

    The count of exclamation marks per post.

    >>> exclamation_summary['exclamation_mark_freq']
    [(0, 1), (1, 2)]

    Shows how many posts had 0, 1, 2, 3, etc. exclamation marks
    (number_of_symbols, count)

    >>> exclamation_summary['top_exclamation_marks']
    [('!', 2)]

    Might be interesting if you have different types of exclamation marks

    >>> exclamation_summary['exclamation_mark_names']
    [['exclamation mark'], ['exclamation mark'], []]

    >>> exclamation_summary['overview']
    {'num_posts': 3,
    'num_exclamation_marks': 2,
    'exclamation_marks_per_post': 0.6666666666666666,
    'unique_exclamation_marks': 1}

    >>> posts2 = ["don't go there!", 'مرحبا. لا تذهب!', '¡Hola! ¿cómo estás?',
    ... 'a few different exclamation marks! make sure you see them!']

    >>> exclamation_summary = extract_exclamations(posts2)

    >>> exclamation_summary['exclamation_marks']
    [['!'], ['!'], ['¡', '!'], ['!', '!']]
    # might be displayed in opposite order due to RTL exclamation mark
    A simple extract of exclamation marks from each of the posts.
    An empty list if none exist

    >>> exclamation_summary['exclamation_marks_flat']
    ['!', '!', '¡', '!', '!', '!']

    All exclamation marks in one flat list.

    >>> exclamation_summary['exclamation_mark_counts']
    [1, 1, 2, 2]

    The count of exclamation marks per post.

    >>> exclamation_summary['exclamation_mark_freq']
    [(1, 2), (2, 2)]

    Shows how many posts had 0, 1, 2, 3, etc. exclamation marks
    (number_of_symbols, count)

    >>> exclamation_summary['top_exclamation_marks']
    [('!', 5), ('¡', 1)]

    Might be interesting if you have different types of exclamation marks

    >>> exclamation_summary['exclamation_mark_names']
    [['exclamation mark'], ['exclamation mark'],
    ['inverted exclamation mark', 'exclamation mark'],
    ['exclamation mark', 'exclamation mark']]

    >>> exclamation_summary['overview']
    {'num_posts': 4,
    'num_exclamation_marks': 6,
    'exclamation_marks_per_post': 1.5,
    'unique_exclamation_marks': 4}
    """
    summary = extract(text_list, EXCLAMATION_MARK, key_name="exclamation_mark")
    summary["exclamation_mark_names"] = [
        [name(c).lower() for c in x] if x else [] for x in summary["exclamation_marks"]
    ]
    summary["exclamation_text"] = [EXCLAMATION.findall(text) for text in text_list]
    return summary


def extract_hashtags(text_list):
    """Return a summary dictionary about hashtags in :attr:`text_list`

    Get a summary of the number of hashtags, their frequency, the top
    ones, and more.

    text_list : list
      A list of text strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about hashtags.

    Examples
    --------
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
    return extract(text_list, HASHTAG, "hashtag")


def extract_intense_words(text_list, min_reps=3):
    """Return a summary dictionary about intense words in :attr:`text_list`

    Get all instances of usage of intense words (positive or negative), using
    words that have :attr:`min_reps` or more repetitions of characters.
    "I looooooveeee youuuuuuu", and "I haaatttteeee youuuuuu" are both intense.

    Parameters
    ----------
    text_list : list
      A text list from which to extract intense words.
    min_reps : int
      The number of times a character has to be repeated for the word to be considered
      intense.

    Returns
    -------
    summary : dict
      A dictionary with various stats about intense words.
    """
    regex = re.compile(r"(\S*)(\S)({}\S*)".format((min_reps - 1) * r"\2"))
    extracted = [["".join(x) for x in regex.findall(text)] for text in text_list]

    return extract(text_list, regex, "intense_word", extracted)


def extract_mentions(text_list):
    """Return a summary dictionary about mentions in ``text_list``

    Get a summary of the number of mentions, their frequency, the top
    ones, and more.

    Parameters
    ----------
    text_list : list
      A list of text strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about mentions.

    Examples
    --------
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
    return extract(text_list, MENTION, "mention")


def extract_numbers(text_list, number_separators=(".", ",", "-")):
    """Return a summary dictionary about numbers in ``text_list``, separated
    by any of ``number_separators``

    Get a summary of the number of numbers, their frequency, the top
    ones, and more. Typically, numbers would contain separators to make them
    easier to read, so these are included by default, which you can modify.

    Parameters
    ----------
    text_list : list
      A list of text strings.
    number_separators : list
      A list of separators that you want to be included as part of the extracted
      numbers.

    Returns
    -------
    summary : dict
      A dictionary with various stats about the numbers.

    Examples
    --------
    >>> posts = ['text before 123', '123,456 text after', 'phone 333-444-555',
    'multiple 123,456 and 123.456.789']
    >>> number_summary = extract_numbers(posts)
    >>> number_summary.keys()
    dict_keys(['numbers', 'numbers_flat', 'number_counts', 'number_freq',
    'top_numbers', 'overview'])

    >>> number_summary['numbers']
    [['123'], ['123,456'], ['333-444-555'], ['123,456', '123.456.789']]

    A simple extract of number from each of the posts. An empty list if
    none exist

    >>> number_summary['numbers_flat']
    ['123', '123,456', '333-444-555', '123,456', '123.456.789']

    All numbers in one flat list.

    >>> number_summary['number_counts']
    [1, 1, 1, 2]

    The count of numbers per post.

    >>> number_summary['number_freq']
    [(1, 3), (2, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. numbers
    (number_of_numbers, count)

    >>> number_summary['top_numbers']
    [('123,456', 2), ('123', 1), ('333-444-555', 1), ('123.456.789', 1)]

    >>> number_summary['overview']
    {'num_posts': 4,
     'num_numbers': 5,
     'numbers_per_post': 1.25,
     'unique_numbers': 4}
    """
    if not number_separators:
        regex = r"\d+"
    else:
        if "-" in number_separators:
            number_separators = [s for s in number_separators if s != "-"] + ["-"]
        separators = "[" + "".join(number_separators) + "]"
        regex = r"(?:(?:\d+" + separators + "?)+)?" + r"\d+"
    return extract(text_list, regex=regex, key_name="number")


def extract_questions(text_list):
    """Return a summary dictionary about question(mark)s in ``text_list``

    Get a summary of the number of question marks, their frequency,
    the top ones, as well the questions asked.

    Parameters
    ----------
    text_list : list
      A list of text strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about questions.

    Examples
    --------
    >>> posts = ['How are you?', 'What is this?', 'No question Here!']
    >>> question_summary = extract_questions(posts)
    >>> question_summary.keys()
    dict_keys(['question_marks', 'question_marks_flat',
    'question_mark_counts', 'question_mark_freq', 'top_question_marks',
    'overview', 'question_mark_names', 'question_text'])

    >>> question_summary['question_marks']
    [['?'], ['?'], []]

    A simple extract of question marks from each of the posts. An empty
    list if none exist

    >>> question_summary['question_marks_flat']
    ['?', '?']

    All question marks in one flat list.

    >>> question_summary['question_mark_counts']
    [1, 1, 0]

    The count of question marks per post.

    >>> question_summary['question_mark_freq']
    [(0, 1), (1, 2)]

    Shows how many posts had 0, 1, 2, 3, etc. question marks
    (number_of_symbols, count)

    >>> question_summary['top_question_marks']
    [('?', 2)]

    Might be interesting if you have different types of question marks
    (Arabic, Spanish, Greek, Armenian, or other)

    >>> question_summary['question_mark_names']
    [['question mark'], ['question mark'], []]

    >>> question_summary['overview']
    {'num_posts': 3,
    'num_question_marks': 2,
    'question_marks_per_post': 0.6666666666666666,
    'unique_question_marks': 1}

    >>> posts2 = ['Πώς είσαι;', 'مرحباً. كيف حالك؟', 'Hola, ¿cómo estás?',
    ... 'Can you see the new questions? Did you notice the different marks?']

    >>> question_summary = extract_questions(posts2)

    >>> question_summary['question_marks']
    [[';'], ['؟'], ['¿', '?'], ['?', '?']]
    # might be displayed in opposite order due to RTL question mark
    A simple extract of question marks from each of the posts. An empty list if
    none exist

    >>> question_summary['question_marks_flat']
    [';', '؟', '¿', '?', '?', '?']

    All question marks in one flat list.

    >>> question_summary['question_mark_counts']
    [1, 1, 2, 2]

    The count of question marks per post.

    >>> question_summary['question_mark_freq']
    [(1, 2), (2, 2)]

    Shows how many posts had 0, 1, 2, 3, etc. question marks
    (number_of_symbols, count)

    >>> question_summary['top_question_marks']
    [('?', 3), (';', 1), ('؟', 1), ('¿', 1)]

    Might be interesting if you have different types of question marks
    (Arabic, Spanish, Greek, Armenian, or other)

    >>> question_summary['question_mark_names']
    [['greek question mark'], ['arabic question mark'],
    ['inverted question mark', 'question mark'],
    ['question mark', 'question mark']]
    # correct order

    >>> question_summary['overview']
    {'num_posts': 4,
    'num_question_marks': 6,
    'question_marks_per_post': 1.5,
    'unique_question_marks': 4}
    """
    summary = extract(text_list, QUESTION_MARK, key_name="question_mark")
    summary["question_mark_names"] = [
        [name(c).lower() for c in x] if x else [] for x in summary["question_marks"]
    ]
    summary["question_text"] = [QUESTION.findall(text) for text in text_list]
    return summary


def extract_urls(text_list):
    """Return a summary dictionary about URLs in ``text_list``

    Get a summary of the number of URLs, their frequency, the top
    ones, and more.
    This does NOT validate URLs, www.a.b would count as a URL

    Parameters
    ----------
    text_list : list
      A list of text strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about URLs.

    Examples
    --------
    >>> posts = ['one link http://example.com', 'two: http://a.com www.b.com',
    ...          'no links here',
    ...          'long url http://example.com/one/two/?1=one&2=two']
    >>> url_summary = extract_urls(posts)
    >>> url_summary.keys()
    dict_keys(['urls', 'urls_flat', 'url_counts', 'url_freq',
    'top_urls', 'overview', 'top_domains', 'top_tlds'])

    >>> url_summary['urls']
    [['http://example.com'],
     ['http://a.com', 'http://www.b.com'],
     [],
     ['http://example.com/one/two/?1=one&2=two']]

    A simple extract of urls from each of the posts. An empty list if
    none exist

    >>> url_summary['urls_flat']
    ['http://example.com', 'http://a.com', 'http://www.b.com',
     'http://example.com/one/two/?1=one&2=two']

    All urls in one flat list.

    >>> url_summary['url_counts']
    [1, 2, 0, 1]

    The count of urls per post.

    >>> url_summary['url_freq']
    [(0, 1), (1, 2), (2, 1)]

    Shows how many posts had 0, 1, 2, 3, etc. urls
    (number_of_urls, count)

    >>> url_summary['top_urls']
    [('http://example.com', 1), ('http://a.com', 1), ('http://www.b.com', 1),
     ('http://example.com/one/two/?1=one&2=two', 1)]

    >>> url_summary['top_domains']
    [('example.com', 2), ('a.com', 1), ('www.b.com', 1)]

    >>> url_summary['top_tlds']
    [('com', 4)]

    >>> url_summary['overview']
    {'num_posts': 4,
     'num_urls': 4,
     'urls_per_post': 1.0,
     'unique_urls': 4}
    """
    extracted = [URL.findall(x) for x in text_list]
    for urllist in extracted:
        for i, url in enumerate(urllist):
            if url.lower().startswith("www") or url.lower().startswith("ftp"):
                urllist[i] = "http://" + url
    domains = [[urlparse(u).netloc for u in e] for e in extracted]
    domains_flat = [item for sublist in domains for item in sublist]
    top_domains = sorted(
        Counter(domains_flat).items(), key=lambda x: x[1], reverse=True
    )
    tlds = [[d.split(".")[-1] for d in dom] for dom in domains]
    tlds_flat = [item for sublist in tlds for item in sublist]
    top_tlds = sorted(Counter(tlds_flat).items(), key=lambda x: x[1], reverse=True)
    summary = extract(text_list, URL, "url", extracted)
    summary["top_domains"] = top_domains
    summary["top_tlds"] = top_tlds
    return summary


def extract_words(text_list, words_to_extract, entire_words_only=False):
    """Return a summary dictionary about :attr:`words_to_extract` in
    :attr:`text_list`.

    Get a summary of the number of words, their frequency, the top
    ones, and more.

    Parameters
    ----------
    text_list : list
      A list of text strings.
    words_to_extract : list
      A list of words to extract from :attr:`text_list`.
    entire_words_only : bool
      Whether or not to find only complete words (as specified by :attr:`words_to_find`)
      or find any any of the words as part of longer strings.

    Returns
    -------
    summary : dict
      A dictionary with various stats about the words.

    Examples
    --------
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
    with ``entire_words_only=False``:

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
    if isinstance(words_to_extract, str):
        words_to_extract = [words_to_extract]

    text_list = [text.lower() for text in text_list]
    words_to_extract = [word.lower() for word in words_to_extract]

    if entire_words_only:
        regex = [r"\b" + x + r"\b" for x in words_to_extract]
        word_regex = re.compile(r"|".join(regex), re.IGNORECASE)
    else:
        regex = [r"\S*" + x + r"\S*" for x in words_to_extract]
        word_regex = re.compile("|".join(regex), re.IGNORECASE)

    return extract(text_list, word_regex, "word")
