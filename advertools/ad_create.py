"""
.. _ad_create:

Create Ads on a Large Scale
===========================

When creating large-scale campaigns, you also need to create ads on a large
scale. For products in a similar category you typically want to use the same
ads, but only replace the product name, "Get the latest <product> now", and
replace `product` as many times as you have ads.

.. container:: thebe

    .. thebe-button::
        Run this code


    .. code-block::
        :class: thebe, thebe-init

        import advertools as adv

        products = ['Dubai', 'Tokyo', 'Singapore']
        adv.ad_create(template='5-star Hotels in {}',
                    replacements=products,
                    max_len=30,
                    fallback='Great Cities')

    .. container:: output

        .. code-block::

            ['5-star Hotels In Dubai',
            '5-star Hotels In Tokyo',
            '5-star Hotels In Singapore']

An important thing to to watch out for, is long product names. Since text ads
have limits on each slot, you need to make sure you don't exceed that limit.
For this you need to provide a `fallback` text in case the product name is
longer than `max_len`.

.. container:: thebe

    .. thebe-button::
        Run this code

    .. code-block::
        :class: thebe, thebe-init

        products = ['Lisbon', 'Porto', 'Algarve', 'Freixo de Espada à Cinta']
        adv.ad_create(template='5-star Hotels in {}',
                    replacements=products,
                    max_len=30,
                    fallback='Portugal')
    .. container:: output

        .. code-block::

            ['5-star Hotels In Lisbon',
            '5-star Hotels In Porto',
            '5-star Hotels In Algarve',
            '5-star Hotels In Portugal']

"""

import string


def ad_create(template, replacements, fallback, max_len=30, capitalize=True):
    """Insert each of the replacement strings in its place within template.

    Parameters
    ----------
    template : str
      A string format template, using braces e.g. "Get the latest {} today."
    replacements : list
      Replacement strings to be inserted in :attr:`template`.
    fallback : str
      The string to insert in :attr:`template` in case :attr:`replacement` is longer
      than :attr:`max_len`.
    max_len : int
      The maximum allowed length of the full string.
    capitalize : bool
      Whether or not to capitalize words in the result.

    Returns
    -------
    formatted : list
      List of ads (strings).

    Examples
    --------
    >>> ad_create("Let's count {}", ["one", "two", "three"], "one", 20)
    ["Let's Count One", "Let's Count Two", "Let's Count Three"]

    >>> ad_create(
    ...     template="My favorite car is {}",
    ...     replacements=["Toyota", "BMW", "Mercedes", "Lamborghini"],
    ...     fallback="great",
    ...     max_len=28,
    ... )
    ['My Favorite Car Is Toyota', 'My Favorite Car Is Bmw',
    'My Favorite Car Is Mercedes', 'My Favorite Car Is Great']

    >>> ad_create(
    ...     "KeEP cApITalization {}",
    ...     ["As IS"],
    ...     fallback="fallback",
    ...     max_len=50,
    ...     capitalize=False,
    ... )
    ['KeEP cApITalization As IS']

    >>> ad_create(
    ...     "This is very long and will produce and error",
    ...     replacements=["something", "long"],
    ...     fallback="Very long",
    ...     max_len=20,
    ... )
    Traceback (most recent call last):
    File "<input>", line 1, in <module>
    File "<input>", line 26, in ad_create
    ValueError: template + fallback should be <= 20 chars
    """
    if len(template.format(fallback)) > max_len:
        raise ValueError("template + fallback should be <= " + str(max_len) + " chars")
    final_ad = []
    for rep in replacements:
        if len(template.format(rep)) <= max_len:
            final_ad.append(template.format(rep))
        else:
            final_ad.append(template.format(fallback))

    return [string.capwords(s) for s in final_ad] if capitalize else final_ad
