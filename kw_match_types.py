import pandas as pd

def kw_broad(words):
    pattern = '\]|\[|\+|\-|"'
    return pd.Series(words).str.replace(pattern, '')


def kw_phrase(words):
    words = kw_broad(words)
    words = ['"' + x + '"' for x in words]
    return pd.Series(words)


def kw_exact(words):
    words = kw_broad(words)
    words = ['[' + x + ']' for x in words]
    return pd.Series(words)


def kw_negative_phrase(words):
    return '-' + kw_phrase(words)


def kw_negative_exact(words):
    return '-' + kw_exact(words)


def kw_modified(word):
    word = word.replace(' ', ' +')
    return '+' + word


def kw_modified_broad(words, target=None):
    words = kw_broad(words)
    print(type(words))
    if target:
        assert isinstance(target, list)
        for t in target:
            words = words.str.replace(t, '+' + t)
        return pd.Series(words)
    else:
        words = [kw_modified(x) for x in words]
        return pd.Series(words)


def kw_match(words, match_types):
    s = pd.Series()
    for m in match_types:
        s = s.append(m(words))
    return s


def kw_type(word):
    kw_funcs = [kw_broad, kw_exact, kw_phrase, kw_negative_exact,
                kw_negative_phrase, kw_modified, kw_modified_broad]
    for func in kw_funcs:
        if '+' in word and not word.startswith('+'):
            return 'modified broad with target'
        if func(word)[0] == word:
            return func.__name__[3:].replace('_', ' ')
    return None


class KeywordList(object):
    def __init__(self, words):
        self.keywords = pd.Series(words)
        self.keywords.name = 'Keyword'

    def broad(self):
        return kw_broad(self.keywords)

    def exact(self):
        return kw_exact(self.keywords)

    def phrase(self):
        return kw_phrase(self.keywords)

    def negative_phrase(self):
        return kw_negative_phrase(self.keywords)

    def negative_exact(self):
        return kw_negative_exact(self.keywords)

    def modified_broad(self, target=None):
        return kw_modified_broad(self.keywords, target)

    def export(self, campaign=None, adgroup=None):
        df = pd.DataFrame(self.keywords)
        if adgroup:
            df['Ad Group'] = adgroup
        if campaign:
            df['Campaign'] = campaign
        return df

    def summarize(self):
        kw_types = pd.Series([kw_type(x) for x in self.keywords])
        print('Keyword types:')
        print(kw_types.value_counts())
        lengths = pd.Series([x.count(' ') + 1 for x in self.keywords])
        lengths.index.name = 'Word length'
        print(lengths.value_counts())
