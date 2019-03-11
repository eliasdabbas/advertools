import unittest
from itertools import permutations, combinations

from advertools.kw_generate import *

import pandas as pd


class KeywordTests(unittest.TestCase):

    def test_match_types_are_capitalized(self):
        df = kw_generate(['one', 'two'], ['three', 'four'],
                         match_types=['eXact', 'PHRase', 'BRoad'])
        self.assertEqual(set(df['Criterion Type']),
                         {'Exact', 'Phrase', 'Broad'})

    def test_raises_error_for_wrong_match_types(self):
        with self.assertRaises(ValueError):
            kw_generate(['one', 'two'], ['three', 'four'],
                        match_types=['hello', 'world'])

    def test_raises_error_for_wrong_max_len(self):
        with self.assertRaises(ValueError):
            kw_generate(['one', 'two'], ['three', 'four'], max_len=1)

    def test_right_combinatorics_fuction_selected(self):
        df_perm = kw_generate(['one', 'two'], ['three', 'four'],
                              order_matters=True)
        self.assertTrue({'one three', 'three one'}
                        .issubset(set(df_perm['Keyword'])))
        df_comb = kw_generate(['one', 'two'], ['three', 'four'],
                              order_matters=False)
        self.assertFalse({'one three', 'three one'}
                         .issubset(set(df_comb['Keyword'])))

    def test_correct_column_names_used(self):
        headers = ['Campaign', 'Ad Group', 'Keyword',
                   'Criterion Type', 'Labels']
        df = kw_generate(['one', 'two'], ['three', 'four'])
        self.assertEqual(list(df.columns.values), headers)

    def test_all_products_in_final_result(self):
        products = {'One', 'Two', 'Three'}
        df = kw_generate(products, ['four', 'five'])
        self.assertEqual(products, set(df['Ad Group']))

    def test_keyword_lengths_vary_between_2_max_len(self):
        df2 = kw_generate(['one', 'two'], ['three', 'four'], max_len=2)
        self.assertEqual(set(df2['Keyword'].str.count(' ')+1), {2})
        df3 = kw_generate(['one', 'two'], ['three', 'four'], max_len=3)
        self.assertEqual(set(df3['Keyword'].str.count(' ')+1), {2, 3})
        df4 = kw_generate(['one', 'two'], ['three', 'four', 'five'], max_len=4)
        self.assertEqual(set(df4['Keyword'].str.count(' ')+1), {2, 3, 4})

    def test_correct_combinations_are_generated(self):
        products = ['one', 'two']
        words = ['three', 'four']
        test_combs = []
        for i in range(2, 4):
            for prod in products:
                for comb in combinations([prod] + words, i):
                    if prod not in comb:
                        continue
                    test_combs.append(' '.join(comb))

        df = kw_generate(products, words, match_types=['Exact'],
                         order_matters=False)
        self.assertEqual(set(test_combs), set(df['Keyword']))

    def test_correct_permutations_are_generated(self):
        products = ['one', 'two']
        words = ['three', 'four']
        test_combs = []
        for i in range(2, 4):
            for prod in products:
                for perm in permutations([prod] + words, i):
                    if prod not in perm:
                        continue
                    test_combs.append(' '.join(perm))

        df = kw_generate(products, words, match_types=['Exact'],
                         order_matters=True)
        self.assertEqual(set(test_combs), set(df['Keyword']))

    def test_correct_campaign_name(self):
        df = kw_generate(['one', 'two'], ['three'], campaign_name='My_campaign')
        self.assertEqual(df['Campaign'][0], 'My_campaign')
        self.assertTrue(len(set(df['Campaign'])) == 1)

    def test_ad_group_names_capitalized(self):
        df = kw_generate(['oNe', 'TWO', 'THree', 'four', 'fivE'], ['six'])
        self.assertEqual(set(['One', 'Two', 'Three', 'Four', 'Five']),
                         set(df['Ad Group']))

    def test_modified_adds_plus_sign_as_many_as_spaces(self):
        df = kw_generate(['one', 'two'], ['three'], match_types=['Modified'])
        self.assertTrue(all(df['Keyword'].str.count(r'\+')
                            == df['Keyword'].str.count(' ')+1))
        self.assertTrue(set(df['Criterion Type']) == {'Broad'})

    def test_all_match_types_used(self):
        df_exact = kw_generate(['one'], ['two'], match_types=['Exact'])
        df_phrase = kw_generate(['one'], ['two'], match_types=['Phrase'])
        df_broad = kw_generate(['one'], ['two'], match_types=['Broad'])
        df_e_p_b = kw_generate(['one'], ['two'],
                               match_types=['Exact', 'Phrase', 'Broad',
                                            'Modified'])
        self.assertEqual(set(df_exact['Criterion Type']), {'Exact'})
        self.assertEqual(set(df_phrase['Criterion Type']), {'Phrase'})
        self.assertEqual(set(df_broad['Criterion Type']), {'Broad'})
        self.assertEqual(set(df_e_p_b['Criterion Type']),
                         {'Exact', 'Phrase', 'Broad'})

    def test_returns_pd_dataframe(self):
        df = kw_generate(['one'], ['two'], order_matters=True)
        self.assertEqual(type(df), pd.core.frame.DataFrame)
        self.assertEqual(df.shape, (6, 5))


words = ['[one]', '"two"', '+three -four', '[five', 'six"',
         '+seven eight nine]']


def test_kw_broad():
    result = kw_broad(words)
    assert result == ['one', 'two', 'three -four', 'five', 'six',
                      'seven eight nine']


def test_kw_exact():
    result = kw_exact(words)
    assert result == ['[one]', '[two]', '[three -four]', '[five]', '[six]',
                      '[seven eight nine]']


def test_exact_contains_brackets():
    result = kw_exact(words)
    assert ['[' in x and ']' in x for x in result]


def test_kw_phrase():
    result = kw_phrase(words)
    assert result == ['"one"', '"two"', '"three -four"', '"five"', '"six"',
                      '"seven eight nine"']


def test_kw_modified():
    result = kw_modified(words)
    assert result == ['+one', '+two', '+three +-four', '+five', '+six',
                      '+seven +eight +nine']


def test_kw_neg_broad():
    result = kw_neg_broad(words)
    assert result == ['-one', '-two', '-three -four', '-five', '-six',
                      '-seven eight nine']


def test_kw_neg_exact():
    result = kw_neg_exact(words)
    assert result == ['-[one]', '-[two]', '-[three -four]', '-[five]', '-[six]',
                      '-[seven eight nine]']


def test_kw_neg_phrase():
    result = kw_neg_phrase(words)
    assert result == ['-"one"', '-"two"', '-"three -four"', '-"five"', '-"six"',
                      '-"seven eight nine"']


if __name__ == '__main__':
        unittest.main()
