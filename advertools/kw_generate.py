
from itertools import permutations

def kw_generate(products, words, max_len=3, match_types=['Exact', 'Phrase', 'Broad'],
                campaign_name='SEM_Campaign'):
    """Generate a data frame of kewywords using a list of products and relevant words.
    `products` will be used as the nams of the ad groups
    `words` are any related words that make it clear that the user is interested in `products`
    `max_len` is the maximum number of words to include in each permutation to product keywords
    `match_types` can be restricted or kept as is based on preference
    `campaign_name` name of campaign! 
    
    >>> products = ['bmw', 'toyota']
    >>> words = ['buy', 'second hand']
    >>> kw_df = kw_generate(products, words)
    >>> kw_df.head()
           Campaign Ad Group          Keyword Criterion Type
    0  SEM_Campaign      bmw          bmw buy          Exact
    1  SEM_Campaign      bmw          bmw buy         Phrase
    2  SEM_Campaign      bmw          bmw buy          Broad
    3  SEM_Campaign      bmw  bmw second hand          Exact
    4  SEM_Campaign      bmw  bmw second hand         Phrase
    """
    headers = ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type']
    keywords_list = []
    for prod in products:
        for i in range(2, max_len+1):
            for perm in permutations([prod] + words, i):
                if prod not in perm:
                    continue
                for match in match_types:
                    row = [
                        campaign_name,
                        prod,
                        ' '.join(perm),
                        match
                    ]
                    keywords_list.append(row)
    return pd.DataFrame.from_records(keywords_list, columns=headers)