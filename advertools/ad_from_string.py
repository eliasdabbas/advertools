"""
.. _ad_from_string:

Create Ads Using Long Descriptive Text (top-down approach)
==========================================================

"""

import string


def ad_from_string(s, slots=(30, 30, 30, 90, 90, 15, 15), sep=None,
                   capitalize=False):
    """Convert string :attr:`s` to an ad by splitting it into groups of words.
    Each group would have a length of at most the allowed length for that slot.

    If the total length of :attr:`s` exceeds the total allowed length, all
    remaining characters would be grouped in the last element of the
    returned list.

    :param str s: a string of characters, with no restrictions on length
    :param list slots: an iterable of integers for the maximum lengths for
        each slot
    :param str sep: character(s) by which to split :attr:`s`
    :param bool capitalize: whether or not to capitalize each word after
                            grouping. Setting it as False would not change the
                            capitalization of the input string
    :returns text_ad: a list of strings

    >>> ad_from_string('this is a short ad')
    ['this is a short ad', '', '', '', '', '', '', '']

    >>> ad_from_string('this is a longer ad and will take the first two slots')
    ['this as a longer ad and would', 'take the first two slots',
    '', '', '', '', '', '']

    >>> ad_from_string("Slots can be changed the way you want", (10, 15, 10))
    ['Slots can', 'be changed the', 'way you', 'want']

    >>> ad_from_string("The capitalization REMAinS as IS bY DefAULt",
    ...                       (10, 15, 10))
    ['The', 'capitalization', 'REMAinS as', 'IS bY DefAULt']

    >>> ad_from_string("set captialize=True to capitalize first letters",
    ...                capitalize=True)
    ['Set Captialize=true To', 'Capitalize First Letters',
     '', '', '', '', '', '']
    """
    str_words = s.split(sep=sep)
    text_ad = ['' for x in range(len(slots)+1)]
    counter = 0

    for i, slot in enumerate(slots):
        while counter <= len(str_words) - 1:
            if len(text_ad[i] + str_words[counter]) + 1 > slot:
                break
            text_ad[i] += (' ' + str_words[counter] if text_ad[i]
                           else str_words[counter])
            counter += 1

    text_ad[-1] = (sep.join(str_words[counter:])
                   if sep is not None else ' '.join(str_words[counter:]))

    return [string.capwords(x) if capitalize else x for x in text_ad]
