from advertools.ad_from_string import ad_from_string


def test_len_result_one_more_than_len_slots():
    for i in range(5):
        result = ad_from_string('sample text', slots=[10 for i in range(i)])
        assert len(result) == i + 1


def test_result_same_as_input_text():
    input_text = 'This is sample text to input'
    result = ad_from_string(input_text)
    assert ' '.join(result).strip() == input_text


def test_long_string_gets_skipped():
    result = ad_from_string('This_is_looooooooooooooooooooong')
    assert result[0] == ''


def test_capitalizes_or_not():
    s = 'This text will be split by the Function'
    capitalized = ad_from_string(s, capitalize=True)
    assert capitalized == ['This Text Will Be Split By The',
                           'Function', '', '', '', '', '', '']
    not_capitalized = ad_from_string(s, capitalize=False)
    assert not_capitalized == ['This text will be split by the',
                               'Function', '', '', '', '', '', '']


def test_result_lengths_within_slots():
    s = 'some random text that will be split by different slot lengths'
    for i in range(10):
        slots = [i, i*3, i*5, i*10]
        result = ad_from_string(s, slots=slots)
        for string, slot in zip(result, slots):
            assert len(string) <= slot
