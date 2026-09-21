# Third Party
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_depart_anticipe():
    system = TunisiaPensionTaxBenefitSystem()
    builder = SimulationBuilder()

    # Simulate a person: mere de 3 enfants
    sim = builder.build_from_entities(
        system,
        {
            "individus": {
                "mere": {
                    "age": {"2024": 52},
                    "cnrps_duree_assurance": {"2024": 65},  # > 15 ans
                    "mere_3_enfants": {"2024": True},
                    "cnrps_salaire_de_base": {"2024": 1000},
                }
            }
        },
    )

    assert sim.calculate("cnrps_eligible", "2024")[0]
    print("Mothers of 3 test passed!")

    # Simulate normal person
    sim2 = builder.build_from_dict(
        system,
        {
            "individus": {
                "normal": {
                    "age": {"2024": 52},
                    "cnrps_duree_assurance": {"2024": 65},
                    "mere_3_enfants": {"2024": False},
                    "cnrps_salaire_de_base": {"2024": 1000},
                }
            }
        },
    )

    assert not sim2.calculate("cnrps_eligible", "2024")[0]
    print("Normal person test passed!")


if __name__ == "__main__":
    test_depart_anticipe()
