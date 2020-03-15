"""
A big part of setting up SEM campaigns consists of generating keywords, and
properly mapping them to landing pages and ads, as well as putting them in the
right campaign and ad group structure.

Keyword research is the part of this task that takes the most time. It is
very tedious, yet extremely important.

The shift here is that we are going to be *generating* keywords as opposed to
researching them.

What is a keyword anyway?

It is basically a phrase that contains two things:

:Product: This is the thing that you are selling. It is simply the name of it.
          "barcelona", "guitar", "rio de janeiro", "accounting".
          The product on its own is not enough for us to understand what the
          user is looking for. "barcelona trips" and "barcelona football club"
          are completely different "keywords" for example.

:Word: To give meaning to the product, it has to come with a word. The word
       can be a verb like "buy" or "purchase", and it can also be another noun,
       but with a clear intent expressed; "price" and "offers" for example
       clearly show purchase intent.

So, to *generate* keywords we need phrases that contain both, the product and
the descriptive word(s).
It is very easy to get the products as you know what you sell.
The next thing you need to come up with are the words that work within your
strategy.
The most import idea here is that once you determine that you sell courses for
example, there aren't really that many words that can describe that intent;
course, courses, tutorial, certification, learn, learning, education, etc.
How many can you come up with? How many exist in any language? Fifteen, twenty?
Once you have those are basically done.

Depending on what service you provide and what segment of the market you target
it shouldn't be difficult to come up with ideas for words (not keywords yet).
You might have an e-commerce site, but want to mainly focus on cheap and
discounted products. Or maybe you have luxury items, and want to exclude words
that signify price sensitivity.

Let's say you have a job site and you know that you provide jobs for
engineering, graphic design, and marketing.
The words are easy to come up with; "job", "jobs", "careers", "vacancies",
"full time", "part time", "work", and so on.

Now what we can do is use the `kw_generate` function to come up with all
possible combinations (order doesn't matter) and/or permutations (order
matters) and get a ready-to-use table to upload and start running the campaign.

>>> products = ['enginering', 'graphic design', 'marketing']
>>> words = ['jobs', 'careers', 'vacancies', 'full time', 'part time']
>>> adv.kw_generate(products, words)
         Campaign    Ad Group                             Keyword    Criterion Type               Labels
0    SEM_Campaign  Enginering                     enginering jobs             Exact                 Jobs
1    SEM_Campaign  Enginering                     enginering jobs            Phrase                 Jobs
2    SEM_Campaign  Enginering                   +enginering +jobs             Broad                 Jobs
3    SEM_Campaign  Enginering                  enginering careers             Exact              Careers
4    SEM_Campaign  Enginering                  enginering careers            Phrase              Careers
..            ...         ...                                 ...              ...                  ...
625  SEM_Campaign   Marketing       part time vacancies marketing            Phrase   Part Time;Vacancies
626  SEM_Campaign   Marketing   +part +time +vacancies +marketing             Broad   Part Time;Vacancies
627  SEM_Campaign   Marketing       part time full time marketing             Exact   Part Time;Full Time
628  SEM_Campaign   Marketing       part time full time marketing            Phrase   Part Time;Full Time
629  SEM_Campaign   Marketing  +part +time +full +time +marketing             Broad   Part Time;Full Time
[630 rows x 5 columns]

And we're done!

Check the `kw_generate` function for more options and details.

"""
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
