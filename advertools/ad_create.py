import string


def ad_create(template, replacements, fallback, max_len=30, capitalize=True):
    """Insert each of the replacement strings in its place within template.

    :param template: a string format template, using braces
    :param replacements: replacements string to be inserted in template
    :param fallback: the string to insert in template in case the replacement
        is too long
    :param max_len: the maximum allowed length of the full string
    :param capitalize: whether or not to capitalize words in the result
    :returns formatted: list of strings

    >>> ad_create("Let\'s count {}", ['one', 'two', 'three'], 'one', 20)
    ["Let's Count One", "Let's Count Two", "Let's Count Three"]

    >>> ad_create(template='My favorite car is {}',
    ...           replacements=['Toyota', 'BMW', 'Mercedes', 'Lamborghini'],
    ...           fallback='great',
    ...           max_len=28)
    ['My Favorite Car Is Toyota', 'My Favorite Car Is Bmw',
    'My Favorite Car Is Mercedes', 'My Favorite Car Is Great']

    >>> ad_create('KeEP cApITalization {}', ['As IS'],
    ...           fallback='fallback', max_len=50, capitalize=False)
    ['KeEP cApITalization As IS']

    >>> ad_create('This is very long and will produce and error',
    ...           replacements=['something', 'long'], fallback='Very long',
    ...           max_len=20)
    Traceback (most recent call last):
    File "<input>", line 1, in <module>
    File "<input>", line 26, in ad_create
    ValueError: template + fallback should be <= 20 chars
    """
    if len(template.format(fallback)) > max_len:
        raise ValueError('template + fallback should be <= '
                         + str(max_len) + ' chars')
    final_ad = []
    for rep in replacements:
        if len(template.format(rep)) <= max_len:
            final_ad.append(template.format(rep))
        else:
            final_ad.append(template.format(fallback))

    return [string.capwords(s) for s in final_ad] if capitalize else final_ad
