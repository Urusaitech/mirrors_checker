#!/usr/bin/env python
from proxy_connect import *
import pytest


def test_get_url_start():
    assert get_mirror() == mirrors[0]


@pytest.mark.parametrize('tries, result', [(210, mirrors[3]),
                                           (220, mirrors[4]),
                                           (900, 'stop')])
def test_get_url_loop(tries, result):
    '''
    Pytest starts next test with the previous test's results
    '''
    x = 0
    try:
        while x < tries:
            x += 1
            get_mirror()
        cur_result = get_mirror()
        assert cur_result == result
    except IndexError as e:
        pytest.skip(str(e))
