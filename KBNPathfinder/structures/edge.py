from dataclasses import dataclass

from KBNPathfinder.metrics.distances import euclidian_distance
from KBNPathfinder.structures.abc import BaseEdge


@dataclass
class EuclidianBaseEdge(BaseEdge):
    @property
    def cost(self):
        return euclidian_distance(*self.nodes)
