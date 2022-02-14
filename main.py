import heapq
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np

logger = logging.getLogger(__file__)

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


""" Deprecated integrated in Egdes
def relative_node_score(node: Node, edge: Edge, max_cost: float) -> float:
    node_score = node.score
    edge_cost = edge.cost
    return node_score * (1 - edge_cost/max_cost)"""

def regional_score(node:Node, neighborhood_relative_scores: List[float], k: int) -> float:
    n = k + 1
    return (node.score + sum(neighborhood_relative_scores))/n

class RandomGraph:

    def __init__(self, n: int = 100, max_cost: float = 0.4):
        self.max_cost = max_cost
        self.nodes: Dict[int, Node] = self.gen_rand_node(n=n)
        self.neighborhood = {node_id: [] for node_id in self.nodes.keys()}
        self.edges: Dict[int, Edge] = self.gen_egdes(n=n)


    @staticmethod
    def gen_rand_node(n=10) -> List[Node]:
        nodes = {}
        x = np.random.rand(n)
        y = np.random.rand(n)
        v = np.random.randint(0, 100, n)
        for i in range(n):
            nodes[i] = Node(id=i, x=x[i], y=y[i], score=v[i])
        return nodes

    def gen_egdes(self, n: int):
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

    def get_k_best_nodes(self, k: int = 10):
        """ Return the best chain of k nodes. Starting with the node of max score"""
        first_node = self.get_node_with_max_score()
        k_best_nodes_list = self.find_next_best_neighbors([first_node], k)
        return k_best_nodes_list

    def find_next_best_neighbors(self, selected_nodes: List[Node], k: int):
        """ Recursivly find k best contiguous nodes"""
        last_node = selected_nodes[-1]
        excluded_nodes_ids = [node.id for node in selected_nodes]
        next_node = self.get_neighboor_with_max_regional_score(last_node.id, excluded_nodes_ids, k)
        if next_node is not None:
            selected_nodes.append(next_node)
        if k > 0:
            selected_nodes = self.find_next_best_neighbors(selected_nodes, k=k-1)
        return selected_nodes

    def get_node_with_max_score(self) -> Node:
        node_score_dict = {node.score: node for node in self.nodes.values()}
        max_score = max(list(node_score_dict.keys()))
        return node_score_dict[max_score]

    def get_k_best_neighbors(self, node_id: int, k: int = 10) -> Dict[int, float]:
        """ Returns a dictionnary with k best relative score indexed with edge_ids
        /!\ Compute intensive method
        """
        node_egdes_id = self.neighborhood[node_id]
        neighbors_scores = {edge_id: self.edges[edge_id].get_dest_relative_score(origin_node_id=node_id, max_cost=self.max_cost) for edge_id in node_egdes_id}
        k_best_edge_ids = heapq.nlargest(k, neighbors_scores, key=neighbors_scores.get)
        k_best_neighbors_scores = {edge_id: relative_score for edge_id, relative_score in neighbors_scores.items() if edge_id in k_best_edge_ids}
        return k_best_neighbors_scores

    def get_node_regional_score(self, node_id:int, k: int = 10) -> float:
        k_best_neighbors_relative_scores = self.get_k_best_neighbors(node_id, k)
        return regional_score(self.nodes[node_id], k_best_neighbors_relative_scores.values(), k)

    def get_neighboor_with_max_regional_score(self, node_id: int, excluded_node_ids_list: List[int], k: int) -> Optional[Node]:
        edges_ids = self.neighborhood[node_id]
        neigh_edges = [self.edges[e_id] for e_id in edges_ids]
        best_neighbor = None
        best_score = 0
        for edge in neigh_edges:
            node = edge.get_dest_node(node_id)
            if node.id not in excluded_node_ids_list:
                regional_score = self.get_node_regional_score(node.id, k)
                if regional_score > best_score:
                    best_score = regional_score
                    best_neighbor = node
        if best_neighbor is None:
            logger.warning("No neighbor found to pursue graph exploration.")
        return best_neighbor


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = RandomGraph()
    g.get_k_best_nodes(k=10)

