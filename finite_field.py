from operator import add, and_, sub, mul, xor
from typing import Optional

from utils import is_prime


class FiniteField:
    """
    A simple implementation of a finite field.

    Attributes
    ----------
    p: int
        A prime number, the order of the field
    n: int, optional
        The power to raise `p` to.
    """
    def __init__(self, p: int, n: Optional[int] = None) -> None:
        if not is_prime(p):
            raise ValueError(f'The order of the finite field should be prime ({p} given)')
        if n:
            self.q = p ** n
        else:
            self.q = p
        self.elements = range(self.q)

    def add(self, a: int, b: int) -> int:
        return self._perform(add, a, b)

    def subtract(self, a: int, b: int) -> int:
        return self._perform(sub, a, b)

    def multiply(self, a: int, b: int) -> int:
        return self._perform(mul, a, b)

    def _perform(self, op, a, b):
        if a not in self.elements:
            raise ValueError(f'Number {a} is not in the field.')
        if b not in self.elements:
            raise ValueError(f'Number {b} is not in the field.')
        return op(a, b) % self.q

    def __eq__(self, other: 'FiniteField') -> bool:
        if not isinstance(other, FiniteField):
            return False
        return self.q == other.q

    def __ne__(self, other: 'FiniteField') -> bool:
        return not self == other

    def __str__(self) -> str:
        return f'A finite field of order {self.q}'


class FiniteField2(FiniteField):
    """
    Finite field of order 2.
    """
    def __init__(self) -> None:
        super().__init__(2)

    def add(self, a: int, b: int) -> int:
        return self._perform(xor, a, b)

    def subtract(self, a: int, b: int) -> int:
        return self.add(a, b)

    def multiply(self, a: int, b: int) -> int:
        return self._perform(and_, a, b)
