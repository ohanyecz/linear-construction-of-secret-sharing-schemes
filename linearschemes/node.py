__all__ = ["Node"]


class Node:
    def __init__(self, name, label=None, child=None, sibling=None):
        self.name = name
        self.label = label
        self.child = child
        self.sibling = sibling

    def __iter__(self):
        yield self
        yield from self.child if self.child else ()
        yield from self.sibling if self.sibling else ()
