import pytest

from KBNPathfinder.graph import Node
from KBNPathfinder.kbn import (
    find_next_best_neighbors,
    get_k_best_nodes,
    get_neighboor_with_max_regional_score,
)


def test_get_k_best_nodes(random_graph):
    first_node = random_graph.nodes[0]
    k_best_nodes_list = get_k_best_nodes(graph=random_graph, first_node=first_node, k=3)
    print(k_best_nodes_list)
    assert len(k_best_nodes_list) == 3
    assert all([isinstance(node, Node) for node in k_best_nodes_list])


def test_find_next_best_neighbors(random_graph):
    # Given
    k = 3
    added_node = random_graph.nodes[84]
    selected_nodes = [random_graph.nodes[0], random_graph.nodes[44]]
    node_count_to_add = k - len(selected_nodes)  # 1

    # When
    final_selected_nodes = find_next_best_neighbors(
        graph=random_graph,
        selected_nodes=selected_nodes,
        node_count_to_add=node_count_to_add,
    )

    # Then
    assert len(final_selected_nodes) == k
    assert final_selected_nodes[-1] == added_node


def test_get_neighboor_with_max_regional_score(random_graph):
    best_neighbor = get_neighboor_with_max_regional_score(
        random_graph,
        node_id=0,
        excluded_node_ids_list=[],
        amount_of_neighbors_to_compare=3,
    )

    assert best_neighbor.id == 44
