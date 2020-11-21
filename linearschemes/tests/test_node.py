import pytest

from ..node import Node


def test_construct_tree():
    tree = Node("root")
    assert tree.name == "root"
    assert tree.label is None
    assert tree.child is None
    assert tree.sibling is None


def test_tree_iterator():
    tree = Node(0)
    tree.child = Node(1)
    tree.child.child = Node(2)
    tree.child.sibling = Node(3)
    tree.child.sibling.child = Node(4)
    tree.child.sibling.sibling = Node(5)

    assert [i.name for i in tree] == [0, 1, 2, 3, 4, 5]
