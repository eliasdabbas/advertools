
from itertools import permutations

import pandas as pd

def kw_generate(products, words, max_len=3, match_types=['Exact', 'Phrase', 'Modified'],
                campaign_name='SEM_Campaign'):
    """Generate a data frame of kewywords using a list of products and relevant words.
    
    Parameters
    ----------
    
    products : will be used as the names of the ad groups
    words : related words that make it clear that the user is interested in `products`
    max_len : the maximum number of words to include in each permutation of product keywords
    match_types : can be restricted or kept as is based on preference, possible values:
        'Exact', 'Phrase', 'Modified', 'Broad'
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
    
    
    Returns
    -------
    
    keywords_df : a pandas.DataFrame ready to upload
    
    """
    POSSIBLE_MATCH_TYPES = ['Exact', 'Phrase', 'Broad', 'Modified']
    if not all([m in POSSIBLE_MATCH_TYPES for m in match_types]):
        raise ValueError('please make sure match types are any of ' + str(POSSIBLE_MATCH_TYPES))

    if max_len < 2:
        raise ValueError('please make sure max_len is >= 2')
        
    
    headers = ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type', 'Labels']
    keywords_list = []
    for prod in products:
        for i in range(2, max_len+1):
            for perm in permutations([prod] + words, i):
                if prod not in perm:
                    continue
                for match in match_types:
                    row = [
                        campaign_name,
                        prod.title(),
                        ' '.join(perm) if match != 'Modified' else '+' + ' +'.join(perm),
                        match,
                        ';'.join([x.title() for x in perm if x != prod])
                    ]
                    keywords_list.append(row)
    return pd.DataFrame.from_records(keywords_list, columns=headers)