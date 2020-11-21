__all__ = ["Node"]


class Node:
    def __init__(self, name, label=None, child=None, sibling=None):
        self.name = name
        self.label = label
        self.child = child
        self.sibling = sibling
        self.parent = None

    def __iter__(self):
        yield self
        yield from self.child if self.child else ()
        yield from self.sibling if self.sibling else ()


class Tree:
    def __init__(self, root: "Node"):
        self.root = root
        self._height = 0
        self._size = 1

    def __iter__(self):
        yield self.root
        yield from self.root.child if self.root.child else ()
        yield from self.root.sibling if self.root.sibling else ()

    def add_node(self, parent, node):
        """
        Adds a new child `node` of `parent`.

        Parameters
        ----------
        parent : Node
            The parent node of the new child
        node : Node
            The new child node of parent

        Returns
        -------
        node : Node
            The newly inserted node so it can be used as a parent.
        """
        if parent is None:
            raise ValueError("Cannot overwrite root node.")

        node.parent = parent
        if parent.child is None:
            parent.child = node
            self._height += 1
            self._size += 1
            return parent.child
        else:
            n = parent.child
            while n.sibling is not None:
                n = n.sibling

            n.sibling = node
            self._size += 1
            return n.sibling

    @property
    def height(self):
        """Returns the height of the tree."""
        return self._height

    @property
    def size(self):
        """Returns the number of nodes in the tree."""
        return self._size
