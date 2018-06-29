import re
from itertools import permutations, combinations

import pandas as pd

def kw_generate(products, words, max_len=3, match_types=['Exact', 'Phrase', 'Modified'],
                order_matters=True, campaign_name='SEM_Campaign'):
    """Generate a data frame of keywords using a list of products and relevant words.
        
    products : will be used as the names of the ad groups
    words : related words that make it clear that the user is interested in `products`
    max_len : the maximum number of words to include in each permutation of product keywords
    match_types : can be restricted or kept as is based on preference, possible values:
        'Exact', 'Phrase', 'Modified', 'Broad'
    order_matters : whether or not the order of words in keywords matters, default False
    campaign_name : name of campaign
    >>> import advertools as adv
    >>> products = ['bmw', 'toyota']
    >>> words = ['buy', 'second hand']
    >>> kw_df = adv.kw_generate(products, words)
    >>> kw_df.head()
           Campaign Ad Group          Keyword Criterion Type       Labels
    0  SEM_Campaign      Bmw          bmw buy          Exact          Buy
    1  SEM_Campaign      Bmw          bmw buy         Phrase          Buy
    2  SEM_Campaign      Bmw        +bmw +buy       Modified          Buy
    3  SEM_Campaign      Bmw  bmw second hand          Exact  Second Hand
    4  SEM_Campaign      Bmw  bmw second hand         Phrase  Second Hand
    
    >>> kw_df.tail()
            Campaign Ad Group                    Keyword Criterion Type \
    13  SEM_Campaign   Toyota         toyota second hand         Phrase
    14  SEM_Campaign   Toyota       +toyota +second hand          Broad
    15  SEM_Campaign   Toyota     toyota buy second hand          Exact
    16  SEM_Campaign   Toyota     toyota buy second hand         Phrase
    17  SEM_Campaign   Toyota  +toyota +buy +second hand          Broad

             Labels
    13      Second Hand
    14      Second Hand
    15  Buy;Second Hand
    16  Buy;Second Hand
    17  Buy;Second Hand

    Returns
    -------
    
    keywords_df : a pandas.DataFrame ready to upload
    
    """
    match_types = [x.title() for x in match_types]
    POSSIBLE_MATCH_TYPES = ['Exact', 'Phrase', 'Broad', 'Modified']
    if not set(match_types).issubset(POSSIBLE_MATCH_TYPES):
        raise ValueError('please make sure match types are any of ' + str(POSSIBLE_MATCH_TYPES))

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
                        ' '.join(comb) if match != 'Modified' else '+' + ' +'.join(comb).replace(' ', ' +'),
                        match if match != 'Modified' else 'Broad',
                        ';'.join([x.title() for x in comb if x != prod])
                    ]
                    keywords_list.append(row)
    return pd.DataFrame.from_records(keywords_list, columns=headers)

def kw_broad(words):
    regex = '^\'|^\"|\'$|\"$|\+|^\[|\]$|^-'
    return [re.sub(regex, '',  ''  + x) for x in words]

def kw_exact(words):
    return ['[' + w + ']' for w in kw_broad(words)]

def kw_phrase(words):
    return ['"' + w + '"' for w in kw_broad(words)]

def kw_modified(words):
    return ['+' + w.replace(' ', ' +') for w in kw_broad(words)]

def kw_neg_broad(words):
    return ['-' + w for w in kw_broad(words)]

def kw_neg_phrase(words):
    return ['-' + w for w in kw_phrase(words)]

def kw_neg_exact(words):
    return ['-' + w for w in kw_exact(words)]
