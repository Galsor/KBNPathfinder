import pytest

from src.structures.graph import KBNGraph, KBNSubGraph


def test_get_coordinates(random_graph: KBNGraph):
    coordinates = random_graph.get_coordinates()

    assert list(coordinates.columns) == ["x", "y"]
    assert coordinates.shape == (len(random_graph.nodes), 2)


def test_subgraph_creation(random_graph: KBNGraph):
    nodes_subspace = [0, 2, 3, 5]

    subgraph = KBNSubGraph(random_graph, nodes_subspace)

    assert all([node in nodes_subspace for node in subgraph.nodes])

    both_nodes_of_each_edges_are_in_nodes_subspace = all(
        [node.id in nodes_subspace
         for edge in subgraph.edges.values()
         for node in edge.nodes]
    )
    assert both_nodes_of_each_edges_are_in_nodes_subspace

    all_edges_in_neighborhood_have_their_nodes_in_subgraph = all(
        [node.id in nodes_subspace
         for node_neighborhood in subgraph.neighborhood.values()
         for edge_id in node_neighborhood
         for node in subgraph.edges[edge_id].nodes]
    )
    assert all_edges_in_neighborhood_have_their_nodes_in_subgraph
