from dataclasses import dataclass


@dataclass
class Node:
    id: int
    x: float
    y: float
    score: int
