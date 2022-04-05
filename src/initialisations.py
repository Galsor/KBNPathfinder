from typing import Dict, Callable

from src.spatial.find import get_closest_node_id
from src.structures.graph import KBNGraph
from src.structures.node import Node


def from_node_with_max_score(graph: KBNGraph,  *args, **kwargs) -> Node:
    return graph.get_node_with_max_score()


def from_closest_node(graph: KBNGraph, x: float, y: float, *args, **kwargs) -> Node:
    nodes_coords_df = graph.coordinates()
    closest_node_id = get_closest_node_id(coordinates=nodes_coords_df, x=x, y=y)
    node = graph.nodes[closest_node_id]
    return node


KBN_INITIALISATIONS: Dict[str, Callable] = {
    "max_score": from_node_with_max_score,
    "closest": from_closest_node,
}