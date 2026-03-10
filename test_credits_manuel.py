from openfisca_core.simulations import SimulationBuilder
from openfisca_tunisia import CountryTaxBenefitSystem

system = CountryTaxBenefitSystem()
builder = SimulationBuilder()

test_case = {
    "individus": {
        "parent1": {
            "retenues_source_payees": {"2021": 3000.0},
            "credit_impot_etranger": {"2021": 500.0}
        }
    },
    "foyers_fiscaux": {
        "foyer1": {
            "declarants": ["parent1"],
            "acomptes_provisionnels_payes": {"2021": 2000.0},
            "impot_total_du": {"2021": 10000.0}
        }
    }
}

sim = builder.build_from_entities(system, test_case)

try:
    print('Impôt total :', sim.calculate('impot_total_du', '2021')[0])
    print('Crédits retenues :', sim.calculate('retenues_source_payees', '2021')[0])
    print('Crédits accomptes :', sim.calculate('acomptes_provisionnels_payes', '2021')[0])
    print('Crédits etrangers :', sim.calculate('credit_impot_etranger', '2021')[0])
    print('Total crédits (FF) :', sim.calculate('total_credits_impot', '2021')[0])
    print('IRPP net à payer (FF) :', sim.calculate('irpp_net_a_payer', '2021')[0])
except Exception as e:
    import traceback
    traceback.print_exc()
