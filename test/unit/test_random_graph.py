import pytest

from src.random_graph import RandomGraph


def test_random_graph():
    g = RandomGraph(n=10)
    expected_properties = ["num", "cat"]

    assert len(g.nodes) == 10
    assert len(g.neighborhood) == 10
    assert g.edges
    assert all([prop in node.properties for node in g.nodes.values() for prop in expected_properties])
