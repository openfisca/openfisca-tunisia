# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_bonifications_cadre_actif():
    system = TunisiaPensionTaxBenefitSystem()
    builder = SimulationBuilder()

    # Simulate a person: Cadre actif with 35 years of service
    sim = builder.build_from_entities(
        system,
        {
            "individus": {
                "actif_35": {
                    "age": {"2024": 55},
                    "duree_service_cadre_actif": {"2024": 35},
                    "cnrps_duree_assurance_annuelle": {
                        "2024": 140
                    },  # 35 ans en trimestres
                }
            }
        },
    )

    # They should get 5 years bonus (20 trimesters)
    res_bonif = sim.calculate("cnrps_bonifications", "2024")[0]
    print(f"Cadre actif bonifications result: {res_bonif}")
    assert res_bonif == 20
    assert sim.calculate("cnrps_duree_assurance", "2024")[0] == 160  # 140 + 20
    print("Cadre Actif (35y) test passed!")

    # Simulate a person: Militaire with 25 years of service
    sim2 = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "militaire_25": {
                    "age": {"2024": 55},
                    "duree_service_militaire": {"2024": 25},
                    "cnrps_duree_assurance_annuelle": {
                        "2024": 100
                    },  # 25 ans en trimestres
                }
            }
        },
    )

    # They should get 5 years bonus (20 trimesters) too
    res2_bonif = sim2.calculate("cnrps_bonifications", "2024")[0]
    print(f"Military bonifications result: {res2_bonif}")
    assert res2_bonif == 20
    assert sim2.calculate("cnrps_duree_assurance", "2024")[0] == 120  # 100 + 20
    print("Militaire (25y) test passed!")


if __name__ == "__main__":
    test_bonifications_cadre_actif()
