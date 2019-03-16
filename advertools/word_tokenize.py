import re


def word_tokenize(s, token_word_len=2, lower_case=True, keep_punctuation=False,
                  regex=r'\w+'):
    """Split text ``s`` into word tokens of length ``token_word_len`` each.

    :param s: Any string of text.
    :param token_word_len: Length of word tokens, defaults to 2.
    :param lower_case: Whether or not to return the result in lower case.
    :param keep_punctuation: Whether or not to keep punctuation in the result.
    :param regex: The regex used to extract words, change if you really
        need a different way of splitting.
    :returns tokenized: List of word tokens of length ``token_word_len`` each.

    >>> s = 'Please split into words of length 1, 2, & 3. Thanks!'

    >>> word_tokenize(s, token_word_len=1, keep_punctuation=False)
    ['please', 'split', 'into', 'words', 'of', 'length',
    '1', '2', '3', 'thanks']

    >>> word_tokenize(s, token_word_len=1, keep_punctuation=True)
    ['please', 'split', 'into', 'words', 'of', 'length',
    '1,', '2,', '&', '3.', 'thanks!']

    >>> word_tokenize(s, token_word_len=2, keep_punctuation=False)
    ['please split', 'split into', 'into words', 'words of',
    'of length', 'length 1', '1 2', '2 3', '3 thanks']

    >>> word_tokenize(s, token_word_len=2, keep_punctuation=True)
    ['please split', 'split into', 'into words', 'words of',
    'of length', 'length 1,', '1, 2,', '2, &', '& 3.', '3. thanks!']

    >>> word_tokenize(s, token_word_len=3, keep_punctuation=False)
    ['please split into', 'split into words', 'into words of',
    'words of length', 'of length 1', 'length 1 2', '1 2 3', '2 3 thanks']

    >>> word_tokenize(s, token_word_len=3, keep_punctuation=True)
    ['please split into', 'split into words', 'into words of',
    'words of length', 'of length 1,', 'length 1, 2,', '1, 2, &',
    '2, & 3.', '& 3. thanks!']
    """
    if keep_punctuation:
        regex = r'\S+'
    regex = re.compile(regex)
    split = [word.lower() if lower_case else word for word in regex.findall(s)]
    return [' '.join(split[i:i+token_word_len])
            for i in range(len(split)-token_word_len+1)]
