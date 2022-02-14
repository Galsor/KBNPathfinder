import pytest

from KBNPathfinder.random_graph import RandomGraph


@pytest.fixture
def random_graph():
    return RandomGraph(n=100, max_cost=0.4, random_seed=42)
