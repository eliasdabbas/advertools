from advertools import reverse_dns_lookup
from advertools.reverse_dns_lookup import _single_request

ip_list = [
    '62.235.238.71',
    '62.235.238.71',
    '62.235.238.71',
    '62.235.238.71',
    '62.235.238.71',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '81.241.228.69',
    '95.163.255.29',
    '105.140.165.213',
    '2.239.215.165',
    '2.239.215.165',
    '2.239.215.165',
    '66.249.65.161',
    '66.249.65.161',
    '82.173.111.205',
    '139.59.215.212',
    '84.227.57.137',
    '84.227.57.137',
    '86.74.165.98',
    '194.230.155.248',
    '84.227.57.137',
    '84.227.57.137',
    '84.194.174.248',
    '81.164.191.132',
    '194.230.155.248',
    '94.225.83.80',
    '213.118.187.163',
    '213.118.187.163',
    '86.74.165.98',
    '94.225.83.80',
    '213.118.187.163',
    '195.16.13.29',
    '195.16.13.29',
    '94.225.160.96',
    '213.211.144.181',
    '213.211.144.181',
    '213.211.144.181',
    '194.230.155.248',
    '86.74.165.98',
    '178.197.224.207',
    '195.16.13.29',
    '195.16.13.29',
    '83.78.170.225',
    ]

result = reverse_dns_lookup(ip_list, max_workers=5)


def test_reverse_dns_correct_columns():
    column_list = ['ip_address', 'count', 'cum_count', 'perc', 'cum_perc', 
                   'hostname', 'aliaslist', 'ipaddrlist', 'errors']
    assert all(result.columns == column_list)


def test_reverse_dns_monotonic():
    assert result['count'].is_monotonic_decreasing
    assert result['cum_count'].is_monotonic_increasing
    assert result['perc'].is_monotonic_decreasing
    assert result['cum_perc'].is_monotonic_increasing


def test_reverse_dns_single_returns_ip_in_result():
    ip = '62.235.238.71'
    result = _single_request(ip)
    assert ip == result[0]


def test_reverse_dns_single_returns_error():
    ip = '0.0.0.0'
    result = _single_request(ip)
    assert result[-1] == '[Errno 1] Unknown host'
