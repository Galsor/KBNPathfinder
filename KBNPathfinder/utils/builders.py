from typing import List

import pandas as pd

from KBNPathfinder.structures.node import Node


def build_nodes_from_pandas(df:pd.DataFrame, score_col: str, x_col:str, y_col:str) -> List[Node]:
    nodes_values = df[[x_col, y_col, score_col]].values
    nodes = []
    for i, row in enumerate(nodes_values):
        nodes.append(Node(id=i, x=row[0], y=row[1], score=row[2]))
    return nodes
