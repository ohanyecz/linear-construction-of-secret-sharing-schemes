import pytest

from ..code_description import *


def test_p_support():
    c = [[0, 0], [1, 0, 0], [0, 1, 0], [0, 0]]
    assert p_support(c) == {2, 3}


def test_projection():
    c = [[0, 0], [1, 0, 0], [0, 1, 0], [0, 0]]
    assert projection(c, {3, 2}) == [[1, 0, 0], [0, 1, 0]]
    assert projection(c, [4, 1]) == [[0, 0], [0, 0]]
    assert projection(c, [3, 2, 1, 4]) == [[0, 0], [1, 0, 0], [0, 1, 0], [0, 0]]
    assert projection(c, {2, 4, 1, 3}) == [[0, 0], [1, 0, 0], [0, 1, 0], [0, 0]]
    assert projection(c, range(1, 5)) == [[0, 0], [1, 0, 0], [0, 1, 0], [0, 0]]


def test_epsilon():
    assert epsilon(-2, 1) == []
    assert epsilon(1, -2) == []
    assert epsilon(3, 2) == [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2)]
