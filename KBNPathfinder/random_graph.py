from typing import List, Optional

import numpy as np

from KBNPathfinder.graph import KBNGraph, Node


class RandomGraph(KBNGraph):

    def __init__(self, n: int = 100, max_cost: float = 0.4, random_seed: Optional[int] = None):
        np.random.seed(random_seed)
        self.max_cost = max_cost
        self.nodes = self.gen_rand_node(n=n)
        self.neighborhood = {node_id: [] for node_id in self.nodes.keys()}
        self.edges = self.build_egdes(n=n)

    @staticmethod
    def gen_rand_node(n=10) -> List[Node]:
        nodes = {}
        x = np.random.rand(n)
        y = np.random.rand(n)
        v = np.random.randint(0, 100, n)
        for i in range(n):
            nodes[i] = Node(id=i, x=x[i], y=y[i], score=v[i])
        return nodes