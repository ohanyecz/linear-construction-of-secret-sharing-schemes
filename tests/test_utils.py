import pytest

from utils import *


def test_powerset():
    assert list(powerset(range(2, 1))) == [set()]
    assert list(powerset(range(2))) == [set(), {0}, {1}, {0, 1}]
    assert list(powerset([0, 1])) == [set(), {0}, {1}, {0, 1}]
    assert list(powerset(range(1, 3))) == [set(), {1}, {2}, {1, 2}]


def test_flatten():
    v1 = [[1, 0], [0, 0, 0]]
    assert flatten(v1) == [1, 0, 0, 0, 0]


@pytest.mark.parametrize('primes', [2, 3, 5, 271, 1951])
def test_is_prime(primes):
    assert is_prime(primes)


@pytest.mark.parametrize('not_primes', [-1, 1, 4, 1953])
def test_is_not_prime(not_primes):
    assert not is_prime(not_primes)
