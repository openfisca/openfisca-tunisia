# Standard Library
import math

# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_coordination_cnss_cnrps():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "mixte": {
                    "age": {"2024": 62},
                    "cnrps_duree_assurance_annuelle": {"2024": 40},  # 10 years in CNRPS
                    "cnss_duree_assurance_annuelle": {"2024": 40},  # 10 years in CNSS
                    "cnrps_salaire_de_base": {"2024": 1000},  # Salary
                }
            }
        },
    )

    # 1. Without CNSS, 40 trimesters < 60 (15 years) required -> Eligible = False
    # With CNSS, total = 80 trimesters >= 60 -> Eligible = True
    eligible = sim.calculate("cnrps_eligible", "2024")[0]
    print(f"Eligible pour retraite mixte: {eligible}")
    assert eligible

    # 2. Base duration is 80 trimesters (20 years)
    # Taux annuité should be the rate for 80 trimesters (2% * 20 = 40% normally, let's see what the barème outputs)
    taux = sim.calculate("cnrps_taux_de_liquidation", "2024")[0]
    print(f"Taux de liquidation (for 80 trimesters): {taux}")  # Expected ~ 0.40

    # 3. Pension brute theorique = 1000 * taux
    # But proratisation = 40 / 80 = 50%
    # So pension brute = 1000 * taux * 0.5
    brute = sim.calculate("cnrps_pension_brute", "2024")[0]
    print(f"Pension brute proratisée: {brute}")

    ref_salary = sim.calculate("cnrps_salaire_de_reference", "2024")[0]
    expected_brute = ref_salary * taux * 0.5
    assert math.isclose(brute, expected_brute, abs_tol=1e-5)


def test_liquidation_separee():
    # If the user has 15 years (60 trimesters) in CNRPS alone, it's a liquidation séparée.
    # Proratisation ratio should be 1.0, not 60/100, and rate calculated on 60.
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "separe": {
                    "age": {"2024": 62},
                    "cnrps_duree_assurance_annuelle": {"2024": 60},  # 15 years in CNRPS
                    "cnss_duree_assurance_annuelle": {"2024": 40},  # 10 years in CNSS
                    "cnrps_salaire_de_base": {"2024": 1000},
                }
            }
        },
    )

    taux = sim.calculate("cnrps_taux_de_liquidation", "2024")[0]

    # Proratisation should be 1.0 (since cnrps_duree >= required 60)
    brute = sim.calculate("cnrps_pension_brute", "2024")[0]
    print(f"Pension brute (Séparée): {brute}")

    # The base pension should be 1000 * taux without any proratisation
    ref_salary = sim.calculate("cnrps_salaire_de_reference", "2024")[0]
    expected_brute = ref_salary * taux * 1.0
    assert math.isclose(brute, expected_brute, abs_tol=1e-5)


if __name__ == "__main__":
    test_coordination_cnss_cnrps()
    test_liquidation_separee()
    print("All Coordination tests passed!")
