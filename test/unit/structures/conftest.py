import math
from typing import Type, Tuple

import pytest

from KBNPathfinder.structures.edge import Edge
from KBNPathfinder.structures.node import Node


@pytest.fixture
def mock_node_pair() -> Tuple[Type[Node]]:
    node1 = Node(id=0, score=0, x=0, y=1)
    node2 = Node(id=1, score=10, x=1, y=0)
    return node1, node2


@pytest.fixture
def mock_euclidian_edge(mock_node_pair) -> Type[Edge]:
    cost = math.sqrt(2)
    return Edge(0, list(mock_node_pair), cost)