import pytest

from utils import powerset, flatten


def test_powerset():
    assert powerset(range(2, 1)) == {frozenset([])}
    assert powerset(range(1, 3)) == {frozenset([]), frozenset([1]), frozenset([2]), frozenset([1, 2])}
    assert powerset([1, 2, 3]) == {frozenset([]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([1, 2]),
                                   frozenset([1, 3]), frozenset([2, 3]), frozenset([1, 2, 3])}


def test_flatten():
    v1 = [[1, 0], [0, 0, 0]]
    assert flatten(v1) == [1, 0, 0, 0, 0]
