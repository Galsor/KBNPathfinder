from abc import ABC, abstractmethod
from typing import Dict, List, Type

from KBNPathfinder.structures.edge import Edge
from KBNPathfinder.structures.node import Node


class BaseKBNGraph(ABC):
    nodes: Dict[int, Type[Node]]
    neighborhood: Dict[int, List[int]]
    edges: Dict[int, Type[Edge]]

    @abstractmethod
    def build_egdes(self) -> Dict[int, Type[Edge]]:
        ...

    @abstractmethod
    def get_node_regional_score(self, node_id: int, k: int) -> float:
        ...
