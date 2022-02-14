import heapq
from abc import ABC
from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass
class Node:
    id: int
    x: float
    y: float
    score: int


@dataclass
class Edge:
    id: int
    nodes: List[Node]

    @staticmethod
    def distance(node1: Node, node2: Node) -> float:
        return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    @property
    def cost(self):
        return self.distance(*self.nodes)

    @property
    def node_dict(self) -> Dict[int, Node]:
        return {node.id: node for node in self.nodes}

    def get_node(self, node_id: int) -> Node:
        return self.node_dict[node_id]

    def has_node(self, node_id: int) -> bool:
        return node_id in [node.id for node in self.nodes]

    def get_dest_node(self, origin_node_id: int) -> Node:
        d = self.node_dict.copy()
        del d[origin_node_id]
        return list(d.values())[0]

    def get_dest_relative_score(self, origin_node_id: int, max_cost: float) -> float:
        dest_node = self.get_dest_node(origin_node_id)
        return dest_node.score * (1 - self.cost / max_cost)


class KBNGraph(ABC):
    max_cost: float
    nodes: Dict[int, Node]
    neighborhood: Dict[int, List[int]]
    edges: Dict[int, Edge]

    def build_egdes(self, n: int):
        edges = {}
        mask = np.tri(n) - np.eye(n)
        for i, node1 in enumerate(self.nodes.values()):
            for j, node2 in enumerate(self.nodes.values()):
                if mask[i][j]:
                    d = Edge.distance(node1, node2)
                    if d < self.max_cost:
                        edge_id = len(edges)
                        edges[edge_id] = Edge(id=edge_id, nodes=[node1, node2])
                        self.neighborhood[node1.id].append(edge_id)
                        self.neighborhood[node2.id].append(edge_id)
        return edges

    def get_node_with_max_score(self) -> Node:
        node_score_dict = {node.score: node for node in self.nodes.values()}
        max_score = max(list(node_score_dict.keys()))
        return node_score_dict[max_score]

    def get_node_regional_score(self, node_id: int, k: int = 10) -> float:
        k_best_neighbors_relative_scores = self.get_k_best_neighbors(node_id, k)
        return self.regional_score(self.nodes[node_id], k_best_neighbors_relative_scores.values())

    @staticmethod
    def regional_score(node: Node, neighborhood_relative_scores: List[float]) -> float:
        n = len(neighborhood_relative_scores) + 1
        return (node.score + sum(neighborhood_relative_scores)) / n

    def get_k_best_neighbors(self, node_id: int, k: int = 10) -> Dict[int, float]:
        """ Returns a dictionnary with k best relative score indexed with edge_ids
        /!\ Compute intensive method
        """
        node_egdes_id = self.neighborhood[node_id]
        neighbors_scores = {edge_id: self.edges[edge_id].get_dest_relative_score(origin_node_id=node_id, max_cost=self.max_cost) for edge_id in node_egdes_id}
        k_best_edge_ids = heapq.nlargest(k, neighbors_scores, key=neighbors_scores.get)
        k_best_neighbors_scores = {edge_id: relative_score for edge_id, relative_score in neighbors_scores.items() if edge_id in k_best_edge_ids}
        return k_best_neighbors_scores