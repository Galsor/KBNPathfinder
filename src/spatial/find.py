from typing import Optional, Tuple

import pandas as pd
from scipy.spatial.distance import cdist


def get_closest_node_id(
    coordinates: pd.DataFrame,
    x: float,
    y: float,
    distance="euclidean",
    x_col: str = "x",
    y_col: str = "y",
    id_col: Optional[str] = None,
) -> int:
    cols = [x_col, y_col]

    if id_col is not None:
        cols.append(id_col)

    coordinates = coordinates[cols]

    if id_col is not None:
        coordinates.set_index(id_col)

    closest_node_id = coordinates.iloc[
        cdist([[x, y]], coordinates.values, metric=distance).argmin()
    ].name
    return closest_node_id


def get_coordinates_bounding_box(
    coordinates: pd.DataFrame,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    return (coordinates["x"].min(), coordinates["y"].min()), (
        coordinates["x"].max(),
        coordinates["y"].max(),
    )
