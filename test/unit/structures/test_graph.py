import pytest

from src.structures.graph import KBNGraph, KBNSubGraph


def test_get_coordinates(random_graph: KBNGraph):
    coordinates = random_graph.coordinates()

    assert list(coordinates.columns) == ["x", "y"]
    assert coordinates.shape == (len(random_graph.nodes), 2)


def test_deactivate_node(random_graph):
    node_id_to_deactivate = 0
    assert node_id_to_deactivate in random_graph.nodes
    node = random_graph.nodes[node_id_to_deactivate]
    edges = [
        random_graph.edges[edge_id]
        for edge_id in random_graph.neighborhood[node_id_to_deactivate]
    ]

    random_graph.deactivate_nodes(node_id_to_deactivate)
    deactivated_node, deactivated_edges = random_graph.deactivated_nodes[
        node_id_to_deactivate
    ]
    assert node_id_to_deactivate not in random_graph.nodes
    assert node_id_to_deactivate in random_graph.deactivated_nodes
    assert deactivated_node == node
    assert set(edges) == set(deactivated_edges)


def test_reactivate_node(random_graph):
    deactivated_node_id = 0
    random_graph.deactivate_nodes(deactivated_node_id)
    assert deactivated_node_id in random_graph.deactivated_nodes

    deactivated_node, deactivated_edges = random_graph.deactivated_nodes[
        deactivated_node_id
    ]
    random_graph.reactivate_node(deactivated_node_id)

    assert deactivated_node_id not in random_graph.deactivated_nodes
    assert deactivated_node_id in random_graph.nodes
    assert random_graph.nodes[deactivated_node_id] == deactivated_node
    assert random_graph.neighborhood[deactivated_node_id] == [
        edge.id for edge in deactivated_edges
    ]
    assert all([edge.id in random_graph.edges for edge in deactivated_edges])
    assert set([random_graph.edges[edge.id] for edge in deactivated_edges]) == set(
        deactivated_edges
    )


def test_delete_node(random_graph):
    node_id_to_delete = 0
    related_edges_ids = random_graph.neighborhood[node_id_to_delete]

    random_graph.delete_node(node_id_to_delete)

    assert node_id_to_delete not in random_graph.nodes
    assert node_id_to_delete not in random_graph.nodes
    assert all([edge_id not in random_graph.edges for edge_id in related_edges_ids])


def test_subgraph_creation(random_graph: KBNGraph):
    nodes_subspace = [0, 2, 3, 5]

    subgraph = KBNSubGraph(random_graph, nodes_subspace)

    assert all([node in nodes_subspace for node in subgraph.nodes])

    both_nodes_of_each_edges_are_in_nodes_subspace = all(
        [
            node.id in nodes_subspace
            for edge in subgraph.edges.values()
            for node in edge.nodes
        ]
    )
    assert both_nodes_of_each_edges_are_in_nodes_subspace

    all_edges_in_neighborhood_have_their_nodes_in_subgraph = all(
        [
            node.id in nodes_subspace
            for node_neighborhood in subgraph.neighborhood.values()
            for edge_id in node_neighborhood
            for node in subgraph.edges[edge_id].nodes
        ]
    )
    assert all_edges_in_neighborhood_have_their_nodes_in_subgraph
