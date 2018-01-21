import unittest
from urllib.parse import parse_qs

import advertools as adv



class AdTestCase(unittest.TestCase):
    
    def test_correct_split(self):
        s = 'this is a short ad'
        s2 = 'string-separated-by-dashes'
        self.assertEqual(adv.ad_from_string(s), ['this is a short ad','', '', '', '', ''])
        self.assertEqual(adv.ad_from_string(s, slots=[5, 5]), ['this', 'is a', 'short ad'])
        self.assertEqual(adv.ad_from_string(s2, sep='-'), ['string separated by dashes', '', '', '', '', ''])
        self.assertEqual(adv.ad_from_string(s2, sep='-', slots=(8, 10, 3, 7)), ['string', 'separated', 'by', 'dashes', ''])
        
    def test_correct_url(self):
        base_url = 'http://www.site.com'
        source = 'the_source'
        medium = 'The  medium'
        campaign = 'campaign%%'
        term = 'keyword1 keyword 2'
        content = 'banner_728x90'
        self.assertEqual(parse_qs(adv.url_utm_ga(url=base_url,
                                        utm_source=source, 
                                        utm_medium=medium,
                                        utm_campaign=campaign,
                                        utm_term=term,
                                        utm_content=content)),
                        parse_qs('http://www.site.com?utm_term=banner_728x90&utm_content=keyword1+keyword+2&utm_campaign=campaign%25%25&utm_medium=The++medium&utm_source=the_source'))


        

        
if __name__ == '__main__':
        unittest.main()