from .regex import WORD_DELIM


def word_tokenize(text_list, phrase_len=2):
    """Split ``text_list`` into phrases of length ``phrase_len`` words each.

    A "word" is any string between white spaces (or beginning or
    end of string) with delimiters stripped from both sides.
    Delimiters include quotes, question marks, parentheses, etc.
    Any delimiter contained within the string remains. See examples below.

    :param text_list: List of strings.
    :param phrase_len: Length of word tokens, defaults to 2.
    :return tokenized: List of lists, split according to ``token_word_len``.

    >>> t = ['split me into length-n-words',
    ... 'commas, (parentheses) get removed!',
    ... 'commas within text remain $1,000, but not the trailing commas.']

    >>> word_tokenize(t, 1)
    [['split', 'me', 'into', 'length-n-words'],
    ['commas', 'parentheses', 'get', 'removed'],
    ['commas', 'within', 'text', 'remain', '$1,000',
    'but', 'not', 'the', 'trailing', 'commas']]


    The comma inside "$1,000" as well as the dollar sign remain, as they
    are part of the "word", but the trailing comma is stripped.

    >>> word_tokenize(t, 2)
    [['split me', 'me into', 'into length-n-words'],
    ['commas parentheses', 'parentheses get', 'get removed'],
    ['commas within', 'within text', 'text remain', 'remain $1,000',
    '$1,000 but', 'but not', 'not the', 'the trailing', 'trailing commas']]


    >>> word_tokenize(t, 3)
    [['split me into', 'me into length-n-words'],
    ['commas parentheses get', 'parentheses get removed'],
    ['commas within text', 'within text remain', 'text remain $1,000',
    'remain $1,000 but', '$1,000 but not', 'but not the',
    'not the trailing', 'the trailing commas']]
    """
    if isinstance(text_list, str):
        text_list = [text_list]
    split = [text.lower().split() for text in text_list]
    split = [[word.strip(WORD_DELIM) for word in text] for text in split]

    return [[' '.join(s[i:i + phrase_len])
             for i in range(len(s) - phrase_len + 1)] for s in split]
