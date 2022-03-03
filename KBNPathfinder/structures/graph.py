import heapq
from typing import Dict, List, Union, Optional, Type

import numpy as np

from KBNPathfinder.metrics.distances import get_distance
from KBNPathfinder.structures.abc import BaseKBNGraph
from KBNPathfinder.structures.edge import Edge, Edge
from KBNPathfinder.structures.node import Node


class KBNGraph(BaseKBNGraph):
    max_cost: float
    nodes: Dict[int, Type[Node]]
    neighborhood: Dict[int, List[int]]
    edges: Dict[int, Type[BaseEdge]]
    edge_offset: Optional[Union[int, float]]

    def build_egdes(self, n: int, cost_fun: str) -> Dict[int, BaseEdge]:
        """
        Build a dictionary of edge_id (key) and Edge objects (values).
        Edges are created if their cost (distance) is inferior to the max cost of the graph.
        If an edge offset is provided the
        :param n:
        :type n:
        :param k:
        :type k:
        :return:
        :rtype:
        """
        edges = {}
        mask = np.tri(n) - np.eye(n)
        for i, node1 in enumerate(self.nodes.values()):
            for j, node2 in enumerate(self.nodes.values()):
                if mask[i][j]:
                    d = BaseEdge.distance(node1, node2)
                    if d < self.max_cost:
                        edge_id = len(edges)
                        edges[edge_id] = Edge(id=edge_id, nodes=[node1, node2], cost=d)
                        self.neighborhood[node1.id].append(edge_id)
                        self.neighborhood[node2.id].append(edge_id)
        return edges

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
