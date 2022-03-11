from typing import Any, Callable, Dict, Type

import numpy as np
from scipy.spatial import distance

from src.structures.node import Node

_DISTANCES: Dict[str, Callable] = {}


def register_distance(name: str) -> Callable:
    def decorator(fun: Callable) -> Callable:
        _DISTANCES[name] = fun

        def wrapper(*args, **kwargs) -> Any:
            return fun(*args, **kwargs)

        return wrapper

    return decorator


def get_distance(name: str) -> Callable:
    try:
        distance_fun = _DISTANCES[name]
        return distance_fun
    except KeyError:
        raise ValueError(
            f"Invalid distance name with {name}. Implemented distances are: [{', '.join(_DISTANCES.keys())}]"
        )


@register_distance("euclidian")
def euclidian_distance(node1: Type[Node], node2: Type[Node]) -> np.float64:
    vector1, vector2 = [node1.x, node1.y], [node2.x, node2.y]
    return distance.euclidean(vector1, vector2)
