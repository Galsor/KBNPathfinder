from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Node:
    id: int
    x: float
    y: float
    score: int
    properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for prop_name, value in self.properties.items():
            self.__setattr__(prop_name, value)

    def __hash__(self):
        return hash((self.id, self.x, self.y, self.score, *self.properties.values()))
