import math

from src.metrics.distances import (_DISTANCES, euclidian_distance,
                                             get_distance, register_distance)
from src.structures.node import Node


def test_register_distance():
    distance_name = "test_distance"

    @register_distance(distance_name)
    def null_distance():
        return 0

    assert "test_distance" in _DISTANCES


def test_get_distance():
    distance_name = "test_distance"
    _DISTANCES[distance_name] = lambda x: 42

    distance_fun = get_distance(distance_name)

    assert distance_fun(None) == 42


def test_euclidian_distance():
    node1, node2 = Node(id=0, x=1, y=0, score=0), Node(id=1, x=0, y=1, score=0)
    distance = euclidian_distance(node1, node2)
    assert distance == math.sqrt(2)
