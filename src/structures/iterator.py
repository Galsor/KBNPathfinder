from dataclasses import dataclass
from typing import List

from src.structures.graph import KBNSubGraph, KBNGraph


@dataclass
class SubgraphGenerator:
    graph: KBNGraph
    node_list: List[int]

    def __next__(self) -> KBNSubGraph:
        return KBNSubGraph(self.graph, self.node_list)
