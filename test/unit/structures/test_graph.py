import pytest

from src.structures.graph import KBNGraph


def test_get_coordinates(random_graph: KBNGraph):
    coordinates = random_graph.get_coordinates()

    assert list(coordinates.columns) == ["x", "y"]
    assert coordinates.shape == (len(random_graph.nodes), 2)
