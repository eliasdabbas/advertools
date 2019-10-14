from advertools.emoji import emoji_search


def test_emoji_search_returns_correct_columns():
    result = emoji_search('dog')
    assert all(result.columns == ['codepoint', 'status', 'emoji',
                                  'name', 'group', 'sub_group'])


def test_emoji_search_correctly_finds_cat():
    result = emoji_search('cat')
    assert (result
            .select_dtypes('object')
            .apply(lambda s: s.str.contains('cat'))
            .apply(lambda row: any(row), axis='columns')
            .all())
