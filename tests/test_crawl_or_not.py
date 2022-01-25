from advertools.spider import _crawl_or_not

url = 'https://example.com'


def test_no_conditions():
    result1 = _crawl_or_not(url)
    result2 = _crawl_or_not(url + '?one=1')
    result3 = _crawl_or_not(url + '/one/two/three')
    result4 = _crawl_or_not(url + '/one/two?hello=yes&1=2')
    assert all([result1, result2, result3, result4])


def test_exclude_url_params_true():
    result = _crawl_or_not(url + '?1=1', exclude_url_params=True)
    assert not result


def test_reject_right_param():
    result = _crawl_or_not(url + '?one=1', exclude_url_params=['one', 'two'])
    assert not result


def test_dont_reject_param():
    result = _crawl_or_not(url + '?hello=1', exclude_url_params=['one', 'two'])
    assert result


def test_include_right_param():
    result1 = _crawl_or_not(url + '?one=1&two=2', include_url_params=['one'])
    result2 = _crawl_or_not(url + '?one=1&two=2',
                            include_url_params=['one', 'two'])
    assert result1 and result2


def test_include_and_exclude():
    result = _crawl_or_not(url + '?one=1&two=2&three=3',
                           exclude_url_params=['hello'],
                           include_url_params=['one', 'four'])
    assert result


def test_exclude_simple_regex():
    result = _crawl_or_not(url, exclude_url_regex='example')
    assert not result


def test_exclude_regex():
    result = _crawl_or_not(url, exclude_url_regex='https:.*ple')
    assert not result


def test_include_simple_regex():
    result = _crawl_or_not(url, include_url_regex='example')
    assert result


def test_include_regex():
    result = _crawl_or_not(url, include_url_regex='https:.*ple')
    assert result

def test_multi_condition():
    result = _crawl_or_not(url, exclude_url_params=True,
                           include_url_regex='example')
    assert result
