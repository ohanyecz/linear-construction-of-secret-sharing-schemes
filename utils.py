from typing import Iterable, Set

__all__ = ['powerset']


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
