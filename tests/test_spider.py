import random
from collections import Counter

import pytest
from advertools.spider import (_numbered_duplicates, _json_to_dict,
                               _split_long_urllist, crawl)

jsonobj = {
    '@context': 'http://schema.org',
    '@type': 'NewsMediaOrganization',
    'name': 'The New York Times',
    'logo': {'@context': 'http://schema.org',
             '@type': 'ImageObject',
             'url': 'https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png',
             'height': 40,
             'width': 250},
    'url': 'https://www.nytimes.com/',
    '@id': 'https://www.nytimes.com/#publisher',
    'diversityPolicy': 'https://www.nytco.com/diversity-and-inclusion-at-the-new-york-times/',
    'ethicsPolicy': 'https://www.nytco.com/who-we-are/culture/standards-and-ethics/',
    'masthead': 'https://www.nytimes.com/interactive/2019/admin/the-new-york-times-masthead.html',
    'foundingDate': '1851-09-18',
    'sameAs': 'https://en.wikipedia.org/wiki/The_New_York_Times'
}

def test_numbered_duplicates_returns_same_num_of_items():
    l1 = ['jan', 'feb', 'jan', 'jan', 'feb', 'mar', 'apr']
    l2 = ['one', 'one', 'one']
    l3 = ['one', 'two', 'three', 'three', 'three', 'two']
    for lst in [l1, l2, l3]:
        result = _numbered_duplicates(lst)
        assert len(result) == len(lst)


def test_numbered_duplicates_returns_correct_items():
    numbers = ['one', 'two', 'three', 'four']
    for i in range(1000):
        sample = random.choices(numbers, k=7)
        result = _numbered_duplicates(sample)
        result_split = [num.rsplit('_', 1)[0] for num in result]
        assert Counter(sample) == Counter(result_split)


def test_json_to_dict_returns_dict():
    result = _json_to_dict(jsonobj)
    assert isinstance(result, dict)
    assert all('jsonld_' in key for key in result)


def test_json_to_dict_contains_number():
    for i in range(1, 6):
        result = _json_to_dict(jsonobj, i)
        to_test = 'jsonld_' + str(i) + '_'
        assert isinstance(result, dict)
        assert all(to_test in key for key in result)


def test_crawl_raises_on_wrong_file_extension():
    with pytest.raises(ValueError):
        crawl('https://example.com', 'myfile.wrong',
              allowed_domains='example.com')


def test_split_long_urllist_correct_lengths():
    testlist = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
    result = _split_long_urllist(testlist, max_len=15)
    assert sum(len(x) for x in result) == len(testlist)
    assert all(len(x) < 15 for x in result)
