import heapq
from typing import Dict, List, Optional, Type

import numpy as np
import pandas as pd

from src.metrics.distances import get_distance
from src.structures.abc import BaseKBNGraph
from src.structures.edge import Edge
from src.structures.node import Node


class KBNGraph(BaseKBNGraph):
    parent: Optional[int] = None

    def __init__(
        self,
        nodes_list: List[Node],
        distance: str = "euclidian",
        max_cost: Optional[float] = None,
        edge_cost_offset: Optional[float] = None,
    ):
        self.max_cost = max_cost
        self.edge_cost_offset = edge_cost_offset if edge_cost_offset is not None else 0
        self._cost_fun = get_distance(distance)

        self.nodes: Dict[int, Type[Node]] = {node.id: node for node in nodes_list}
        self.neighborhood = {node_id: [] for node_id in self.nodes}
        self.edges: Dict[int, Type[Edge]] = {}
        self.build_egdes()

    @property
    def id(self):
        return id(self)

    def build_egdes(self) -> Dict[int, Type[Edge]]:
        """
        Build a dictionary of edge_id (key) and Edge objects (values).
        Edges are created if their cost (distance) is inferior to the max cost of the graph.
        If an edge cost offset is provided the cost value is added with the offset.
        Offsets can represents the cost of visit of a Node (ex: time spent to visit a museum or a shop
        :param cost_offset:
        :type cost_offset: float
        :return: Dictionnary of edges indexes with their id
        :rtype: Dict[int, Edge]
        """
        if self.max_cost is None:
            edges = self._build_edges_without_max_cost()
        else:
            edges = self._build_edges_with_max_cost()
        return edges

    def _build_edges_with_max_cost(self) -> None:
        n = len(self.nodes)
        mask = np.tri(n) - np.eye(n)

        for i, node1 in enumerate(self.nodes.values()):
            for j, node2 in enumerate(self.nodes.values()):
                if mask[i][j]:
                    d = self._cost_fun(node1, node2) + self.edge_cost_offset
                    if d < self.max_cost:
                        self.make_edge(d, node1, node2)

    def _build_edges_without_max_cost(self) -> None:
        """
        Building edges and setting the max edge cost values as class attribute
        """
        max_cost = 0
        n = len(self.nodes)
        mask = np.tri(n) - np.eye(n)

        for i, node1 in enumerate(self.nodes.values()):
            for j, node2 in enumerate(self.nodes.values()):
                if mask[i][j]:
                    d = self._cost_fun(node1, node2) + self.edge_cost_offset
                    self.make_edge(d, node1, node2)
                    if d > max_cost:
                        max_cost = d

        self.max_cost = max_cost

    def make_edge(self, d: float, node1: Type[Node], node2: Type[Node]) -> None:
        edge_id = len(self.edges)
        self.edges[edge_id] = Edge(id=edge_id, nodes=[node1, node2], cost=d)
        self.neighborhood[node1.id].append(edge_id)
        self.neighborhood[node2.id].append(edge_id)

    @property
    def mean_score(self):
        return np.mean([node.score for node in self.nodes.values()])

    def get_node_with_max_score(self) -> Node:
        node_score_dict = {node.score: node for node in self.nodes.values()}
        max_score = max(list(node_score_dict.keys()))
        return node_score_dict[max_score]

    def get_node_regional_score(self, node_id: int, k: int = 10) -> float:
        """
        node_id: Id of the node to investigate
        k: amount of nodes to consider in scoring"""
        k_best_neighbors_relative_scores = self.get_k_best_neighbors(node_id, k)
        return self.regional_score(
            self.nodes[node_id], k_best_neighbors_relative_scores.values()
        )

    @staticmethod
    def regional_score(node: Node, neighborhood_relative_scores: List[float]) -> float:
        n = len(neighborhood_relative_scores) + 1
        return (node.score + sum(neighborhood_relative_scores)) / n

    def get_k_best_neighbors(self, node_id: int, k: int = 10) -> Dict[int, float]:
        """Returns a dictionnary with k best relative score indexed with edge_ids
        /!\ Compute intensive method
        """
        node_egdes_id = self.neighborhood[node_id]
        neighbors_scores = {
            edge_id: self.edges[edge_id].get_dest_relative_score(
                origin_node_id=node_id, max_cost=self.max_cost
            )
            for edge_id in node_egdes_id
        }
        k_best_edge_ids = heapq.nlargest(k, neighbors_scores, key=neighbors_scores.get)
        k_best_neighbors_scores = {
            edge_id: relative_score
            for edge_id, relative_score in neighbors_scores.items()
            if edge_id in k_best_edge_ids
        }
        return k_best_neighbors_scores

    def get_coordinates(self) -> pd.DataFrame:
        coords = {node.id: [node.x, node.y] for node in self.nodes.values()}
        df = pd.DataFrame(coords).T.rename(columns={0: "x", 1: "y"})
        return df


class KBNSubGraph(KBNGraph):
    def __init__(self, parent_graph: KBNGraph, nodes: List[int]):
        self.parent = parent_graph.id
        self.nodes = {node_id: parent_graph.nodes[node_id] for node_id in nodes}

        self.edges = {}
        self.neighborhood = {node_id: [] for node_id in self.nodes}
        self._extract_edges_and_neighboors(parent_graph)

        self.max_cost = parent_graph.max_cost
        self.edge_cost_offset = parent_graph.edge_cost_offset
        self._cost_fun = parent_graph._cost_fun

    def _extract_edges_and_neighboors(self, parent_graph: KBNGraph) -> Dict[int, List[Type[Edge]]]:
        """ Collect edges when **both** nodes are included in the subgraph. Then update class variables."""
        valid_nodes = list(self.nodes.keys())
        for edge_id, edge in parent_graph.edges.items():
            edge_in_subgraph = all([node.id in valid_nodes for node in edge.nodes])
            if edge_in_subgraph:
                self.edges[edge_id] = edge
                for node in edge.nodes:
                    self.neighborhood[node.id].append(edge_id)

