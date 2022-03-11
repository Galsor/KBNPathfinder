import math

import numpy as np

from src.initialisations import from_node_with_max_score, from_closest_node


def test_from_node_with_max_score(random_graph):
    max_node = from_node_with_max_score(random_graph)

    max_score = max([node.score for node in random_graph.nodes.values()])

    assert max_node.score == max_score

def test_from_closest_node(random_graph):
    closed_node = from_closest_node(random_graph, x=0, y=0)

    ids = [node.id for node in random_graph.nodes.values()]
    min_id = ids[np.argmin([math.sqrt(node.x**2 + node.y**2) for node in random_graph.nodes.values()])]

    assert closed_node.id == min_id