from typing import List, Optional

import pandas as pd

from src.structures.node import Node


def build_nodes_from_pandas(
    df: pd.DataFrame,
    score_col: str,
    x_col: str,
    y_col: str,
    id_col: Optional[str] = None,
) -> List[Node]:
    selected_cols = [x_col, y_col, score_col]
    if id_col is not None:
        selected_cols.append(id_col)

    nodes_values = df[selected_cols].values
    nodes = []
    for i, row in enumerate(nodes_values):
        id_value = row[3] if id_col is not None else i
        nodes.append(Node(id=id_value, x=row[0], y=row[1], score=row[2]))
    return nodes
