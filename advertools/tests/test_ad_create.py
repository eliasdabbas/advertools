import unittest

from advertools import ad_create


class AdCreateTests(unittest.TestCase):
    
    def test_raises_error_for_long_input_strings(self):
        with self.assertRaises(ValueError):
            ad_create('short template {}', ['one', 'two', 'three'], 'very long fallback string', 20)
        with self.assertRaises(ValueError):
            ad_create('very long template string {}', ['one', 'two', 'three'], 'short', 20)
            
    def test_all_replacements_used(self):
        replacements = ['one', 'two', 'three']
        result = ad_create('Hello {}', replacements, 'fallback')
        self.assertTrue(all([rep in ' '.join(result) for rep in replacements]))
    
    def test_fallback_used_if_string_long(self):
        replacements = ['one', 'two', 'three hundrend thousand']
        result = ad_create('Hello {}', replacements, 'fallback', max_len=20)
        self.assertEqual(result, ['Hello one', 'Hello two', 'Hello fallback'])

    
#     def test_match_types_are_capitalized(self):
#         df = kw_generate(['one', 'two'], ['three', 'four'], match_types=['eXact', 'PHRase', 'BRoad'])
#         self.assertEqual(set(df['Criterion Type']), {'Exact', 'Phrase', 'Broad'})


if __name__ == '__main__':
        unittest.main()