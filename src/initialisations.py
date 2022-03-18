from src.spatial.find import get_closest_node_id
from src.structures.graph import KBNGraph
from src.structures.node import Node


def from_node_with_max_score(graph: KBNGraph) -> Node:
    return graph.get_node_with_max_score()


def from_closest_node(graph: KBNGraph, x: float, y: float) -> Node:
    nodes_coords_df = graph.coordinates()
    closest_node_id = get_closest_node_id(coordinates=nodes_coords_df, x=x, y=y)
    node = graph.nodes[closest_node_id]
    return node
