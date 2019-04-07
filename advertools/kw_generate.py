
__all__ = ['kw_broad', 'kw_exact', 'kw_generate', 'kw_modified',
           'kw_neg_broad', 'kw_neg_exact', 'kw_neg_phrase',
           'kw_phrase']

import re
from itertools import permutations, combinations

import pandas as pd


def kw_generate(products, words, max_len=3,
                match_types=('Exact', 'Phrase', 'Modified'),
                order_matters=True, campaign_name='SEM_Campaign'):
    """Generate a data frame of keywords using a list of products and relevant
    words.

    :param products: will be used as the names of the ad groups
    :param words: related words that make it clear that the user is interested
        in ``products``
    :param max_len: the maximum number of words to include in each permutation
        of product keywords
    :param match_types: can be restricted or kept as is based on preference,
        possible values: 'Exact', 'Phrase', 'Modified', 'Broad'
    :param order_matters: whether or not the order of words in keywords
        matters, default False
    :param campaign_name: name of campaign
    :returns keywords_df: a pandas.DataFrame ready to upload

    >>> import advertools as adv
    >>> products = ['bmw', 'toyota']
    >>> words = ['buy', 'second hand']
    >>> kw_df = adv.kw_generate(products, words)
    >>> kw_df.head()
           Campaign Ad Group          Keyword Criterion Type       Labels
    0  SEM_Campaign      Bmw          bmw buy          Exact          Buy
    1  SEM_Campaign      Bmw          bmw buy         Phrase          Buy
    2  SEM_Campaign      Bmw        +bmw +buy          Broad          Buy
    3  SEM_Campaign      Bmw  bmw second hand          Exact  Second Hand
    4  SEM_Campaign      Bmw  bmw second hand         Phrase  Second Hand

    >>> kw_df.tail()
            Campaign Ad Group                    Keyword Criterion Type           Labels
    55  SEM_Campaign   Toyota     second hand toyota buy         Phrase  Second Hand;Buy
    56  SEM_Campaign   Toyota  +second hand +toyota +buy          Broad  Second Hand;Buy
    57  SEM_Campaign   Toyota     second hand buy toyota          Exact  Second Hand;Buy
    58  SEM_Campaign   Toyota     second hand buy toyota         Phrase  Second Hand;Buy
    59  SEM_Campaign   Toyota  +second hand +buy +toyota          Broad  Second Hand;Buy
    """
    match_types = [x.title() for x in match_types]
    possible_match_types = ['Exact', 'Phrase', 'Broad', 'Modified']
    if not set(match_types).issubset(possible_match_types):
        raise ValueError('please make sure match types are any of '
                         + str(possible_match_types))

    if max_len < 2:
        raise ValueError('please make sure max_len is >= 2')

    comb_func = permutations if order_matters else combinations
    headers = ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type', 'Labels']
    keywords_list = []
    for prod in products:
        for i in range(2, max_len+1):
            for comb in comb_func([prod] + words, i):
                if prod not in comb:
                    continue
                for match in match_types:
                    row = [
                        campaign_name,
                        prod.title(),
                        (' '.join(comb) if match != 'Modified' else
                            '+' + ' '.join(comb).replace(' ', ' +')),
                        match if match != 'Modified' else 'Broad',
                        ';'.join([x.title() for x in comb if x != prod])
                    ]
                    keywords_list.append(row)
    return pd.DataFrame.from_records(keywords_list, columns=headers)


def kw_broad(words):
    """Return ``words`` in broad match.

    :param words: list of strings
    :returns formatted: `words` in broad match type

    >>> keywords = ['[learn guitar]', '"guitar courses"', '+guitar +tutor']
    >>> kw_broad(keywords)
    ['learn guitar', 'guitar courses', 'guitar tutor']
    """
    regex = r'^\'|^\"|\'$|\"$|\+|^\[|\]$|^-'
    return [re.sub(regex, '', x) for x in words]


def kw_exact(words):
    """Return ``words`` in exact match.

    :param words: list of strings
    :returns formatted: `words` in exact match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_exact(keywords)
    ['[learn guitar]', '[guitar courses]', '[guitar tutor]']
    """
    return ['[' + w + ']' for w in kw_broad(words)]


def kw_phrase(words):
    """Return ``words`` in phrase match.

    :param words: list of strings
    :returns formatted: `words` in phrase match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_phrase(keywords)
    ['"learn guitar"', '"guitar courses"', '"guitar tutor"']
    """
    return ['"' + w + '"' for w in kw_broad(words)]


def kw_modified(words):
    """Return ``words`` in modified broad match.

    :param words: list of strings
    :returns formatted: `words` in modified broad match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_modified(keywords)
    ['+learn +guitar', '+guitar +courses', '+guitar +tutor']
    """
    return ['+' + w.replace(' ', ' +') for w in kw_broad(words)]


def kw_neg_broad(words):
    """Return ``words`` in negative broad match.

    :param words: list of strings
    :returns formatted: `words` in negative broad match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_neg_broad(keywords)
    ['-learn guitar', '-guitar courses', '-guitar tutor']
    """
    return ['-' + w for w in kw_broad(words)]


def kw_neg_phrase(words):
    """Return ``words`` in negative phrase match.

    :param words: list of strings
    :returns formatted: `words` in negative phrase match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_neg_phrase(keywords)
    ['-"learn guitar"', '-"guitar courses"', '-"guitar tutor"']
    """
    return ['-' + w for w in kw_phrase(words)]


def kw_neg_exact(words):
    """Return ``words`` in negative exact match.

    :param words: list of strings
    :returns formatted: `words` in negative exact match type

    >>> keywords = ['learn guitar', 'guitar courses', 'guitar tutor']
    >>> kw_neg_exact(keywords)
    ['-[learn guitar]', '-[guitar courses]', '-[guitar tutor]']
    """
    return ['-' + w for w in kw_exact(words)]
