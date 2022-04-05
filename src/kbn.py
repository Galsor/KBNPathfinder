import logging
import time
from typing import List, Optional, Type

from src.contraints.base import BaseConstraint
from src.contraints.update import revert_constraints_for_all, update_constraints
from src.initialisations import KBN_INITIALISATIONS
from src.spatial.convolutions import get_subgraphs_nodes_list_from_k_best_nodes_convolution
from src.structures.graph import KBNGraph, Node
from src.utils.iterator import SubgraphIterator

logger = logging.getLogger(__name__)


def get_groups_of_k_best_nodes_from_max_score(
    graph: KBNGraph,
    total_k: int = 10,
    n_groups: int = 5,
    constraints: List[BaseConstraint] = [],
    max_iter: Optional[int] = None,
    initialisation: str = "max_score",
    *args,
    **kwargs
) -> List[List[Type[Node]]]:
    logger.info(f"Main graph information -> Shape:{graph.shape}. Connectivity:{graph.connectivity}")
    logger.info(f"Task objective: select {total_k} nodes divided in {n_groups} groups")

    k_values = dispatch_k_in_n_groups(total_k, n_groups)
    subgraphs_nodes_ids = get_subgraphs_nodes_list_from_k_best_nodes_convolution(
        graph, k=max(k_values), *args, **kwargs
    )
    subgraph_gen = SubgraphIterator(graph, subgraphs_nodes_ids)

    i = 0
    results = []
    max_iter = max_iter if max_iter is not None else n_groups * 3
    while len(results) < n_groups or i < max_iter:
        k = k_values[len(results)]
        logger.info(f"Starting iteration {i} [group {len(results)}]")


        subgraph = next(subgraph_gen)
        logger.info(f"Selected subgraph information -> Shape:{subgraph.shape}. Connectivity:{subgraph.connectivity}")

        init_node = KBN_INITIALISATIONS[initialisation](
            subgraph, k=k, constraints=constraints
        )
        logger.info(f"Node selected for initialisation: {init_node}")
        candidates = get_k_best_nodes(subgraph, init_node, k=k)
        logger.info(f"Candidates selected ({len(candidates)}): {candidates}")
        if len(candidates) >= k:
            results.append(candidates)
            graph.deactivate_nodes(candidates)
            if len(results) == n_groups:
                break
        else:
            revert_constraints_for_all(constraints, candidates)
        i += 1
    return results


def dispatch_k_in_n_groups(total_k, n_groups) -> List[int]:
    base, rest = total_k // n_groups, total_k % n_groups
    k_values = [base for _ in range(n_groups)]
    for i in range(rest):
        k_values[i % n_groups] += 1
    return k_values


def get_k_best_nodes_from_convolution(
        graph: KBNGraph, k: int, constraints: List[BaseConstraint] = []
) -> List[Type[Node]]:
    subgraph = get_subgraphs_nodes_list_from_k_best_nodes_convolution(graph, k, window_overlap=0.9)
    k_best_nodes_list = get_k_best_nodes_from_max_score(subgraph, k, constraints)
    return k_best_nodes_list


def get_k_best_nodes_from_max_score(
    graph: KBNGraph, k: int = 10, constraints: List[BaseConstraint] = []
) -> List[Type[Node]]:
    best_node = graph.get_node_with_max_score()
    k_best_nodes_list = find_next_best_neighbors(graph, [best_node], k - 1, constraints)
    return k_best_nodes_list


def get_k_best_nodes(graph: KBNGraph, first_node: Node, k: int = 10) -> List[Node]:
    """Return the best chain of k nodes. Starting with the node of max score"""
    k_best_nodes_list = find_next_best_neighbors(graph, [first_node], k - 1)
    return k_best_nodes_list

def find_next_best_neighbors(
    graph: KBNGraph,
    selected_nodes: List[Node],
    node_count_to_add: int,
    constraints: List[BaseConstraint] = [],
) -> List[Node]:
    """Recursivly find k best contiguous nodes"""
    last_node = selected_nodes[-1]
    update_constraints(constraints, last_node)

    t0 = time.time()
    next_node = get_neighboor_with_max_regional_score(
        graph, last_node.id, node_count_to_add, constraints
    )

    logger.info(f"Node selection duration: {round(time.time() - t0, 2)}s")
    logger.info(f"Node selected: {next_node}")

    if next_node is not None:
        selected_nodes.append(next_node)
        graph.deactivate_nodes(last_node.id)

    if node_count_to_add > 1:
        # Pursue recursion
        node_count_to_add -= 1
        selected_nodes = find_next_best_neighbors(
            graph, selected_nodes, node_count_to_add, constraints
        )
    elif next_node is not None:
        graph.deactivate_nodes(next_node.id)
        update_constraints(constraints, next_node)

    return selected_nodes


def get_neighboor_with_max_regional_score(
    graph: KBNGraph,
    node_id: int,
    amount_of_neighbors_to_compare: int,
    constraints: List[BaseConstraint] = [],
) -> Optional[Node]:

    edges_ids = graph.neighborhood[node_id]
    neigh_edges = [graph.edges[e_id] for e_id in edges_ids]
    best_neighbor = None
    best_score = 0

    for edge in neigh_edges:
        node = edge.get_dest_node(node_id)
        score = compute_score(graph, node, amount_of_neighbors_to_compare, constraints)
        if score > best_score:
            best_score = score
            best_neighbor = node

    if best_neighbor is None:
        logger.warning("No neighbor found to pursue graph exploration.")

    return best_neighbor


def compute_score(
    graph: KBNGraph,
    node: Node,
    amount_of_neighbors_to_compare: int,
    constraints: List[BaseConstraint] = [],
) -> float:
    regional_score = graph.get_node_regional_score(
        node.id, amount_of_neighbors_to_compare
    )
    scores = [regional_score]
    for constraint in constraints:
        scores.append(constraint.penalize_score(node))

    worst_score = min(scores)
    return worst_score
