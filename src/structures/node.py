from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Node:
    id: int
    x: float
    y: float
    score: int
    properties: Dict[str, Any] = field(default_factory={})
