from advertools.word_tokenize import word_tokenize


def test_word_tokenize_splits_by_correct_number():
    s = 'this is a text to split be different lengths'
    for i in range(1, 4):
        result = word_tokenize(s, i)
        assert {word.count(' ') for word in result}.pop() == i - 1


def test_word_tokenize_provides_correct_case():
    s = 'Split tHIs with DiFFerent cases'
    result_lower = word_tokenize(s, lower_case=True)
    assert all(word.islower() for word in result_lower)

    result_upper = word_tokenize(s, lower_case=False)
    assert result_upper == ['Split tHIs', 'tHIs with',
                            'with DiFFerent', 'DiFFerent cases']


def test_word_tokenize_keeps_punctuation_correctly():
    s = 'Some, text with: some ** ) punctuation !!'
    result_no_punc = word_tokenize(s, keep_punctuation=False)
    assert result_no_punc == ['some text', 'text with', 'with some',
                              'some punctuation']

    result_no_punc = word_tokenize(s, keep_punctuation=True)
    assert result_no_punc == ['some, text', 'text with:', 'with: some',
                              'some **', '** )', ') punctuation',
                              'punctuation !!']
