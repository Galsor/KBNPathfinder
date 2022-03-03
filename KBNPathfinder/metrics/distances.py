import numpy as np
from scipy.spatial import distance
from typing import Type, Callable, Dict

from KBNPathfinder.structures.graph import Node


def euclidian_distance(node1: Type[Node], node2: Type[Node]) -> np.float64:
    vector1, vector2 = [node1.x, node1.y], [node2.x, node2.y]
    return distance.euclidean(vector1, vector2)


DISTANCES: Dict[str: Callable] = {
    "euclidian": euclidian_distance
}
