import pandas as pd
import pytest

from src.spatial.convolutions import Convolver


@pytest.fixture
def mock_convolver() -> Convolver:
    coords = pd.DataFrame([[0.1, 0.1],
                           [0.115, 0.11],
                           [0.3, 0.5]], columns=["x", "y"])
    return Convolver(coords=coords, x_col="x", y_col="y", window_shape=(0.1, 0.1))


def test_get_index_in_frame(mock_convolver):
    indexes = mock_convolver.get_index_in_frame(x_min=0.1, y_min=0.1)
    assert len(indexes) == 2
    assert all(i in indexes for i in [0,1])
