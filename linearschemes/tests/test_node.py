import pytest

from ..node import *


def test_construct_node():
    n = Node(0)
    assert n.name == 0
    assert n.label is None
    assert n.child is None
    assert n.sibling is None
    assert n.parent is None

    c = Node(3)
    n2 = Node(1, child=c)
    assert n2.name == 1
    assert n2.label is None
    assert n2.child is c
    assert n2.sibling is None
    assert n.parent is None

    n3 = Node(1, child=Node(2, label="MyLabel"))
    assert n3.child.label == "MyLabel"


def test_node_iterator():
    n = Node(0, child=Node(1))
    assert [i.name for i in n] == [0, 1]

    n2 = Node(0, child=Node(
        1, sibling=Node(2,
                        child=Node(3, sibling=Node(5)),
                        sibling=Node(4))))
    assert [i.name for i in n2] == [0, 1, 2, 3, 5, 4]


def test_construct_tree():
    r = Node(0)
    t = Tree(r)
    assert t.root is r
    assert t.height == 0
    assert t.size == 1


def test_add_node_to_tree():
    t = Tree(Node(0))
    p = t.add_node(t.root, Node(1))
    assert t.root.child.name == 1
    assert t.root.child.child is None
    assert t.root.child.sibling is None
    assert t.size == 2
    assert t.height == 1

    p = t.add_node(t.root, Node(2))
    assert t.size == 3
    assert t.height == 1

    p = t.add_node(p, Node(3))
    assert t.size == 4
    assert t.height == 2


def test_tree_iterator():
    t = Tree(Node(0))
    p = t.add_node(t.root, Node(1))
    p = t.add_node(t.root, Node(2))
    t.add_node(p, Node(3))
    p = t.add_node(p, Node(4))
    t.add_node(p, Node(5))
    t.add_node(t.root, Node(6))

    assert [i.name for i in t] == [0, 1, 2, 3, 4, 5, 6]
