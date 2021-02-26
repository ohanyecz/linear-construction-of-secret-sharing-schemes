from itertools import product
from typing import Callable, Dict, Iterable, Iterator, List, Set, Union

from finite_field import FiniteField
from mytypes import Epsilon, Vector


__all__ = ["p_support", "projection", "epsilon", "generate_vector_cond", "generate_vector", "g_property"]


def p_support(c: Vector) -> Set[int]:
    """Calculate p-support of a code vector."""
    return {i for i, cw in enumerate(c, start=1) if any(cw)}


def projection(c: Vector, x: Union[Iterable[int], range]) -> Vector:
    """The projection of a vector """
    return [c[i-1] for i in sorted(x)]


def epsilon(r: int, k: int) -> Epsilon:
    return [(i, j) for j in range(1, k+1) for i in range(1, r+1)]


def generate_vector_cond(field: 'FiniteField', *, shares: List[int], cond: Callable[[Vector], bool]) -> Iterator[list]:
    """
    Generate a code vector where `cond` holds.

    Parameters
    ----------
    field: FiniteField
        The field from which the labels are generated.
    shares: list
        The share size of the participants.
    cond: callable
        The condition which the vector must satisfy. In most cases, `cond` checks the p-support of a code vector.


    Returns
    -------
    res: Iterator


    Examples
    --------
    Generate all possible edge label for which the p-support is in the set {2, 3} (only the first few result is shown):


    >>> from code_description import generate_vector_cond
    >>> from finite_field import FiniteField2
    >>> field = FiniteField2()
    >>> cond = lambda x: p_support(x) <= {2, 3}
    >>> shares = [2, 3, 3, 2]
    >>> for label in generate_vector_cond(field, shares=shares, cond=cond):
    ...    print(label)
    ...
    [[0, 0], [0, 0, 0], [0, 0, 0], [0, 0]]
    [[0, 0], [0, 0, 0], [0, 0, 1], [0, 0]]
    [[0, 0], [0, 0, 0], [0, 1, 0], [0, 0]]
    [[0, 0], [0, 0, 0], [0, 1, 1], [0, 0]]
    [[0, 0], [0, 0, 0], [1, 0, 0], [0, 0]]
    [[0, 0], [0, 0, 0], [1, 0, 1], [0, 0]]
    [[0, 0], [0, 0, 0], [1, 1, 0], [0, 0]]

    """
    for i in generate_vector(field, shares=shares):
        if cond(i):
            yield i


def generate_vector(field: FiniteField, *, shares: List[int]) -> Iterator[list]:
    """
    Generate all possible code vectors in `field`.


    Parameters
    ----------
    field: FiniteField
        The field from which the labels are generated.
    shares: list
        The share size of the participants.


    Returns
    -------
    res: Iterator

    """
    for i in product(field.elements, repeat=sum(shares)):
        j, res = 0, []
        for s in shares:
            res.append(list(i)[j:(j+s)])
            j += s
        yield res


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
