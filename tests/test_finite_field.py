from finite_field import *


def test_construct_field():
    f = FiniteField(5)
    assert f.q == 5
    f2 = FiniteField(2, 4)
    assert f2.q == 16


def test_construct_field2():
    f = FiniteField2()
    assert f.q == 2
    assert list(f.elements) == [0, 1]
