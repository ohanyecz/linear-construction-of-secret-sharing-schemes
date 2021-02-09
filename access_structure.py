from typing import Callable, Dict, FrozenSet, Iterable, Iterator, Optional, Set, Union, ValuesView

from mytypes import QualifiedSets, ForbiddenSets
from utils import powerset


class AccessStructure:
    """
    Class to hold the access structure on a set of participants.

    An access structure on the set of participants specifies those subsets of the participants
    who are qualified to reconstruct the secret and those subsets of the participants who are
    forbidden to obtain additional knowledge about the secret by pooling their shares.


    Attributes
    ----------
    participants : int or set
        The number of the participants
    gamma_min : dict, optional
        The minimal elements in Gamma
    delta_max : dict, optional
        The maximal elements in Delta
    gamma: dict, optional
        The qualified sets Gamma
    delta: dict, optional
        The unqualified sets Delta


    Notes
    -----
    - It is recommended that either `gamma_min` OR `gamma` *and* `delta` should be passed to the class.
    If no parameter is passed, the class assumes a complete trivial access structure (*i.e.* Gamma is the empty set and
    Delta is equal to the power set of the participants)

    - If only `gamma_min` is passed, then it is assumed that the access structure is complete.
    If this behaviour is not intended, pass the maximal sets `delta_max` as well.

    - You can access the minimal sets in Gamma, maximal sets in Delta, Gamma and Delta itself directly:
    >>> ac.gamma_min
    >>> ac.delta_max
    >>> ac.gamma
    >>> ac.delta


    Examples
    --------
    >>> trivial = AccessStructure(4)
    >>> trivial.is_trivial()
    True
    >>> trivial.gamma
    set()
    >>> print(trivial)
    A trivial access structure on the set of 4 participants.
    >>> g_min = {'1': {1, 2}, '2': {3, 4}, '3': {2, 3}}
    >>> ac = AccessStructure(4, gamma_min=g_min)
    >>> print(ac)
    A non-trivial access structure on the set of 4 participants.
    >>> ac.is_trivial()
    False
    >>>
    >>> ac2 = AccessStructure.from_string(4, '12', '34', '23')
    >>> ac2.gamma_min
    {'1': {1, 2}, '2': {3, 4}, '3': {2, 3}}
    >>> ac == ac2
    True

    """

    def __init__(self,
                 participants: Union[int, Set[int]], *,
                 gamma_min: Optional[QualifiedSets] = None,
                 delta_max: Optional[ForbiddenSets] = None,
                 gamma: Optional[Set[FrozenSet[int]]] = None,
                 delta: Optional[Set[FrozenSet[int]]] = None) -> None:
        if isinstance(participants, int):
            self.participants = set(range(1, participants+1))
        elif isinstance(participants, set):
            self.participants = participants
        else:
            raise TypeError(f'Cannot handle type {type(participants)} as participants')

        if gamma_min or delta_max:
            self.gamma_min = gamma_min
            self.gamma = self._expand(gamma_min, lambda x, y: y <= x)

            if gamma_min and delta_max:
                if gamma_min == delta_max:
                    raise ValueError(f'gamma_min and delta_max are the same sets.')
                if _is_empty_intersection(gamma_min, delta_max):
                    raise ValueError(f'Intersection of gamma_min and delta_max is not empty.')

            if delta_max:
                self.delta_max = delta_max
            else:
                self.delta_max = self._calculate_elements(max, self.gamma)
            self.delta = self._expand(self.delta_max, lambda x, y: x <= y)
        elif gamma and delta:
            self.gamma = gamma
            self.delta = delta
            self.gamma_min = self._calculate_elements(min, self.delta)
            self.delta_max = self._calculate_elements(max, self.gamma)
        else:
            self.gamma_min = gamma_min
            self.delta_max = delta_max
            self.gamma = set()
            self.delta = {frozenset(i) for i in powerset(self.participants)}

    @classmethod
    def from_string(cls, participants: Union[int, Set[int]], *args: str) -> 'AccessStructure':
        """
        Construct an `AccessStructure` from the string representation of the minimal sets in Gamma.

        Examples
        --------
        >>> ac1 = AccessStructure.from_string(4, '12', '34', '23')
        >>> ac1.gamma_min
        {'1': {1, 2}, '2': {3, 4}, '3': {2, 3}}
        >>> gamma_min = ['12', '23']
        >>> ac2 = AccessStructure.from_string(4, *gamma_min)
        >>> ac2.gamma_min
        {'1': {1, 2}, '2': {2, 3}}

        """
        g_min = {}
        for i, e in enumerate(args, start=1):
            g_min[str(i)] = {int(j) for j in e}
        return cls(participants, gamma_min=g_min)

    def is_complete(self) -> bool:
        """
        Check if `self` is a complete access structure.

        An access structure is complete if the union of Gamma and Delta equals to the power set of
        the participants.
        """
        return self.delta == {frozenset(i) for i in powerset(self.participants)} - self.gamma

    def is_trivial(self) -> bool:
        """
        Check if `self` is a trivial access structure.

        An access structure is trivial if Gamma equals to the empty set. Further, the secret would not be
        completely secret if the empty set not in Delta.
        """
        return not (self.gamma and frozenset() in self.delta)

    def dual(self) -> 'AccessStructure':
        """Return the dual access structure of `self`."""
        gamma_dual, delta_dual = set(), set()

        for x in powerset(self.participants):
            x_c = frozenset(self.participants - x)
            if x_c in self.delta:
                gamma_dual.add(frozenset(x))
            elif x_c in self.gamma:
                delta_dual.add(frozenset(x))

        return AccessStructure(self.participants, gamma=gamma_dual, delta=delta_dual)

    def _calculate_elements(self,
                            f: Callable[[Iterable], int],
                            s: Set[FrozenSet[int]]) -> Union[QualifiedSets, ForbiddenSets]:
        """
        Return the minimal or maximal sets.

        If the function `max` is passed then this function returns the maximal sets in a larger set. If the `min`
        function is passed the the function returns the minimal sets in a set.

        Parameters
        ----------
        f: callable
            A function which returns either the minimal or maximal element of an iterable.
        s: set
            The set from the function calculates the minimal or maximal sets.

        Returns
        -------
        res: dict
            The minimal or maximal sets where a key uniquely identifies a set.
        """
        frozen_ps = set(frozenset(i) for i in powerset(self.participants))
        s_comp = frozen_ps - s
        length = f(len(i) for i in s_comp)
        mset = [i for i in s_comp if len(i) == length]
        return {str(k): set(v) for k, v in enumerate(mset, start=1)}

    def _expand(self,
                s: Dict[str, Set[int]],
                compare: Callable[[set, set], bool]) -> Set[FrozenSet[int]]:
        res = set()
        for i in s.values():
            for psi in powerset(self.participants):
                if compare(psi, i):
                    res.add(frozenset(psi))
        return res

    def __eq__(self, other: 'AccessStructure') -> bool:
        if not isinstance(other, AccessStructure):
            return False
        return (self.participants == other.participants and
                len(self.gamma_min) == len(other.gamma_min) and
                all(i in other.gamma_min.values() for i in self.gamma_min.values()) and
                all(i in self.gamma_min.values() for i in other.gamma_min.values()) and
                len(self.delta_max) == len(other.delta_max) and
                all(i in other.delta_max.values() for i in self.delta_max.values()) and
                all(i in self.delta_max.values() for i in other.delta_max.values()))

    def __ne__(self, other: 'AccessStructure') -> bool:
        return not self == other

    def __str__(self) -> str:
        s = f'access structure on the set of {len(self.participants)} participants.'
        if self.is_trivial():
            return f'A trivial {s}'
        return f'A non-trivial {s}'


def _is_empty_intersection(a, b) -> bool:
    """Check if the intersection of two sets is empty."""
    a = set(frozenset(i) for i in a.values())
    b = set(frozenset(i) for i in b.values())
    return bool(a & b)
