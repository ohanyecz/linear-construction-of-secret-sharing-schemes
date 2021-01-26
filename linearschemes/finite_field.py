from typing import Optional

__all__ = ["FiniteField", "FiniteField2"]


class FiniteField:
    """
    A simple implementation of a finite field.

    Attributes
    ----------
    p : int
        A prime number, the order of the field
    """
    def __init__(self, p: int, n: Optional[int] = None) -> None:
        if n:
            self.q = p ** n
        else:
            self.q = p
        self.elements = range(self.q)

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.q

    def subtract(self, a: int, b: int) -> int:
        return (a - b) % self.q

    def multiply(self, a: int, b: int) -> int:
        return (a * b) % self.q

    def divide(self, a: int, b: int) -> int:
        b_inv = self.inverse(b)
        return self.multiply(a, b_inv)

    def inverse(self, a: int) -> int:
        return pow(a, self.q - 2, self.q)


class FiniteField2(FiniteField):
    """
    Finite field of order 2.
    """
    def __init__(self) -> None:
        super().__init__(2)

    def add(self, a: int, b: int) -> int:
        return a ^ b

    def subtract(self, a: int, b: int) -> int:
        return self.add(a, b)

    def multiply(self, a: int, b: int) -> int:
        return a & b


