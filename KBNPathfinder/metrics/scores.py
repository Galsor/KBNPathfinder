from typing import Union


def node_relative_score(node_score: Union[int, float], edge_cost: Union[int, float], max_cost: Union[int, float]) -> float:
    return node_score * (1 - edge_cost / max_cost)