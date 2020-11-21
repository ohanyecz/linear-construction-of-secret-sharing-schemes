from typing import List, Set, Tuple, Union


__all__ = ["p_support", "projection", "epsilon"]


def p_support(c: List[List[int]]) -> Set[int]:
    """Calculate p-support of a code vector `c`."""
    return {i + 1 for i, cw in enumerate(c) if any(cw)}


def projection(c: List[List[int]], x: Union[Set[int], List[int], range]) -> List[List[int]]:
    return [c[i-1] for i in sorted(x)]


def epsilon(r: int, k: int) -> List[Tuple[int, int]]:
    return [(i, j) for j in range(1, k+1) for i in range(1, r+1)]
