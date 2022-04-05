from abc import ABC, abstractmethod
from typing import List
from heapq import nlargest


from src.structures.graph import KBNGraph


class BaseConvolutionScore(ABC):

    def __new__(cls, *args, **kwargs) -> float:
        return cls.score(*args, **kwargs)

    @classmethod
    @abstractmethod
    def score(cls, *args, **kwargs) -> float:
        ...


class KBestNodes(BaseConvolutionScore):

    @classmethod
    def score(cls, graph: KBNGraph, node_ids: List[int], k: int, *args, **kwargs) -> float:
        """ returns the sum of selected nodes score
        nodes_ids is the list of nodes_id as returned by the Convolver
        """
        nodes_scores = [graph.nodes[node_id].score for node_id in node_ids]
        best_scores = nlargest(k, nodes_scores)
        return sum(best_scores)
