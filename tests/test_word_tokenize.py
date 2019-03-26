from advertools.word_tokenize import word_tokenize


def test_word_tokenize_splits_by_correct_number():
    s = ['this is a text to split by different lengths']
    for i in range(1, 4):
        result = word_tokenize(s, i)
        assert {word.count(' ') for word in result[0]}.pop() == i - 1
