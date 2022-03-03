from typing import List, Optional

import numpy as np

from KBNPathfinder.structures.graph import KBNGraph, Node


class RandomGraph(KBNGraph):
    def __init__(
        self, n: int = 100, max_cost: float = 0.4, distance: str = "euclidian", edge_cost_offset: float = 0.0, random_seed: Optional[int] = None
    ):
        np.random.seed(random_seed)
        nodes_list = self.gen_rand_node(n=n)
        super(RandomGraph, self).__init__(nodes_list, distance = distance, max_cost= max_cost, edge_cost_offset=edge_cost_offset)

    @staticmethod
    def gen_rand_node(n=10) -> List[Node]:
        nodes = []
        x = np.random.rand(n)
        y = np.random.rand(n)
        v = np.random.randint(0, 100, n)
        for i in range(n):
            nodes.append(Node(id=i, x=x[i], y=y[i], score=v[i]))
        return nodes
