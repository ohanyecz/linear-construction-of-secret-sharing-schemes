import pytest

from utils import powerset, flatten


def test_powerset():
    assert list(powerset(range(2, 1))) == [set()]
    assert list(powerset(range(2))) == [set(), {0}, {1}, {0, 1}]
    assert list(powerset([0, 1])) == [set(), {0}, {1}, {0, 1}]
    assert list(powerset(range(1, 3))) == [set(), {1}, {2}, {1, 2}]


def test_flatten():
    v1 = [[1, 0], [0, 0, 0]]
    assert flatten(v1) == [1, 0, 0, 0, 0]
