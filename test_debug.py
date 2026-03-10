from openfisca_core.simulations import SimulationBuilder
from openfisca_tunisia import CountryTaxBenefitSystem
system = CountryTaxBenefitSystem()
builder = SimulationBuilder()
test_case = {
    'individus': {'parent1': {}},
    'foyers_fiscaux': {'foyer1': {
        'declarants': ['parent1'], 
        'acomptes_provisionnels_payes': {'2021': 2000.0}, 
        'retenues_source_payees': {'2021': 3000.0}, 
        'credit_impot_etranger': {'2021': 500.0}, 
        'impot_total_du': {'2021': 10000.0}
    }}
}
sim = builder.build_from_entities(system, test_case)
try:
    print('Acomptes:', sim.calculate('acomptes_provisionnels_payes', '2021'))
    print('Retenues:', sim.calculate('retenues_source_payees', '2021'))
    print('Crédits etrangers:', sim.calculate('credit_impot_etranger', '2021'))
    print('Total credits:', sim.calculate('total_credits_impot', '2021'))
    print('IRPP brut calcule:', sim.calculate('irpp', '2021'))
    print('IRPP Net a Payer:', sim.calculate('irpp_net_a_payer', '2021'))
except Exception as e:
    import traceback
    traceback.print_exc()
