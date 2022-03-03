import numpy as np
import ray
from scipy.spatial import distance
from typing import Type

from KBNPathfinder.structures.graph import Node


@ray.remote
def euclidian_distance(node1: Type[Node], node2: Type[Node]) -> np.float64:
    vector1, vector2 = [node1.x, node1.y], [node2.x, node2.y]
    return distance.euclidean(vector1, vector2)




