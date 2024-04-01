"""
.. _word_frequency:

Text Analysis
#############

Absolute and Weighted Word Count
================================

When analyzing a corpus of documents (I'll simply call it a text list), one of
the main tasks to accomplish to start text mining is to first count the words.
While there are many text mining techniques and approaches, the
:func:`word_frequency` function works mainly by counting words in a text list.
A "word" is defined as a sequence of characters split by whitespace(s), and
stripped of non-word characters (commas, dots, quotation marks, etc.).
A "word" is actually a phrase consisting of one word, but you have the option
of getting phrases that have two words, or more. This can be done simply
by providing a value for the :attr:`phrase_len` parameter.

Absolute vs Weighted Frequency
------------------------------

In social media reports, analytics, keyword reports, url and page reports, we
get more information than simply the text. We get numbers describing those
posts or page titles, or product names, or whatever the text list might
contain. Numbers can be pageviews, shares, likes, retweets, sales, bounces,
sales, etc. Since we have numbers to quantify those phrases, we can improve our
counting by taking into consideration the number list that comes with the text
list.

For example, if you have an e-commerce site that has two products, let's say
you have bags and shoes, then your products are split 50:50 between bags and
shoes.
But what if you learn that shoes generate 80% of your sales?
Although shoes form half your products, they generate 80% of your revenue. So
the *weighted count* of your products is 80:20.

Let's say two people post two different posts on a social media platform. One
of them says, "It's raining", and the other says, "It's snowing". As in the
above example, the content is split 50:50 between "raining" and "snowing", but
we get a much more informative picture if we get the number of followers of
each of those accounts (or the number of shares, likes, etc.). If one of them
has a thousand followers, and other has a million (which is typical on social
media, as well as in pageviews report, e-commerce and most other datasets),
then you get a completely different picture about your dataset.

These two simple examples contain two posts, and a word each. The
:func:`word_frequency` function can provide insight on hidden trends especially
in large datasets, and when the sentences or phrases are also longer then a
word or two each.

Let's take a look at how to use the :func:`word_frequency` function, and what
the available parameters and options are.


.. glossary::

    text_list
        The list of phrases or documents that you want to analyze. Here are
        some possible ideas that you might use this for:

            * keywords, whether in a PPC or SEO report
            * page titles in an analytics report
            * social media posts (tweets, Facebook posts, YouTube video titles
              or descriptions etc.)
            * e-commerce reports (where the text would be the product names)

    num_list
        Ideally, if you have more than one column describing :attr:`text_list`
        you should experiment with different options. Try weighting the words
        by pageviews, then try by bounce rate and see if you get different
        interesting findings.
        With e-commerce reports, you can see which word appears the most, and
        which word is associated with more revenue.

    phrase_len
        You should also experiment with different lengths of phrases. In many
        cases, one-word phrases might not be as meaningful as two-words or
        three.

    regex
        The default is to simply split words by whitespace, and provide phrases
        of length :attr:`phrase_len`.
        But you may want to count the occurrences of certain patterns of text.
        Check out the :ref:`regex <regex>` module for the available regular
        expressions that might be interesting. Some of the pre-defined ones are
        hashtags, mentions, questions, emoji, currencies, and more.

    rm_words
        A list of words to remove and ignore from the count. Known as
        stop-words these are the most frequently used words in a language,
        the most used, but don't add much meaning to the content (a, and, of,
        the, if, etc.). By default a set of English stopwords is provided
        (which you can check and possibly may want to modify), or run
        ``adv.stopwords.keys()`` to get a list of all the available stopwords
        in the available languages.
        In some cases (like page titles for example), you might get "words"
        that need to be removed as well, like the pipe "|" character for
        example.

    extra_info
        The returned DataFrame contains the default columns
        ``[word, abs_freq, wtd_freq, rel_value]``. You can get extra
        columns for percentages and cumulative percentages that add perspective
        to the other columns. Set this parameter to :attr:`True` if you want
        that.

Below are all the columns of the returned DataFrame:

=========================  ================================================
:attr:`word`               Words in the document list each on its own row.
                           The length of these words is determined by
                           :attr:`phrase_len`, essentially phrases if
                           containing more than one word each.
:attr:`abs_freq`           The number of occurrences of each word in all
                           the documents.
:attr:`wtd_freq`           Every occurrence of :attr:`word` multiplied by
                           its respective value in :attr:`num_list`.
:attr:`rel_value`          :attr:`wtd_freq` divided by :attr:`abs_freq`,
                           showing the value per occurrence of :attr:`word`
:attr:`abs_perc`           Absolute frequency percentage.
:attr:`abs_perc_cum`       Cumulative absolute percentage.
:attr:`wtd_freq_perc`      Weighted frequency percentage.
:attr:`wtd_freq_perc_cum`  Cumulative weighted frequency percentage.
=========================  ================================================

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    import advertools as adv
    import pandas as pd
    tweets = pd.read_csv('data/tweets.csv')
    tweets

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


.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    word_freq = adv.word_frequency(text_list=tweets['tweet_text'],
                                   num_list=tweets['followers_count'])

    # try sorting by 'abs_freq', 'wtd_freq', and 'rel_value':
    word_freq.sort_values(by='abs_freq', ascending=False).head(25)

"""  # noqa: E501

