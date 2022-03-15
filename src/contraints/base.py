from abc import ABC, abstractmethod

from src.structures.node import Node


class BaseConstraint(ABC):
    @abstractmethod
    def penalize_score(self, node: Node) -> float:
        ...
