import logging
import math
from typing import List, Optional, Tuple, Dict

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.metrics.convolution import KBestNodes, BaseConvolutionScore
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


def get_subgraphs_nodes_list_from_k_best_nodes_convolution(
        graph: KBNGraph,
        k: int,
        window_shape: Optional[Tuple[float, float]] = None,
        window_overlap: float = 0.75,
        convolution_score: BaseConvolutionScore = KBestNodes
) -> List[List[int]]:
    """
        Explore the graph through a convolution and
        returns a sorted list of nodes id.
        Each element of the list represents the structure of a Subgraph

        TODO: Refactor node score. Unrelevant abstraction

    :param graph: The graph
    :type graph: KBNGraph
    :param k: The amount of best nodes to consider for the compute of the score
    :type k: int
    :param window_shape: The shape of the convolution window
    :type window_shape: Tuple[float, float]
    :param window_overlap: The ratio of the last window to keep in the next frame. Between 0 and 1. Default 0.9
    :type window_overlap: float
    :param convolution_score: A method to
    :type convolution_score: BaseConvolutionScore
    :return: The subgraph including all the nodes of the selected window
    :rtype: KBNSubGraph
    """

    coordinates = graph.coordinates

    (min_x, min_y), (max_x, max_y) = get_coordinates_bounding_box(coordinates)
    norm_x, norm_y = math.sqrt((max_x - min_x)**2), math.sqrt((max_y - min_y)**2)

    if window_shape is None:
        window_shape = compute_default_convolution_window_shape(graph, k, norm_x, norm_y)
    offset_x, offset_y = step_offsets(window_shape, window_overlap)

    logger.info(window_shape)
    logger.info(f"Offsets x:{offset_x}, y:{offset_y}")

    convolver = Convolver(coordinates, window_shape)

    region_by_scores: Dict[float, List[int]] = {}
    iterations_x, iterations_y = [np.arange(min_, max_, offset_)
                                  for min_, max_, offset_ in
                                  zip((min_x, min_y), (max_x, max_y), (offset_x, offset_y))]

    logger.info(f"Amount of subgraphs: {len(iterations_x) * len(iterations_y)}")
    with tqdm(leave=True, mininterval=0.5, total=len(iterations_x) * len(iterations_y)) as pbar:
        for x in iterations_x:
            for y in iterations_y:
                pbar.update(1)
                nodes_indexes = convolver.get_index_in_frame(x, y)
                if len(nodes_indexes) < k:
                    continue
                score = convolution_score(graph, nodes_indexes, k)
                region_by_scores[score] = nodes_indexes

    sorted_subgraphs_nodes_list = [v for k, v in sorted(region_by_scores.items(), reverse=True)]

    return sorted_subgraphs_nodes_list



def compute_default_convolution_window_shape(graph: KBNGraph, k: int, norm_x: float, norm_y: float, min_ratio=0.1) -> Tuple[float, float]:
    """
     Compute default shape of the window according to the node density of the graph.
     Given the fact that `window_surface` / k = `graph_surface` / N_nodes
     The surface coverved by the window is expected to include k nodes
    """
    nodes_count = len(graph.nodes)
    # k nodes are expected to be in the window
    windowing_ratio = k / nodes_count
    if windowing_ratio < min_ratio:
        # Prevent to convolution over-precision taking at least 1% of the graph
        windowing_ratio = min_ratio
    logger.info(f"Windowing ratio: {windowing_ratio}")

    return windowing_ratio * norm_x, windowing_ratio * norm_y


def step_offsets(window_shape: Tuple[float, float], window_overlap_ratio: float) -> Tuple[float, float]:
    """
    Return the distance between initial values of two steps.
    This distances is intended to preserve the window overlap ratio.
    i.e. returns 10% of the window distance if `window_overlap_ratio` at 90% (0.9).
    """
    offset_x, offset_y = tuple(w_len * (1 - window_overlap_ratio) for w_len in window_shape)
    return offset_x, offset_y
