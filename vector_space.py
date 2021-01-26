from random import choices
from typing import List

from .finite_field import FiniteField

__all__ = ['VectorSpace']


class VectorSpace:
    def __init__(self, field: FiniteField) -> None:
        self.field = field

    @staticmethod
    def is_in_field(vector_space: 'VectorSpace', vector: List[int]) -> bool:
        """Determine if `vector` is in the vector space of `vector_space`."""
        return all(i in vector_space.field.elements for i in vector)

    def multiply(self, a: int, vector: List[int]) -> List[int]:
        """Multiply a `vector` with scalar `a`."""
        if a not in self.field.elements:
            raise ValueError(f'{a} is not in the field of order {self.field.q}')
        if not VectorSpace.is_in_field(self, vector):
            raise ValueError(f'{vector} is not in the vector space')
        return [self.field.multiply(a, i) for i in vector]

    def add(self, v1: List[int], v2: List[int]) -> List[int]:
        """Add two vectors in the vector space of `self`."""
        if not VectorSpace.is_in_field(self, v1):
            raise ValueError(f'{v1} is not in the vector space')
        if not VectorSpace.is_in_field(self, v2):
            raise ValueError(f'{v2} is not in the vector space')
        if len(v1) != len(v2):
            raise ValueError(f'Cannot add two vectors with different lengths')
        return [self.field.add(i, j) for i, j in zip(v1, v2)]

    def choose_vector(self, length: int) -> List[int]:
        """Uniformly choose a vector of length `length` in the vector space of `self`."""
        return choices(self.field.elements, k=length)

    def __eq__(self, other: 'VectorSpace') -> bool:
        if not isinstance(other, VectorSpace):
            return False
        return self.field.q == other.field.q

    def __ne__(self, other: 'VectorSpace') -> bool:
        if not isinstance(other, VectorSpace):
            return True
        return not self == other

    def __str__(self) -> str:
        return f'A vector space over a field of order {self.field.q}'
