import math
from typing import List, Optional, Tuple

import pandas as pd

from src.spatial.find import get_coordinates_bounding_box
from src.structures.graph import KBNGraph, KBNSubGraph

logger = logging.getLogger(__name__)

class Convolver:
    x_series: pd.Series
    y_series: pd.Series
    window_x_len: float
    window_y_len: float

    def __init__(self, coords: pd.DataFrame, window_shape: Tuple[float, float],  x_col: str = "x", y_col: str = "y"):
        self.x_series = coords[x_col]
        self.y_series = coords[y_col]
        self.window_x_len, self.window_y_len = window_shape

    def get_index_in_frame(
        self, x_min: float, y_min: float
    ) -> List[int]:
        valid_x_index = self.get_index_when_values_are_between(
            self.x_series, min=x_min, max=x_min + self.window_x_len
        )
        valid_y_index = self.get_index_when_values_are_between(
            self.y_series, min=y_min, max=y_min + self.window_y_len
        )

        index_in_frame = valid_x_index.intersection(valid_y_index)

        return index_in_frame.to_list()

    @staticmethod
    def get_index_when_values_are_between(
        serie: pd.Series, min: float, max: float
    ) -> pd.Index:
        return serie[serie.between(min, max)].index


def find_best_regions(graph: KBNGraph, k: int, window_size: Optional[float] = None) -> KBNSubGraph:
    # TODO: Convolv along coordinates to find region when the sum k best nodes score is the highest.
    #  Return a subgraph with all nodes in the region.
    """Pseudo code
    for lat in range(lat_min, lat_max - step, step):
        for lon in range(lon_min, lon_max - step, step):
            nodes = get_nodes_in_coord_range(lon, lat, window_size:Tuple) " Window_size > step
            get_X_max_nodes(nodes)
    """

    coordinates = graph.coordinates()
    convolver = Convolver(coordinates)
    (min_x, min_y), (max_x, max_y) = get_coordinates_bounding_box(coordinates)

    if window_size is None:
        window_surface = k / graph.node_density  #At least k nodes are expected to be in this window size
        window_size = math.sqrt(window_surface) #TODO : bad idea to compute a square. Better to compute a rectancle with same proportions than the map

    n_steps_x = (x_max - x_min)/window_size
    n_steps_y = ()
    #TODO : continue.




    raise NotImplementedError
