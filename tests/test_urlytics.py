import pandas as pd
from advertools.urlytics import url_to_df

domain = 'http://example.com'
domain_path = 'https://example.com/path'
path_rel = '/path_rel'
path_rel_noslash = 'no_slash_no_nothing'
domain_query = 'https://www.example.com?one=1&two=2'
domain_query_rel = '/?one=1&two=2'
port = 'https://www.example.com:80'
fragment = 'https://example.com/#fragment'
fragment_rel = '/#fragment_rel'
full = 'ftp://example.com:20/cat/sub_cat?one=10&three=30#frag_2'

ordered_q_param_urls = ['https://example.com?a=a&b=b&c=c',
                        'https://example.com?b=b&c=c',
                        'https://example.com?c=c',
                        'https://example.com?a=a&c=c']

def test_urltodf_convert_str_tolist():
    result = url_to_df('https://www.example.com')
    assert isinstance(result, pd.DataFrame)


def test_path_rel_noslash():
    result = url_to_df(path_rel_noslash)
    assert result['scheme'][0] == ''
    assert result['netloc'][0] == ''


def test_abs_and_rel():
    result = url_to_df([domain, path_rel])
    assert 'dir_1' in result
    assert len(result) == 2


def test_domainpath_fragrel_full():
    result = url_to_df([domain_path, fragment_rel, full])
    assert len(result) == 3
    assert 'dir_2' in result
    query_set = {'query_one', 'query_three'}
    assert query_set.intersection(result.columns) == query_set

def test_no_path_has_no_last_dir():
    result = url_to_df(domain_query)
    assert 'last_dir' not in result

def test_all():
    result = url_to_df([domain, domain_path, path_rel, domain_query,
                        domain_query_rel, port, fragment, fragment_rel, full])
    assert len(result) == 9
    assert 'port' in result
    assert 'hostname' in result
    assert 'last_dir' in result

def test_all():
    result = url_to_df([domain, domain_path, path_rel, domain_query,
                        domain_query_rel, port, fragment, fragment_rel, full])

def test_query_params_are_ordered_by_fullness():
    result = url_to_df(ordered_q_param_urls)
    query_df = result.filter(regex='^query_')
    sorted_q_params = (query_df
                       .notna()
                       .mean()
                       .sort_values(ascending=False).index)
    assert (query_df.columns == sorted_q_params).all()
