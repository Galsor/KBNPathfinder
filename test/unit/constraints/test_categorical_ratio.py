from typing import Dict, Tuple

import pytest

from src.contraints.categorical_ratio import FlexibleCategoricalRatioConstraint

@pytest.fixture
def mock_constraints() -> Tuple[str, Dict[str, float], int]:
    return "cat", {"A": 0.7, "B": 0.2, "C": 0.1}, 5

@pytest.fixture
def mock_flexible_categorical_ratio_constraint(random_graph, mock_constraints) -> FlexibleCategoricalRatioConstraint:
    property_name, objectives, k = mock_constraints
    return FlexibleCategoricalRatioConstraint(property_name, objectives, random_graph, k)


def test_constructor(mock_flexible_categorical_ratio_constraint, mock_constraints):
    property_name, objectives, k = mock_constraints
    expected_cat_counts = {cat: 0 for cat in objectives}
    expected_objectives_counts = {cat: int(k*obj) for cat, obj in objectives.items()}

    assert mock_flexible_categorical_ratio_constraint.property_name == property_name
    assert mock_flexible_categorical_ratio_constraint.objectives == objectives
    assert mock_flexible_categorical_ratio_constraint.category_counts == expected_cat_counts
    assert mock_flexible_categorical_ratio_constraint.objectives_counts == expected_objectives_counts


def test_compute_category_means(mock_flexible_categorical_ratio_constraint, random_graph):
    cat_means = mock_flexible_categorical_ratio_constraint.compute_category_means(random_graph)
    print(cat_means)
    assert cat_means == {'A': 43.85, 'B': 52.06, 'C': 53.19}


def test_update_state(mock_flexible_categorical_ratio_constraint, random_graph):
    node_to_add = random_graph.nodes[0]
    mock_flexible_categorical_ratio_constraint.update_state(node_to_add)
    assert mock_flexible_categorical_ratio_constraint.category_counts == {'A': 0, 'B': 1, 'C': 0}

@pytest.mark.parametrize("mock_category_counts, expected_completion_states", [
    ({'A': 0, 'B': 0, 'C': 0}, {'A': 0.0, 'B': 0.0, 'C': 1.0}), #C has a low objective so completed by default
    ({'A': 0, 'B': 1, 'C': 0}, {'A': 0.0, 'B': 1.0, 'C': 1.0}),
    ({'A': 1, 'B': 1, 'C': 1}, {'A': 0.3333, 'B': 1.0, 'C': 1.0}),
])
def test_completion_state(mock_category_counts, expected_completion_states, mock_flexible_categorical_ratio_constraint):
    mock_flexible_categorical_ratio_constraint.category_counts = mock_category_counts
    completion_state = mock_flexible_categorical_ratio_constraint.completion_state
    print(mock_flexible_categorical_ratio_constraint.objectives_counts)
    assert completion_state == expected_completion_states

@pytest.mark.parametrize("nodes_added, candidate, expected_penalization_ratio",
                         [
                             ([0, 1, 2], 3, 0.55),
                             ([0, 1, 2], 4, 0),
                             ([0, 1, 2], 9, 1.0),
                         ])
def test_penalize_score(nodes_added, candidate, expected_penalization_ratio, mock_flexible_categorical_ratio_constraint, random_graph):

    candidate_node = random_graph.nodes[candidate]
    for node_id in nodes_added:
        mock_flexible_categorical_ratio_constraint.update_state(random_graph.nodes[node_id])
    penalized_score = mock_flexible_categorical_ratio_constraint.penalize_score(candidate_node)
    penalization_ratio = round(1 - (penalized_score / candidate_node.score), 2)

    assert penalization_ratio == expected_penalization_ratio

