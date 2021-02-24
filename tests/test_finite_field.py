import pytest

from finite_field import *


def test_construct_bad_field():
    with pytest.raises(ValueError) as exc_info:
        FiniteField(4)
    assert exc_info.type is ValueError
    assert 'should be prime' in exc_info.value.args[0]


def test_construct_field():
    f = FiniteField(5)
    assert f.q == 5
    assert list(f.elements) == list(range(5))
    f2 = FiniteField(2, 4)
    assert f2.q == 16
    assert list(f2.elements) == list(range(16))


def test_construct_field2():
    f = FiniteField2()
    assert f.q == 2
    assert list(f.elements) == [0, 1]


@pytest.mark.parametrize('a, b, expected_result', [
    (0, 1, 1),
    (255, 1, 0),
])
def test_add_elements_field_256(a, b, expected_result):
    f_256 = FiniteField(2, 8)
    assert f_256.add(a, b) == expected_result


@pytest.mark.parametrize('a, b, expected_result', [
    (0, 0, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 0),
])
def test_add_elements_field_2(a, b, expected_result):
    f_2 = FiniteField2()
    assert f_2.add(a, b) == expected_result


@pytest.mark.parametrize('a, b, expected_result', [
    (0, 1, 255),
    (1, 0, 1),
    (255, 10, 245),
])
def test_subtract_elements_field_256(a, b, expected_result):
    f_256 = FiniteField(2, 8)
    assert f_256.subtract(a, b) == expected_result


@pytest.mark.parametrize('a, b, expected_result', [
    (0, 0, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 0),
])
def test_subtract_elements_field_2(a, b, expected_result):
    f_2 = FiniteField2()
    assert f_2.subtract(a, b) == expected_result


@pytest.mark.parametrize('a, b, expected_result', [
    (128, 2, 0),
    (128, 4, 0),
    (10, 2, 20),
    (0, 1, 0),
    (1, 1, 1)
])
def test_multiply_field_256(a, b, expected_result):
    f_256 = FiniteField(2, 8)
    assert f_256.multiply(a, b) == expected_result


@pytest.mark.parametrize('a, b, expected_result', [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1)
])
def test_multiply_field_2(a, b, expected_result):
    f_2 = FiniteField2()
    assert f_2.multiply(a, b) == expected_result


def test_bad_values():
    f_256 = FiniteField(2, 8)
    with pytest.raises(ValueError) as exc_info:
        f_256.add(312, 2)
    assert exc_info.type is ValueError
    assert 'is not in the field' in exc_info.value.args[0]

    with pytest.raises(ValueError) as exc_info:
        f_256.add(2, 312)
    assert exc_info.type is ValueError
    assert 'is not in the field' in exc_info.value.args[0]


def test_finite_field_equality():
    f_256 = FiniteField(2, 8)
    f_2 = FiniteField2()
    assert f_256 == f_256
    assert not f_256 == f_2
    assert not f_2 == f_256
    assert not f_256 == 'Hello'
    assert not 'Hello' == f_256


def test_finite_field_unequality():
    f_256 = FiniteField(2, 8)
    f_2 = FiniteField2()
    assert not f_256 != f_256
    assert f_256 != f_2
    assert f_2 != f_256
    assert f_256 != 'Hello'
    assert 'Hello' != f_256
