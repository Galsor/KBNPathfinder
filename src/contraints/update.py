from typing import List, Type

from src.contraints.base import BaseConstraint
from src.structures.node import Node


def update_constraints(
    constraints: List[Type[BaseConstraint]], selected_node: Type[Node]
) -> None:
    for constraint in constraints:
        constraint.update_state(selected_node)


def revert_constraints(
    constraints: List[Type[BaseConstraint]], node_to_remove: Type[Node]
) -> None:
    for constraint in constraints:
        constraint.revert_state(node_to_remove)


def revert_constraints_for_all(
    constraints: List[Type[BaseConstraint]], nodes_to_remove: List[Type[Node]]
) -> None:
    for node in nodes_to_remove:
        revert_constraints(constraints, node)
