from typing import Any, Dict, List, Type

import pandas as pd

from src.contraints.base import BaseConstraint
from src.structures.graph import KBNGraph
from src.structures.node import Node


class FlexibleCategoricalRatioConstraint(BaseConstraint):
    def __init__(
        self, property_name: str, objectives: Dict[Any, float], graph: KBNGraph, k: int
    ):
        self.property_name = property_name
        self.objectives = objectives
        self.objectives_counts = {
            cat: int(obj * k) for cat, obj in self.objectives.items()
        }
        self.k = k
        self.category_counts = {cat: 0 for cat in objectives}
        self.category_means = self.compute_category_means(graph)

    @property
    def completion_state(self) -> Dict[str, float]:
        return {
            cat: round(count / self.objectives_counts[cat], 4)
            if self.objectives_counts[cat] != 0
            else 1.0
            for cat, count in self.category_counts.items()
        }

    def update_state(self, added_node: Node) -> None:
        category = added_node.properties.get(self.property_name)
        if category is not None:
            self.category_counts[category] += 1

    def revert_state(self, node_to_remove: Type[Node]) -> None:
        category = node_to_remove.properties.get(self.property_name)
        if category is not None:
            self.category_counts[category] -= 1

    def compute_category_means(self, graph: KBNGraph) -> Dict[Any, float]:
        df_category = pd.DataFrame(
            [
                [node.properties.get(self.property_name), node.score]
                for node in graph.nodes.values()
            ],
            columns=[self.property_name, "score"],
        )
        df_cat_means = df_category.groupby([self.property_name]).agg("mean").round(2)
        return df_cat_means.to_dict()["score"]

    def penalize_score(self, candidate: Node) -> float:
        """Translate categories values with their ratio of completion.
        This approach preserves High potential values and enable categorical ratio constraints to be unfilled
        """
        category = candidate.properties[self.property_name]
        score = candidate.score
        penalization = self.category_means[category] * self.completion_state[category]
        penalized_score = score - penalization
        return round(penalized_score, 2) if penalized_score > 0 else 0
