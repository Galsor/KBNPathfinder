from dataclasses import dataclass
from typing import Dict, List, Type

from KBNPathfinder.metrics.scores import node_relative_score
from KBNPathfinder.structures.node import Node


@dataclass
class Edge:
    id: int
    nodes: List[Type[Node]]
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
