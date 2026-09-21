# Third Party
import numpy as np

# First Party
from openfisca_tunisia_pension.tools import mean_over_k_nonzero_largest

vector = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
res = mean_over_k_nonzero_largest(vector, 2)
print("Resultat de Numba:", res)
