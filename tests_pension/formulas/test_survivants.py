# Standard Library
import math

# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def run_sim(nb_orphelins, conjoint_eligible):
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "famille_test": {
                    "age_deces": {"2024-01": 60},  # deceased
                    "cnrps_pension_reference_deces": {"2024-01": 1000.0},
                    "nombre_orphelins_eligibles": {"2024-01": nb_orphelins},
                    "conjoint_survivant_eligible": {"2024-01": conjoint_eligible},
                }
            }
        },
    )
    rev = sim.calculate("cnrps_pension_de_reversion", "2024-01")[0]
    orph = sim.calculate("cnrps_pension_orphelins_totale", "2024-01")[0]
    return rev, orph


def test_reversion_seule_1_orphelin():
    rev, orph = run_sim(1, True)
    assert math.isclose(rev, 750.0, abs_tol=1e-5)  # 75% of 1000
    assert math.isclose(orph, 100.0, abs_tol=1e-5)  # 10% of 1000


def test_reversion_3_orphelins():
    rev, orph = run_sim(3, True)
    assert math.isclose(rev, 700.0, abs_tol=1e-5)  # 75% - 5% = 70%
    assert math.isclose(orph, 300.0, abs_tol=1e-5)  # 10% * 3 = 30%


def test_reversion_4_orphelins():
    rev, orph = run_sim(4, True)
    assert math.isclose(rev, 600.0, abs_tol=1e-5)  # 75% - 5% - 10% = 60%
    assert math.isclose(orph, 400.0, abs_tol=1e-5)  # 10% * 4 = 40%


def test_reversion_5_orphelins():
    rev, orph = run_sim(5, True)
    assert math.isclose(rev, 500.0, abs_tol=1e-5)  # cap 50%
    assert math.isclose(orph, 500.0, abs_tol=1e-5)  # remaining 50%


def test_orphelins_seuls_sans_conjoint_2_orp():
    rev, orph = run_sim(2, False)
    assert math.isclose(rev, 0.0, abs_tol=1e-5)
    assert math.isclose(orph, 950.0, abs_tol=1e-5)  # 2 * 10% + 75% = 95%


def test_orphelins_seuls_sans_conjoint_4_orp():
    rev, orph = run_sim(4, False)
    assert math.isclose(rev, 0.0, abs_tol=1e-5)
    assert math.isclose(
        orph, 1000.0, abs_tol=1e-5
    )  # 4 * 10% + 75% = 115% -> capped at 100%


if __name__ == "__main__":
    test_reversion_seule_1_orphelin()
    test_reversion_3_orphelins()
    test_reversion_4_orphelins()
    test_reversion_5_orphelins()
    test_orphelins_seuls_sans_conjoint_2_orp()
    test_orphelins_seuls_sans_conjoint_4_orp()
    print("All Survivor tests passed!")
