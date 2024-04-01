"""
.. _ad_from_string:

Create Ads Using Long Descriptive Text (top-down approach)
==========================================================

Many times you have long descriptive text about your products, especially on
their respective landing pages. The allowed length of text ads has become
considerably long on many platforms. On Google Ads for example, you have slots
of 30, 30, 30, 90, and 90 characters, for a total of 270. That's more than
enough space to talk about the main features of your product.

The question is, how do you utilize that long description text that has all the
details that you want, and make sure it fits correctly within the limits given
by the platform you are using?

The :func:`ad_from_string` function does exactly that. Given a long string, it
divides it into slots of any given length that you specify, and if any text
remains it will be appended to the end of the returned list.

Another important benefit of this is that you can take those long descriptions
(or write them) once, and then you can easily split them into different slots
based on the ad format and the platform you are using.

Here is a quick overview of the available parameters and options:

.. glossary::

    s
        The string that you want to split. This would typically be available
        on the landing pages of each product.

    slots

        The lengths that you want to split into. Note that although the default
        uses Google Ads' text ad template, you can change it to any other
        group of slots, with more or fewer slots of different lengths.

    sep

        The separator by which to split the text. The default is :attr:`None`
        which splits the text by whitespace, but you can change it to something
        else if needed. Sometimes you might want the text split by hyphens
        (URLs for example) so you can split by that character.

    capitalize

        The default is :attr:`False` which leaves the capitalization of
        :attr:`s` intact. If you set it to :attr:`True` then the first letter
        of each word would be capitalized.


**Example**

Note that in any case, the returned list of characters is longer than the
provided slots by one. So if you provide five slots, for example, the function
will always return a list of length six.

This is to ensure that the remainder of the text is not lost if it is longer,
so you know what is missing. In case you have shorter text, you will still have
one element more than the provided slots to ensure consistency.

.. thebe-button::
    Run this code


.. code-block::
    :class: thebe, thebe-init

    import advertools as adv
    desc_text = "Get the latest gadget online. The GX12 model comes with 13 things that do a lot of good stuff for your health. Start shopping now."
    len(desc_text)  # 130



Now let's see how this same description can be utilized in different scenarios

Google Text Ads
^^^^^^^^^^^^^^^

Since this is shorter than the default Google values, you will get extra empty
slots (with an additional last one).

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    adv.ad_from_string(desc_text)  # default values (Google text ads)

.. code-block::

    ['Get the latest gadget online.',
    'The GX12 model comes with 13',
    'things that do a lot of good',
    'stuff for your health. Start shopping now.',
    '',
    '',
    '',
    '']

Facebook Feed Ads
^^^^^^^^^^^^^^^^^

In this case, it is also shorter than the default value, so you get an extra
space.

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    adv.ad_from_string(desc_text, [125, 25, 30])  # Facebook feed ads

.. code-block:

    ['Get the latest gadget online. The GX12 model comes with 13 things that do a lot\
     of good stuff for your health. Start shopping',
    'now.',
    '',
    '']

Since it might not look good having just one word in the second slot, and an
empty last one, you might want to change it as follows:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    adv.ad_from_string(desc_text, [90, 25, 30])

.. code-block::

    ['Get the latest gadget online. The GX12 model comes with 13 things that do a lot of good',
    'stuff for your health.',
    'Start shopping now.',
    '']


Facebook Instant Article Ad
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here is a case where our text is longer than the provided limitations, so we
end up having an extra space that is not used:

.. thebe-button::
    Run this code

.. code-block::
    :class: thebe, thebe-init

    adv.ad_from_string(desc_text, [25, 30])  # Facebook instant article ad

.. code-block::

    ['Get the latest gadget',
    'online. The GX12 model comes',
    'with 13 things that do a lot of good stuff for your health. Start shopping now.']
"""  # noqa: E501

import string


def ad_from_string(s, slots=(30, 30, 30, 90, 90, 15, 15), sep=None, capitalize=False):
    """Convert string :attr:`s` to an ad by splitting it into groups of words.

    Each group would have a length of at most the allowed length for that slot.

    If the total length of :attr:`s` exceeds the total allowed length, all
    remaining characters would be grouped in the last element of the
    returned list.

    Parameters
    ----------
    s : str
      A string of characters, with no restrictions on length.
    slots : list
      An iterable of integers for the maximum lengths for each slot
    sep : str
      Character(s) by which to split :attr:`s`.
    capitalize : bool
      Whether or not to capitalize each word after grouping. Setting it as False would
      not change the capitalization of the input string

    Returns
    -------
    text_ad : list
      A list of strings according to split spec.

    Examples
    --------
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
    text_ad = ["" for x in range(len(slots) + 1)]
    counter = 0

    for i, slot in enumerate(slots):
        while counter <= len(str_words) - 1:
            if len(text_ad[i] + str_words[counter]) + 1 > slot:
                break
            text_ad[i] += " " + str_words[counter] if text_ad[i] else str_words[counter]
            counter += 1

    text_ad[-1] = (
        sep.join(str_words[counter:])
        if sep is not None
        else " ".join(str_words[counter:])
    )

    return [string.capwords(x) if capitalize else x for x in text_ad]
