# Standard Library
import math

# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_capital_deces_actif_normal():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "agent_actif": {
                    "age_deces": {"2024-01": 45},
                    "deces_par_accident": {"2024-01": False},
                    "cnrps_remuneration_annuelle_deces": {"2024-01": 12000},
                    "cnrps_duree_services_effectifs": {"2024-01": 15},
                    "nombre_enfants_charge": {"2024-01": 2},  # +20%
                }
            }
        },
    )

    # R = 12000
    # MA = (12000/12) * 15 = 15000
    # CD1 = 12000 + 15000 = 27000
    # ME = 27000 * 0.10 * 2 = 5400
    # CD = 27000 + 5400 = 32400

    res = sim.calculate("cnrps_capital_deces", "2024-01")[0]
    print(f"Capital Décès (Actif Normal): {res}")
    assert math.isclose(res, 32400.0, abs_tol=1e-5)


def test_capital_deces_accident_travail():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "agent_accident": {
                    "age_deces": {"2024-01": 50},
                    "deces_par_accident": {"2024-01": True},  # Should double
                    "cnrps_remuneration_annuelle_deces": {"2024-01": 12000},
                    "cnrps_duree_services_effectifs": {"2024-01": 15},
                    "nombre_enfants_charge": {"2024-01": 2},
                }
            }
        },
    )

    # Same base calculation: 32400
    # Accident multiplier: x 2 = 64800
    res = sim.calculate("cnrps_capital_deces", "2024-01")[0]
    print(f"Capital Décès (Accident): {res}")
    assert math.isclose(res, 64800.0, abs_tol=1e-5)


def test_capital_deces_retraite_72_ans():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "retraite_vieux": {
                    "age_deces": {"2024-01": 72},
                    "deces_par_accident": {"2024-01": False},
                    "cnrps_remuneration_annuelle_deces": {"2024-01": 12000},
                    "cnrps_duree_services_effectifs": {"2024-01": 35},  # Capped at 18
                    "nombre_enfants_charge": {"2024-01": 0},
                }
            }
        },
    )

    # R = 12000
    # MA = (12000 / 12) * 18_max = 18000
    # CD1 = 12000 + 18000 = 30000
    # ME = 0
    # Base = 30000
    # Retraite age 72 (70-75) -> 40% -> 30000 * 0.4 = 12000
    res = sim.calculate("cnrps_capital_deces", "2024-01")[0]
    print(f"Capital Décès (Retraite 72 ans): {res}")
    assert math.isclose(res, 12000.0, abs_tol=1e-5)


if __name__ == "__main__":
    test_capital_deces_actif_normal()
    test_capital_deces_accident_travail()
    test_capital_deces_retraite_72_ans()
    print("All Capital Décès tests passed!")