import re
from collections import defaultdict

import pandas as pd

import advertools as adv
from advertools.word_tokenize import word_tokenize


def word_frequency(
    text_list,
    num_list=None,
    phrase_len=1,
    regex=None,
    rm_words=adv.stopwords["english"],
    extra_info=False,
):
    """Count the absolute as well as the weighted frequency of words
    in :attr:`text_list` (based on :attr:`num_list`).

    Parameters
    ----------
    text_list : list
      Typically short phrases, but could be any list of full blown documents. Usually,
      you would use this to analyze tweets, book titles, URLs, etc.
    num_list : list
      A list of numbers with the same length as :attr:`text_list`, describing a certain
      attribute of these 'documents'; views, retweets, sales, etc.
    regex : str
      The regex used to split words. Doesn't need changing in most cases.
    phrase_len : int
      The length in words of each token the text is split into (ngrams), defaults to 1.
    rm_words : set
      Words to remove from the list a.k.a 'stop-words'. The default uses. To get all
      available languages run ``adv.stopwords.keys()``.
    extra_info : bool
      Whether or not to give additional metrics about the frequencies.

    Returns
    -------
    abs_wtd_df : pandas.DataFrame
      Absolute and weighted counts DataFrame.

    Examples
    --------
    >>> import advertools as adv
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

    Although "kiwi" occurred twice :attr:`abs_freq`, and "apple" occurred three
    times, the phrases in which "kiwi" appear have a total score of 500,
    so it beats "apple" on :attr:`wtd_freq` even though "apple" wins on
    :attr:`abs_freq`. You can sort by any of the columns of course.
    :attr:`rel_value` shows the value per occurrence of each word, as you can
    see, it is simply obtained by dividing :attr:`wtd_freq` by
    :attr:`abs_freq`.

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

    Setting :attr:`phrase_len` to 2, "words" become two-word phrases instead.
    Note that we are setting :attr:`rm_words` to the empty list so we can keep
    the stopwords and see if that makes sense:

    >>> word_frequency(text_list2, phrase_len=2, rm_words=[])
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

    The same result as above showing all possible columns by setting
    :attr:`extra_info` to :attr:`True`:

    >>> adv.word_frequency(text_list, num_list, extra_info=True)
         word  abs_freq  abs_perc  abs_perc_cum  wtd_freq  wtd_freq_perc  wtd_freq_perc_cum  rel_value
    0    kiwi         2  0.222222      0.222222       500       0.333333           0.333333      250.0
    1   mango         1  0.111111      0.333333       400       0.266667           0.600000      400.0
    2   apple         3  0.333333      0.666667       300       0.200000           0.800000      100.0
    3  orange         2  0.222222      0.888889       200       0.133333           0.933333      100.0
    4  banana         1  0.111111      1.000000       100       0.066667           1.000000      100.0
    """  # noqa: E501
    if num_list is None:
        num_list = [1 for _ in range(len(text_list))]
    if isinstance(regex, str):
        regex = re.compile(regex)
        text_list = [" ".join(regex.findall(text)) for text in text_list]

    word_freq = defaultdict(lambda: [0, 0])

    for text, num in zip(word_tokenize(text_list, phrase_len=phrase_len), num_list):
        for word in text:
            if word.lower() in rm_words:
                continue
            word_freq[word.lower()][0] += 1
            word_freq[word.lower()][1] += num

    columns = ["abs_freq", "wtd_freq"]

    abs_wtd_df = (
        pd.DataFrame.from_dict(word_freq, orient="index", columns=columns)
        .sort_values("wtd_freq", ascending=False)
        .assign(rel_value=lambda df: df["wtd_freq"] / df["abs_freq"])
        .round()
    )
    if extra_info:
        abs_wtd_df.insert(
            1, "abs_perc", value=abs_wtd_df["abs_freq"] / abs_wtd_df["abs_freq"].sum()
        )
        abs_wtd_df.insert(2, "abs_perc_cum", abs_wtd_df["abs_perc"].cumsum())
        abs_wtd_df.insert(
            4, "wtd_freq_perc", abs_wtd_df["wtd_freq"] / abs_wtd_df["wtd_freq"].sum()
        )
        abs_wtd_df.insert(5, "wtd_freq_perc_cum", abs_wtd_df["wtd_freq_perc"].cumsum())

    abs_wtd_df = abs_wtd_df.reset_index().rename(columns={"index": "word"})
    if set(num_list) == {1}:
        abs_wtd_df = abs_wtd_df.drop(["wtd_freq", "rel_value"], axis=1)
    return abs_wtd_df
