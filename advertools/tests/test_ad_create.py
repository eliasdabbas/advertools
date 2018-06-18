import unittest
import sys
sys.path.insert(1, '/advertools/')
import advertools.ad_create import ad_create


class AdCreateTests(unittest.TestCase):
    
    def test_raises_error_for_long_input_strings(self):
        with self.assertRaises(ValueError):
            ad_create('short template {}', ['one', 'two', 'three'], 'very long fallback string', 20)
        with self.assertRaises(ValueError):
            ad_create('very long template string {}', ['one', 'two', 'three'], 'short', 20)
            
    def test_all_replacements_used(self):
        replacements = ['one', 'two', 'three']
        result = ad_create('Hello {}', replacements, 'fallback', capitalize=False)
        self.assertTrue(all([rep in ' '.join(result) for rep in replacements]))
    
    def test_fallback_used_if_string_long(self):
        replacements = ['one', 'two', 'three hundrend thousand']
        result = ad_create('Hello {}', replacements, 'fallback', max_len=20, capitalize=False)
        self.assertEqual(result, ['Hello one', 'Hello two', 'Hello fallback'])

    def test_final_string_capitalized_or_not(self):
        capitalized = ad_create('heLLo {}', ['ONE', 'tWo', 'tHree', 'Four'], 'fallback', capitalize=True)
        not_capitalized = ad_create('heLLo {}', ['ONE', 'tWo', 'tHree', 'Four'], 'fallback', capitalize=False)
        self.assertEqual(capitalized, ['Hello One', 'Hello Two', 'Hello Three', 'Hello Four'])
        self.assertEqual(not_capitalized, ['heLLo ONE', 'heLLo tWo', 'heLLo tHree', 'heLLo Four'])


if __name__ == '__main__':
        unittest.main()
