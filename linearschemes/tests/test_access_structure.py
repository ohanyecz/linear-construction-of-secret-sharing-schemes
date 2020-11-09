import pytest

from ..access_structure import AccessStructure


def test_construct_bad_access_structure():
    with pytest.raises(ValueError) as exc:
        AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]],
                        delta_max=[[1, 2], [1, 3], [1, 4], [2, 4]])
    assert "is in both sets" in exc.value.args[0]


def test_from_string():
    ac1 = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    ac2 = AccessStructure.from_string(4, "12", "34", "23")
    ac3 = AccessStructure.from_string(4, "34", "12", "23")
    assert ac2 == ac1
    assert ac3 == ac1


def test_is_complete():
    ac1 = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    ac2 = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]], delta_max=[[1, 3], [1, 4]])
    assert ac1.is_complete()
    assert not ac2.is_complete()


def test_is_trivial():
    ac = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    assert not ac.is_trivial()


def test_dual():
    ac = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    ac2 = AccessStructure(4, gamma_min=[[1, 3], [2, 3], [2, 4]])
    ac_dual = ac.dual()
    ac_dual_dual = ac_dual.dual()
    assert ac_dual == ac2
    assert ac_dual_dual == ac


def test_access_structure_equality():
    ac = AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    ac_f = AccessStructure(4, gamma=[[1, 2], [2, 3], [3, 4], [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]],
                           delta=[[1, 3], [1, 4], [2, 4], [1], [2], [3], [4], []])
    ac2 = AccessStructure(4, gamma_min=[[2, 3], [3, 4]])
    assert ac == ac_f
    assert ac != ac2
    assert ac != 4
