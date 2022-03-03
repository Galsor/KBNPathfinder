from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type, Dict

from KBNPathfinder.metrics.scores import node_relative_score
from KBNPathfinder.structures.node import Node


@dataclass
class BaseEdge(ABC):
    id: int
    nodes: List[Type[Node]]

    @property
    @abstractmethod
    def cost(self) -> float:
        ...

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


class BaseKBNGraph(ABC):
    nodes: Dict[int, Type[Node]]
    neighborhood: Dict[int, List[int]]
    edges: Dict[int, Type[BaseEdge]]

    @abstractmethod
    def build_egdes(self) -> Dict[int, Type[BaseEdge]]:
        ...

    @abstractmethod
    def get_node_regional_score(self, node_id: int, k: int) -> float:
        ...
