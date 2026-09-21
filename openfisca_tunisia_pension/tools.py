"""Tools.

PYTEST_DONT_REWRITE — ce module est compilé par numba dès son import, avec des signatures
explicites. pytest réécrit les modules qu'il importe pour détailler les assertions en échec,
et numba ne sait pas compiler le module réécrit. Le marqueur ci-dessus l'en exclut.
"""

# Third Party
import numpy as np
from numba import float32, int64, jit


def make_mean_over_largest(k):
    def mean_over_largest(vector):
        return mean_over_k_nonzero_largest(vector, k=int(k))

    return mean_over_largest


def make_mean_over_consecutive_largest(k):
    def mean_over_consecutive_largest(vector):
        return mean_over_k_consecutive_largest(vector, k=int(k))

    return mean_over_consecutive_largest


@jit(float32(float32[:], int64), nopython=True)
def mean_over_k_nonzero_largest(vector, k):
    """Return the mean over the k largest values of a vector."""
    if k == 0:
        return 0
    nonzeros = (vector > 0.0).sum()
    if k >= nonzeros:
        return vector.sum() / (nonzeros + (nonzeros == 0))

    z = -np.partition(-vector, kth=k)
    upper_bound = min(k, nonzeros)
    return z[:upper_bound].sum() / upper_bound


@jit(float32(float32[:], int64), nopython=True)
def mean_over_k_consecutive_largest(vector, k):
    """Return the mean over the k largest consecutive values of a vector."""
    if k == 0:
        return 0
    nonzeros = (vector > 0.0).sum()
    if k >= nonzeros:
        return vector.sum() / (nonzeros + (nonzeros == 0))

    if k == 1:
        return vector.max()

    n = len(vector)
    mean = np.zeros(n + 1 - k, dtype=np.float32)
    for p in range(n + 1 - k):
        for i in range(k):
            mean[p] += vector[p + i]
        mean[p] = mean[p] / k
    return mean.max()


def revalorise(
    pension_au_31_decembre_annee_precedente,
    pension,
    annee_de_liquidation,
    revalorisation,
    period,
):
    """Applique la revalorisation à la pension servie."""
    # Third Party
    from openfisca_core.model_api import where

    # Si l'année de liquidation est dans le futur, retourner un tableau vide
    if hasattr(pension, "empty_array"):
        # Pour les périodes futures, retourner un tableau vide
        future_mask = annee_de_liquidation > period.start.year
        if future_mask.any():
            return where(
                future_mask,
                pension.empty_array(),
                pension_au_31_decembre_annee_precedente * (1 + revalorisation),
            )

    # Appliquer la revalorisation
    return pension_au_31_decembre_annee_precedente * (1 + revalorisation)
