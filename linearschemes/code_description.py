from typing import List, Set, Union


__all__ = ["p_support", "projection"]


def p_support(c: List[List[int]]) -> Set[int]:
    """Calculate p-support of a code vector `c`."""
    return {i + 1 for i, cw in enumerate(c) if any(cw)}


def projection(c: List[List[int]], x: Union[Set[int], List[int], range]) -> List[List[int]]:
    return [c[i-1] for i in sorted(x)]
