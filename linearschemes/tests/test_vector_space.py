import pytest

from ..finite_field import *
from ..vector_space import *


@pytest.fixture
def vso2():
    return VectorSpace(FiniteField2())


@pytest.fixture
def vso256():
    return VectorSpace(FiniteField(2, 8))


def test_construct_vector_space(vso256):
    assert vso256.field == FiniteField(2, 8)


@pytest.mark.parametrize('good_data', [
    [0, 4, 8, 12],
    [0, 4, 8, 255]
])
def test_vector_is_in_field(good_data, vso256):
    assert VectorSpace.is_in_field(vso256, good_data)


@pytest.mark.parametrize('bad_data', [
    [0, 4, 8, 256],
    [-3, 4, 8, 12],
])
def test_vector_is_not_in_field(bad_data, vso256):
    assert not VectorSpace.is_in_field(vso256, bad_data)


def test_multiply(vso256):
    v1 = [4, 6, 8, 10]
    v2 = [4, 128, 10, 255]
    v3 = [256, 120, 12, 5]
    assert vso256.multiply(0, v1) == [0, 0, 0, 0]
    assert vso256.multiply(1, v1) == [4, 6, 8, 10]
    assert vso256.multiply(2, v2) == [8, 0, 20, 254]

    with pytest.raises(ValueError) as excinfo:
        vso256.multiply(2, v3)
        assert 'not in the order' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        vso256.multiply(340, v1)
        assert 'not in the field' in str(excinfo.value)


def test_add(vso256):
    v1 = [1, 2, 3, 4]
    v2 = [5, 6, 7, 8]
    v3 = [252, 253, 254, 255]
    v4 = [1, 256, 34, 23]
    assert vso256.add(v1, v2) == [6, 8, 10, 12]
    assert vso256.add(v1, v3) == [253, 255, 1, 3]

    with pytest.raises(ValueError) as excinfo:
        vso256.add(v1, v4)
        assert 'not in the vector space' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        vso256.add(v4, v1)
        assert 'not in the vector space' in str(excinfo.value)


@pytest.mark.skip
def test_choose_vector():
    # how to test randomly generated vectors?
    vs = VectorSpace(FiniteField(2, 8))
    length = 10
    assert len(vs.choose_vector(length)) == 10


def test_equality(vso2, vso256):
    vs = VectorSpace(FiniteField(2, 8))
    assert vso2 == vso2
    assert vso256 == vs
    assert vs == vso256
    assert not vso2 == vso256
    assert not vso256 == vso2
    assert not vso2 == 'Hello'


def test_non_equality(vso2, vso256):
    vs = VectorSpace(FiniteField(2, 8))
    assert not vso2 != vso2
    assert not vso256 != vs
    assert not vs != vso256
    assert vso2 != vso256
    assert vso256 != vso2
    assert vso2 != 'Hello'


def test_string_representation(vso256):
    assert 'of order 256' in str(vso256)
