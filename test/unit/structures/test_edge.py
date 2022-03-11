import pytest

from KBNPathfinder.structures.edge import Edge
from KBNPathfinder.structures.node import Node


def test_edge_constructor(mock_node_pair):
    edge_id = 0
    edge_cost = 42
    e = Edge(id=edge_id, nodes=list(mock_node_pair), cost=edge_cost)

    assert e.id == edge_id
    assert e.cost == edge_cost
    assert set([node.id for node in e.nodes]) == set(
        [node.id for node in mock_node_pair]
    )


def test_get_node(mock_euclidian_edge, mock_node_pair):
    node_id = mock_node_pair[0].id

    node = mock_euclidian_edge.get_node(node_id)

    assert isinstance(node, Node)
    assert node.id == node_id


@pytest.mark.parametrize("node_id, expected_result", [(0, True), (99, False)])
def test_has_node(node_id, expected_result, mock_euclidian_edge):
    has_node = mock_euclidian_edge.has_node(node_id)
    assert has_node == expected_result


def test_get_dest_node(mock_euclidian_edge):
    node1, node2 = mock_euclidian_edge.nodes
    dest_node = mock_euclidian_edge.get_dest_node(node1.id)
    assert isinstance(dest_node, Node)
    assert dest_node.id == node2.id


def test_get_dest_relative_score(mock_euclidian_edge):
    org_node_id = mock_euclidian_edge.nodes[0].id
    rel_score = mock_euclidian_edge.get_dest_relative_score(
        origin_node_id=org_node_id, max_cost=100
    )
    assert round(rel_score, 4) == 9.8586
