import re


def word_tokenize(s, word_token_len=2, lower_case=True, keep_punctuation=False,
                  regex=r'\w+'):
    """Split text ``s`` into word tokens of length ``word_token_len`` each.

    :param s: Any string of text.
    :param word_token_len: Length of word tokens, defaults to 2.
    :param lower_case: Whether or not to return the result in lower case.
    :param keep_punctuation: Whether or not to keep punctuation in the result.
    :param regex: The regex used to extract words, change if you really
        need a different way of splitting.
    :return: List of word tokens of length ``word_token_len`` each.

    s = 'Please split into words of length 1, 2, & 3. Thanks!'

    >>> word_tokenize(s, word_token_len=1, keep_punctuation=False)
    ['please', 'split', 'into', 'words', 'of', 'length',
    '1', '2', '3', 'thanks']

    >>> word_tokenize(s, word_token_len=1, keep_punctuation=True)
    ['please', 'split', 'into', 'words', 'of', 'length',
    '1,', '2,', '&', '3.', 'thanks!']

    >>> word_tokenize(s, word_token_len=2, keep_punctuation=False)
    ['please split', 'split into', 'into words', 'words of',
    'of length', 'length 1', '1 2', '2 3', '3 thanks']

    >>> word_tokenize(s, word_token_len=2, keep_punctuation=True)
    ['please split', 'split into', 'into words', 'words of',
    'of length', 'length 1,', '1, 2,', '2, &', '& 3.', '3. thanks!']

    >>> word_tokenize(s, word_token_len=3, keep_punctuation=False)
    ['please split into', 'split into words', 'into words of',
    'words of length', 'of length 1', 'length 1 2', '1 2 3', '2 3 thanks']

    >>> word_tokenize(s, word_token_len=3, keep_punctuation=True)
    ['please split into', 'split into words', 'into words of',
    'words of length', 'of length 1,', 'length 1, 2,', '1, 2, &',
    '2, & 3.', '& 3. thanks!']
    """
    regex = re.compile(regex)
    if keep_punctuation:
        split = [x.lower() for x in s.split()] if lower_case else s.split()
    else:
        split = [word.lower() if lower_case else word
                 for word in regex.findall(s)]
    return [' '.join(split[i:i+word_token_len])
            for i in range(len(split)-word_token_len+1)]
