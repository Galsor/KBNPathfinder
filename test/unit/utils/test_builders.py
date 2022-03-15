import pandas as pd
import pytest

from src.structures.node import Node
from src.utils.builders import build_nodes_from_pandas


def test_build_nodes_from_pandas():
    df = pd.DataFrame(
        {
            "score": [0, 1, 2],
            "x": [10, 5, 0],
            "y": [5, 10, 0],
            "prop": ["foo", "foo", "bar"],
        }
    )
    nodes_list = build_nodes_from_pandas(
        df, x_col="x", y_col="y", score_col="score", properties_cols=["prop"]
    )

    assert len(nodes_list) == 3
    assert all([isinstance(item, Node) for item in nodes_list])
