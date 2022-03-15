from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from src.structures.graph import KBNGraph, Node


class RandomGraph(KBNGraph):
    CATEGORICAL_PROPERTIES = ["A", "B", "C"]

    def __init__(
        self,
        n: int = 100,
        max_cost: float = 0.4,
        distance: str = "euclidian",
        edge_cost_offset: float = 0.0,
        with_properties: bool = False,
        random_seed: Optional[int] = None,
    ):
        self.random_gen = np.random.default_rng(seed=random_seed)
        nodes_list = self.gen_rand_node(n=n, with_properties=with_properties)
        super(RandomGraph, self).__init__(
            nodes_list,
            distance=distance,
            max_cost=max_cost,
            edge_cost_offset=edge_cost_offset,
        )

    def gen_rand_node(self, n=10, with_properties=False) -> List[Node]:
        nodes = []
        x, y = self.gen_random_coordinates(n)
        v = self.gen_random_scores(n)
        properties = self.gen_properties(n, with_categorical=True, with_numerical=True)
        for i in range(n):
            nodes.append(
                Node(id=i, x=x[i], y=y[i], score=v[i], properties=properties[i])
            )
        return nodes

    def gen_random_coordinates(self, n: int) -> Tuple[np.ndarray, np.ndarray]:
        return self.random_gen.random(n), self.random_gen.random(n)

    def gen_random_scores(self, n: int) -> np.ndarray:
        return self.random_gen.integers(0, 100, n)

    def gen_properties(
        self, n: int, with_categorical: bool = True, with_numerical: bool = True
    ) -> List[Dict[str, Union[str, int]]]:
        properties = [{} for _ in range(n)]

        raw_properties = {}
        if with_categorical:
            categories = self.gen_rand_cat_property(n)
            raw_properties["cat"] = categories
        if with_numerical:
            numerical = self.gen_rand_num_property(n)
            raw_properties["num"] = numerical

        for prop_name, values in raw_properties.items():
            for i, value in enumerate(values):
                properties[i][prop_name] = values[i]

        return properties

    def gen_rand_cat_property(self, n: int) -> np.ndarray:
        probabilistic_distribution = self.random_gen.dirichlet(
            np.ones(len(self.CATEGORICAL_PROPERTIES)), size=1
        )[0]
        return self.random_gen.choice(
            self.CATEGORICAL_PROPERTIES, size=n, p=probabilistic_distribution
        )

    def gen_rand_num_property(self, n: int) -> np.ndarray:
        return self.random_gen.integers(0, 100, n)
