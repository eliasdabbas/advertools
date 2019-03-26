import re
from collections import defaultdict

import advertools as adv
import pandas as pd

from advertools.word_tokenize import word_tokenize


def word_frequency(text_list, num_list=None, phrase_len=1, regex=None,
                   rm_words=adv.stopwords['english'], extra_info=False):
    """Count the absolute as well as the weighted frequency of words
    in ``text_list`` (based on ``num_list``).

    :param text_list: iterable of strings.
        Typically short phrases, but could be any list of full blown documents.
        Usually, you would use this to analyze tweets, book titles, URLs, etc.
    :param num_list: iterable of numbers.
        A list of numbers with the same length as ``text_list``, describing a
        certain attribute of these 'documents'; views, retweets, sales, etc.
    :param regex: string.
        The regex used to split words. Doesn't need changing in most cases.
    :param phrase_len: integer, the length in words of each token the
        text is split into, defaults to 1.
    :param rm_words: iterable of strings.
        Words to remove from the list 'stop-words'. The default uses
        ``spacy``'s list of English stopwords. To get all available languages
        run ``adv.stopwords.keys()``
    :param extra_info: boolean.
        Whether or not to give additional columns about the frequencies
    :returns abs_wtd_df: absolute and weighted DataFrame.
        pandas.DataFrame with several metrics calculated. The most important
        are ``abs_freq`` and ``wtd_freq``. These show the difference between
        the number of occurrences of each word together with their respective
        weighted occurrences (frequency vs. weighted frequency). Other metrics
        are also provided. The columns are as follows:

        word: Word.
            Words in the document list each on its own row. The length of
            these words is determined by ``token_word_len``, essentially
            phrases if containing more than one word each.
        abs_freq: Absolute frequency.
            The number of occurrences of each word in all the documents.
        wtd_freq: Weighted frequency.
            Every occurrence of ``word`` multiplied by its respective value in
            ``num_list`` provided by the function call.
        rel_value: Relative value.
            ``wtd_freq`` divided by ``abs_freq``, showing the value per
            occurrence of ``word``

        :extra_info:

        abs_perc: Absolute frequency percentage.
            ``abs_freq`` divided by the sum of all occurrences of words.
        abs_perc_cum: Cumulative absolute percentage.
            Cumulative sum of ``abs_perc`` to see how many words form x% of
            the occurrences.
        wtd_freq_perc: ``wtd_freq`` divided by the total weighted frequencies
            of all words.
        wtd_freq_perc_cum: Cumulative weighted frequncy percentage.
            Cumulative sum of ``wtd_freq_perc`` to see how many words form x%
            of the weighted occurrences.

    >>> text_list = ['apple orange', 'apple orange banana',
    ...              'apple kiwi', 'kiwi mango']
    >>> num_list = [100, 100, 100, 400]

    >>> adv.word_frequency(text_list, num_list)
         word  abs_freq  wtd_freq  rel_value
    0    kiwi         2       500      250.0
    1   mango         1       400      400.0
    2   apple         3       300      100.0
    3  orange         2       200      100.0
    4  banana         1       100      100.0

    "kiwi" occurred twice (abs_freq), one of these phrases has a score of 100,
    and the other 400, so the wtd_freq is the sum (100 + 400 = 500)

    >>> adv.word_frequency(text_list)  # num_list values default to 1 each
         word  abs_freq  wtd_freq  rel_value
    0   apple         3         3        1.0
    1  orange         2         2        1.0
    2    kiwi         2         2        1.0
    3  banana         1         1        1.0
    4   mango         1         1        1.0

    >>> text_list2 = ['my favorite color is blue',
    ... 'my favorite color is green', 'the best color is green',
    ... 'i love the color black']

    Setting ``token_word_len`` to 2, "words" become two-word phrases instead:

    >>> word_frequency(text_list2, token_word_len=2, rm_words=[])
                  word  abs_freq  wtd_freq  rel_value
    0         color is         3         3        1.0
    1      my favorite         2         2        1.0
    2   favorite color         2         2        1.0
    3         is green         2         2        1.0
    4          is blue         1         1        1.0
    5         the best         1         1        1.0
    6       best color         1         1        1.0
    7           i love         1         1        1.0
    8         love the         1         1        1.0
    9        the color         1         1        1.0
    10     color black         1         1        1.0

    >>> adv.word_frequency(text_list, num_list, extra_info=True)
         word  abs_freq  abs_perc  abs_perc_cum  wtd_freq  wtd_freq_perc  wtd_freq_perc_cum  rel_value
    0    kiwi         2  0.222222      0.222222       500       0.333333           0.333333      250.0
    1   mango         1  0.111111      0.333333       400       0.266667           0.600000      400.0
    2   apple         3  0.333333      0.666667       300       0.200000           0.800000      100.0
    3  orange         2  0.222222      0.888889       200       0.133333           0.933333      100.0
    4  banana         1  0.111111      1.000000       100       0.066667           1.000000      100.0

    This is the same result as above but giving the full DataFrame including
    all columns.
    """
    if num_list is None:
        num_list = [1 for i in range(len(text_list))]
    if isinstance(regex, str):
        regex = re.compile(regex)
        text_list = [' '.join(regex.findall(text)) for text in text_list]

    word_freq = defaultdict(lambda: [0, 0])

    for text, num in zip(word_tokenize(text_list, phrase_len=phrase_len),
                         num_list):
        for word in text:
            if word.lower() in rm_words:
                continue
            word_freq[word.lower()][0] += 1
            word_freq[word.lower()][1] += num

    columns = ['abs_freq', 'wtd_freq']

    abs_wtd_df = (pd.DataFrame.from_dict(word_freq, orient='index',
                                         columns=columns)
                  .sort_values('wtd_freq', ascending=False)
                  .assign(rel_value=lambda df: df['wtd_freq'] / df['abs_freq'])
                  .round())
    if extra_info:
        abs_wtd_df.insert(1, 'abs_perc', value=abs_wtd_df['abs_freq'] /
                          abs_wtd_df['abs_freq'].sum())
        abs_wtd_df.insert(2, 'abs_perc_cum', abs_wtd_df['abs_perc'].cumsum())
        abs_wtd_df.insert(4, 'wtd_freq_perc', abs_wtd_df['wtd_freq'] /
                          abs_wtd_df['wtd_freq'].sum())
        abs_wtd_df.insert(5, 'wtd_freq_perc_cum',
                          abs_wtd_df['wtd_freq_perc'].cumsum())

    abs_wtd_df = abs_wtd_df.reset_index().rename(columns={'index': 'word'})

    return abs_wtd_df
