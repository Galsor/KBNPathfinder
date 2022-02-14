import pytest

from KBNPathfinder.random_graph import RandomGraph


def test_random_graph():
    g = RandomGraph(n=10)

    assert len(g.nodes) == 10
    assert len(g.neighborhood) == 10
    assert g.edges
