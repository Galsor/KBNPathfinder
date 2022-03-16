from typing import List, Optional

import pandas as pd

from src.structures.node import Node


def build_nodes_from_pandas(
    df: pd.DataFrame,
    score_col: str,
    x_col: str,
    y_col: str,
    id_col: Optional[str] = None,
    properties_cols: List[str] = [],
) -> List[Node]:
    nodes = []
    for i, row in df.iterrows():
        properties = row[properties_cols].to_dict()
        id_value = row[id_col] if id_col is not None else i
        nodes.append(
            Node(
                id=id_value,
                x=row[x_col],
                y=row[y_col],
                score=row[score_col],
                properties=properties,
            )
        )
    return nodes
