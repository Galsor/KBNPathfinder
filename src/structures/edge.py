from dataclasses import dataclass
from typing import Dict, Type, Tuple

from src.metrics.scores import node_relative_score
from src.structures.node import Node


@dataclass
class Edge:
    id: int
    nodes: Tuple[Type[Node]]
    cost: float

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
        return node_relative_score(dest_node.score, self.cost, max_cost)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f"{type(other)} can't be compared with Edge.")
        eq_id = self.id == other.id
        eq_nodes = set(other.nodes) == set(self.nodes)
        eq_cost = other.cost == self.cost
        return all([eq_id, eq_nodes, eq_cost])

    def __hash__(self):
        return hash((self.id, self.nodes[0], self.nodes[1], self.cost))

