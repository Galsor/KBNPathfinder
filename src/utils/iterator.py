from dataclasses import dataclass
from typing import List

from src.structures.graph import KBNSubGraph, KBNGraph


@dataclass
class SubgraphIterator:
    graph: KBNGraph
    node_list: List[List[int]]

    def __next__(self) -> KBNSubGraph:
        return KBNSubGraph(self.graph, self.node_list.pop(0))
