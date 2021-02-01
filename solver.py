from typing import Optional

from tqdm import tqdm

from node import Node, Tree


__all__ = ['Solver']


class Solver:
    def __init__(self, p, vector_space, r):
        self.p = range(1, p+1)
        self.vector_space = vector_space
        self.n = p
        self.r = r
        self.tree = Tree(Node("ROOT"))

    def build_tree(self, progress: Optional[bool] = False):
        ...
