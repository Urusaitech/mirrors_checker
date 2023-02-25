#!/usr/bin/env python
from countries import *
import pytest


@pytest.mark.parametrize('a, result', [('si', 16000),
                                       ('am', 42000)])
def test_choose_port_good(a, result):
    assert choose_port(a) == result


def test_port_not_found():
    assert choose_port('oq') == 7000


def test_port_not_str():
    assert choose_port(9) == 7000


def test_get_domain_start():
    assert get_domain() == 'ar'


@pytest.mark.parametrize('attempts, expected_result', [(3, 'az'),
                                                       (3, 'be'),
                                                       (100, 'ke')])
def test_get_domain_started_a_few_times(attempts, expected_result):
    '''
    The tested func changes its start position each time it was called
    :param attempts: int
    :param expected_result: str
    '''
    flag = 0
    actual_result = ''
    while flag <= attempts:
        flag += 1
        actual_result = get_domain()
    assert actual_result == expected_result

