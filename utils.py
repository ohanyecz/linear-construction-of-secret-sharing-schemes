from math import sqrt
from typing import Iterable, Iterator, List, Set

from mytypes import Vector


def powerset(iterable: Iterable) -> Iterator[Set[int]]:
    """
    Generates the powerset of elements of `iterable`.

    Examples
    --------
    >>> list(powerset(range(2)))
    [set(), {0}, {1}, {0, 1}]
    >>> for i in powerset(range(2)):
    ...     print(i)
    ...
    set()
    {0}
    {1}
    {0, 1}

    """
    s = list(iterable)
    n = len(s)

    for i in range(2 ** n):
        t = set()
        for j in range(n):
            if i & (1 << j):
                t.add(s[j])
        yield t


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


def is_prime(n: int) -> bool:
    """Check if `n` is prime."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(sqrt(n))+1, 2):
        if n % i == 0:
            return False

    return True
