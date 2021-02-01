from itertools import product
from typing import Dict, List, Set, Tuple, Union


__all__ = ["p_support", "projection", "epsilon", "labels", "g_property"]


def p_support(c: List[List[int]]) -> Set[int]:
    """Calculate p-support of a code vector `c`."""
    return {i + 1 for i, cw in enumerate(c) if any(cw)}


def projection(c: List[List[int]], x: Union[Set[int], List[int], range]) -> List[List[int]]:
    return [c[i-1] for i in sorted(x)]


def epsilon(r: int, k: int) -> List[Tuple[int, int]]:
    return [(i, j) for j in range(1, k+1) for i in range(1, r+1)]


def labels(field, length):
    """A generator function which generates an edge label from elements of `field` of given `length`."""
    for i in product(field, repeat=length):
        yield list(i)


def g_property(gamma_min: Dict[str, set], c_vectors: Dict[str, list]) -> bool:
    """
    Check if the g-property holds for the minimal sets in Gamma.

    Parameters
    ----------
    gamma_min: dict
        A minimal sets in Gamma.
    c_vectors: dict
        A dictionary where each key unambiguously identify a code vector :math:`c^{i,j}`.

    Returns
    -------
    res: bool
        True if the g-property holds for the given minimal sets and a set of vectors; False otherwise.

    See Also
    --------
    code_description : for definitions
    epsilon : The definition of :math:`\varepsilon`.

    Notes
    -----
    This function implements the first part of Definition 3.2.

    Examples
    --------
    Let the minimal sets be
    >>> g_min = {'1': {1, 2}, '2': {3, 4}, '3': {2, 3}}
    so r = 3. Let q = 2 and the set of vectors be
    >>> vec = {'11': [[1, 0], [1, 0, 0], [0, 0, 0], [0, 0]],
    ...        '21': [[0, 0], [0, 0, 0], [1, 0, 0], [1, 0]],
    ...        '31': [[0, 0], [1, 0, 0], [0, 0, 1], [0, 0]],
    ...        '12': [[0, 1], [0, 1, 0], [0, 0, 0], [0, 0]],
    ...        '22': [[0, 0], [0, 0, 0], [0, 1, 0], [0, 1]],
    ...        '32': [[0, 0], [0, 0, 1], [0, 1, 0], [0, 0]]}
    >>> g_property(g_min, vec)
    True

    """
    return all(p_support(c_ij) <= gamma_min[i[0]] for i, c_ij in c_vectors.items())