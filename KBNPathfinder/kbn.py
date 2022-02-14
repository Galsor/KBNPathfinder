from typing import List
import logging

from KBNPathfinder.graph import KBNGraph, Node

logger = logging.getLogger(__name__)

def get_k_best_nodes(graph: KBNGraph, first_node: Node, k: int = 10):
    """ Return the best chain of k nodes. Starting with the node of max score"""
    #TODO: Add initialisation methods
    # - Start_node = Node with Max Score
    # - Best regional score
    k_best_nodes_list = find_next_best_neighbors(graph, [first_node], k)
    return k_best_nodes_list

def find_next_best_neighbors(graph: KBNGraph, selected_nodes: List[Node], k: int):
    """ Recursivly find k best contiguous nodes"""
    last_node = selected_nodes[-1]
    excluded_nodes_ids = [node.id for node in selected_nodes]
    next_node = get_neighboor_with_max_regional_score(last_node.id, excluded_nodes_ids, k)
    if next_node is not None:
        selected_nodes.append(next_node)
    if k > 0:
        selected_nodes = find_next_best_neighbors(graph, selected_nodes, k=k-1)
    return selected_nodes

def get_neighboor_with_max_regional_score(graph: KBNGraph, node_id: int, excluded_node_ids_list: List[int], k: int) -> Optional[Node]:
    edges_ids = graph.neighborhood[node_id]
    neigh_edges = [graph.edges[e_id] for e_id in edges_ids]
    best_neighbor = None
    best_score = 0
    for edge in neigh_edges:
        node = edge.get_dest_node(node_id)
        if node.id not in excluded_node_ids_list:
            regional_score = graph.get_node_regional_score(node.id, k)
            if regional_score > best_score:
                best_score = regional_score
                best_neighbor = node
    if best_neighbor is None:
        logger.warning("No neighbor found to pursue graph exploration.")
    return best_neighbor