from advertools.word_tokenize import word_tokenize


def test_word_tokenize_splits_by_correct_number():
    s = ['this is a text to split by different lengths']
    for i in range(1, 4):
        result = word_tokenize(s, i)
        assert {word.count(' ') for word in result[0]}.pop() == i - 1


def test_word_tokenize_converts_str_to_list():
    s = 'this is a normal string'
    result = word_tokenize(s)
    assert isinstance(result, list)
