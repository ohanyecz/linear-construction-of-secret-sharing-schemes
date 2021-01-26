from typing import Callable, Dict, Iterable, List, Optional, Set, ValuesView

from utils import powerset

__all__ = ['AccessStructure']


class AccessStructure:
    """
    Class to hold the access structure on a set of participants.

    An access structure on the set of participants specifies those subsets of the participants
    who are qualified to reconstruct the secret and those subsets of the participants who are
    forbidden to obtain additional knowledge about the secret by pooling their shares.


    Attributes
    ----------
    n : `int`
        The number of the participants
    gamma_min : `list`, optional
        The minimal elements in Gamma
    delta_max : `list`, optional
        The maximal elements in Delta
    gamma: `list`, optional
        The qualified sets Gamma
    delta: `list`, optional
        The unqualified sets Delta


    Notes
    -----
    - It is recommended that either `gamma_min` OR `gamma` *and* `delta` should be passed to the class.
    If no parameter is passed, the behaviour of the class is undefined.

    - If only `gamma_min` is passed, then the class *assumes* that the access structure is complete.
    If this behaviour is not intended, pass the maximal sets `delta_max` as well.

    - You can access the minimal sets in Gamma, maximal sets in Delta, Gamma and Delta itself directly.
    >>> ac.gamma_min
    >>> ac.delta_max
    >>> ac.gamma
    >>> ac.delta


    Examples
    --------
    >>> import linearschemes as ls
    >>> ac = ls.AccessStructure(4, gamma_min=[[1, 2], [3, 4], [2, 3]])
    >>> ac.is_trivial()
    False
    >>> ac2 = ls.AccessStructure(4, gamma=[[1, 2], [2, 3], [3, 4], [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]], delta=[[1, 3], [1, 4], [2, 4], [1], [2], [3], [4], []]))
    >>> ac == ac2
    True
    """
    def __init__(self,
                 n: int,
                 gamma_min: Optional[List[List[int]]] = None,
                 delta_max: Optional[List[List[int]]] = None,
                 gamma: Optional[List[List[int]]] = None,
                 delta: Optional[List[List[int]]] = None) -> None:
        self._n = n
        self._ps = powerset(range(1, n+1))
        if gamma_min or delta_max:
            if gamma_min and delta_max:
                a = set(frozenset(i) for i in gamma_min)
                b = set(frozenset(i) for i in delta_max)
                aib = a & b
                if aib:
                    raise ValueError(f"Element {aib} is in both sets.")

            self._gamma_min = _to_dict(gamma_min)
            self._gamma = self._expand(self._gamma_min.values(), lambda x, y: y <= x)

            if delta_max:
                self._delta_max = _to_dict(delta_max)
            else:
                self._delta_max = self._calculate_elements(max, self._gamma)
            self._delta = self._expand(self._delta_max.values(), lambda x, y: x <= y)

        if gamma and delta:
            self._gamma = set(frozenset(i) for i in gamma)
            self._delta = set(frozenset(i) for i in delta)
            self._gamma_min = self._calculate_elements(min, self._gamma)
            self._delta_max = self._calculate_elements(max, self._delta)

    @classmethod
    def from_string(cls, n: int, *args: str) -> "AccessStructure":
        """
        Construct an `AccessStructure` from the string representation of the minimal sets in Gamma.

        Examples
        --------
        >>> import linearschemes as ls
        >>> ac = ls.AccessStructure.from_string(4, "12", "34", "23")
        >>> ac.is_complete()
        True
        """
        return cls(n, [[int(e) for e in i] for i in args])

    def is_complete(self) -> bool:
        """
        Check if `self` is a complete access structure.

        An access structure is complete if the union of Gamma and Delta equals to the power set of
        the participants.
        """
        return self._gamma | self._delta == self._ps

    def is_trivial(self) -> bool:
        """
        Check if `self` is a trivial access structure.

        An access structure is trivial if Gamma equals to the empty set. Further, the secret would not be
        completely secret if the empty set not in Delta.
        """
        return not (set() != self._gamma and frozenset([]) in self._delta)

    def dual(self) -> "AccessStructure":
        """Return the dual access structure of `self`."""
        gamma_dual, delta_dual = [], []
        p = set(range(1, self._n + 1))

        for x in self._ps:
            x = set(x)
            if p - x in self._delta:
                gamma_dual.append(list(x))
            elif p - x in self._gamma:
                delta_dual.append(list(x))

        return AccessStructure(self._n, gamma=gamma_dual, delta=delta_dual)

    def _calculate_elements(self, f: Callable, s: Set[frozenset]) -> Dict[str, frozenset]:
        c = self._ps - s
        ml = f(len(i) for i in c)
        return _to_dict([i for i in c if len(i) == ml])

    def _expand(self,
                s: ValuesView[frozenset],
                comp: Callable[[frozenset, frozenset], bool]) -> Set[frozenset]:
        res = set()
        for i in set(frozenset(i) for i in s):
            for psi in self._ps:
                if comp(psi, i):
                    res.add(psi)
        return res

    @property
    def gamma(self):
        return self._gamma

    @property
    def delta(self):
        return self._delta

    @property
    def gamma_min(self):
        return self._gamma_min

    @property
    def delta_max(self):
        return self._delta_max

    @property
    def n(self):
        return self._n

    def __eq__(self, other: "AccessStructure") -> bool:
        if not isinstance(other, AccessStructure):
            return False
        return self._n == other.n and self._gamma == other.gamma and self._delta == other.delta

    def __ne__(self, other: "AccessStructure") -> bool:
        return not self == other


def _to_dict(iterable: Iterable) -> Dict[str, frozenset]:
    """Convert an `iterable` to a dictionary of `int`: `frozenset` pairs"""
    return dict([(str(i+1), frozenset(e)) for i, e in enumerate(iterable)])
