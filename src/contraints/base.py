from abc import ABC, abstractmethod
from typing import Type

from src.structures.node import Node


class BaseConstraint(ABC):
    @abstractmethod
    def penalize_score(self, node: Type[Node]) -> float:
        ...

    def update_state(self, added_node: Type[Node]) -> None:
        pass

    def revert_state(self, node_to_remove: Type[Node]) -> None:
        pass
