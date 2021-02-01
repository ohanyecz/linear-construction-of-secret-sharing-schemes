from typing import Iterable, List, Set

from mytypes import Vector

__all__ = ['powerset', 'flatten']


def powerset(iterable: Iterable) -> Set[frozenset]:
    """Calculate the powerset of `iterable."""
    s = list(iterable)
    n = len(s)
    res = set()

    for i in range(2 ** n):
        t = set()
        for j in range(n):
            if i & (1 << j):
                t.add(s[j])
        res.add(frozenset(t))
    return res


def flatten(v: Vector) -> List[int]:
    """
    Return a copy of the vector `v` collapsed into one dimension.

    Parameters
    ----------
    v: Vector
        The input array to flatten.

    Returns
    -------
    y: list
        A copy of the input array, flattened.

    Examples
    --------
    >>> v = [[1, 0], [1, 0, 0], [0, 0, 0], [0, 0]]
    >>> flatten(v)
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]

    """
    y = []
    for i in v:
        y += i
    return y
