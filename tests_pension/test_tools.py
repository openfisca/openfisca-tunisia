"""Tests of tools."""

# Third Party
import numpy as np

# First Party
from openfisca_tunisia_pension.tools import mean_over_k_consecutive_largest


def test_mean_over_consecutive_largest():
    array = np.array([1] * 5 + [100] * 5 + [1000] * 5).astype(np.float32)

    assert mean_over_k_consecutive_largest(array, 1) == 1000
    assert mean_over_k_consecutive_largest(array, 3) == 1000
    assert mean_over_k_consecutive_largest(array, 5) == 1000
    assert mean_over_k_consecutive_largest(array, 6) == 850
