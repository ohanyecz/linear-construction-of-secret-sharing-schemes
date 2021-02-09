import pytest

from access_structure import AccessStructure


@pytest.fixture
def min_set():
    return {'1': {1, 2}, '2': {3, 4}, '3': {2, 3}}


@pytest.fixture
def max_set():
    return {'1': {1, 4}, '2': {2, 4}, '3': {1, 3}}


def test_construct_bad_access_structure(min_set):
    bad_max_set = {'1': {1, 2}, '2': {1, 3}, '3': {1, 4}, '4': {2, 4}}
    with pytest.raises(ValueError) as exc_info:
        AccessStructure(set(range(4)), gamma_min=min_set, delta_max=bad_max_set)
    assert exc_info.type is ValueError
    assert 'is not empty' in exc_info.value.args[0]

    with pytest.raises(ValueError) as exc_info:
        AccessStructure(set(range(1, 5)), gamma_min=min_set, delta_max=min_set)
    assert exc_info.type is ValueError
    assert 'are the same sets' in exc_info.value.args[0]


def test_construct_access_structure(min_set, max_set):
    ac = AccessStructure(set(range(1, 5)), gamma_min=min_set)
    assert ac.participants == set(range(1, 5))
    assert ac.gamma_min == min_set
    assert ac.delta_max == max_set


def test_from_string(min_set):
    ac = AccessStructure(4, gamma_min=min_set)
    ac1 = AccessStructure.from_string(4, '12', '34', '23')
    assert ac1.gamma_min == min_set
    assert ac == ac1


def test_is_complete(min_set):
    ac = AccessStructure(4, gamma_min=min_set)
    assert ac.is_complete()
    ac2 = AccessStructure(4, gamma_min={'1': {1, 2}, '2': {3, 4}, '3': {2, 3}},
                          delta_max={'1': {1, 3}, '2': {1, 4}})
    assert not ac2.is_complete()


def test_is_trivial(min_set):
    ac = AccessStructure(4, gamma_min=min_set)
    assert not ac.is_trivial()
    ac2 = AccessStructure(4)
    assert ac2.is_trivial()


def test_dual(min_set):
    ac = AccessStructure(4, gamma_min=min_set)
    ac_dual = ac.dual()
    dual_gamma_min = {'1': {1, 3}, '2': {2, 4}, '3': {2, 3}}
    assert all(i in dual_gamma_min.values() for i in ac_dual.gamma_min.values())
    ac_dual_dual = ac_dual.dual()
    assert all(i in ac.gamma_min.values() for i in ac_dual_dual.gamma_min.values())


def test_access_structure_equality(min_set, max_set):
    ac1 = AccessStructure(4, gamma_min=min_set)
    ac2 = AccessStructure(4, gamma_min=max_set)
    ac3 = AccessStructure(4, gamma_min={'1': {3, 4}, '2': {2, 3}, '3': {1, 2}})
    assert ac1 == ac1
    assert not ac1 == ac2
    assert not ac2 == ac1
    assert ac1 == ac3
    assert ac3 == ac1
    assert not ac1 == 'Hello'


def test_access_structure_inequality(min_set, max_set):
    ac1 = AccessStructure(4, gamma_min=min_set)
    ac2 = AccessStructure(4, gamma_min=max_set)
    ac3 = AccessStructure(4, gamma_min={'1': {3, 4}, '2': {2, 3}, '3': {1, 2}})
    assert not ac1 != ac1
    assert ac1 != ac2
    assert ac2 != ac1
    assert not ac1 != ac3
    assert not ac3 != ac1
    assert ac1 != 'Hello'
