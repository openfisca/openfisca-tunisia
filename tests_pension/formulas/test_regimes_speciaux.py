# Standard Library
import math

# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_regime_gouverneurs():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "gouverneur_non_eligible": {
                    "gouverneur_duree_service": {
                        "2024": 4
                    },  # 1 year (4 trimesters) -> not eligible
                    "gouverneur_remuneration": {"2024": 1000},
                },
                "gouverneur_normal": {
                    "gouverneur_duree_service": {
                        "2024": 20
                    },  # 5 years (20 trimesters) -> 30%
                    "gouverneur_remuneration": {"2024": 1000},
                },
                "gouverneur_maxed": {
                    "gouverneur_duree_service": {
                        "2024": 80
                    },  # 20 years = 120% -> capped at 90%
                    "gouverneur_remuneration": {"2024": 1000},
                },
            }
        },
    )

    pension_non_eligible = sim.calculate("gouverneur_pension_brute", "2024")[0]
    pension_normal = sim.calculate("gouverneur_pension_brute", "2024")[1]
    pension_maxed = sim.calculate("gouverneur_pension_brute", "2024")[2]

    assert pension_non_eligible == 0.0
    # 20 trimesters * 0.015 = 0.30 -> 1000/month = 12000/year -> 12000 * 0.30 = 3600
    assert math.isclose(pension_normal, 3600.0, abs_tol=1e-5)
    # Capped at 90% -> 12000 * 0.90 = 10800
    assert math.isclose(pension_maxed, 10800.0, abs_tol=1e-5)


def test_regime_deputes():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "depute_non_eligible": {
                    "depute_nombre_legislatures": {"2024": 0},
                    "depute_indemnite": {"2024": 2000},
                },
                "depute_1_leg": {
                    "depute_nombre_legislatures": {"2024": 1},  # 30%
                    "depute_indemnite": {"2024": 2000},
                },
                "depute_maxed": {
                    "depute_nombre_legislatures": {"2024": 4},  # Capped at 90%
                    "depute_indemnite": {"2024": 2000},
                },
            }
        },
    )

    pension_non_eligible = sim.calculate("depute_pension_brute", "2024")[0]
    pension_1_leg = sim.calculate("depute_pension_brute", "2024")[1]
    pension_maxed = sim.calculate("depute_pension_brute", "2024")[2]

    assert pension_non_eligible == 0.0
    # 2000/month = 24000/year -> 24000 * 0.30 = 7200
    assert math.isclose(pension_1_leg, 7200.0, abs_tol=1e-5)
    # 24000 * 0.90 = 21600
    assert math.isclose(pension_maxed, 21600.0, abs_tol=1e-5)


if __name__ == "__main__":
    test_regime_gouverneurs()
    test_regime_deputes()
    print("All Special Regimes tests passed!")
