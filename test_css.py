import datetime
import numpy as np

from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.scenarios import init_single_entity

tax_benefit_system = TunisiaTaxBenefitSystem()
year = 2018

scenario = init_single_entity(
    tax_benefit_system.new_scenario(),
    axes = [[
        dict(
            count = 3,
            name = 'salaire_imposable',
            max = 100000,
            min = 0,
            )
        ]],
    period = year,
    parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
    )
simulation = scenario.new_simulation()

salaire_imposable = simulation.calculate_add('salaire_imposable', year)
print("salaire_imposable", salaire_imposable)

irpp = simulation.calculate('irpp', period = year)
print("irpp", irpp)

# print(tax_benefit_system.parameters(year).prelevements_sociaux.contribution_sociale_solidarite.entreprise.montant_minimum)
# montant_entreprise = tax_benefit_system.parameters(year).prelevements_sociaux.contribution_sociale_solidarite.entreprise.montant_minimum
# taux = np.array([11, 31], dtype='int64')
# print(montant_entreprise.calc(taux))

contribution_sociale_solidarite = simulation.calculate_add('contribution_sociale_solidarite', year)
print("contribution_sociale_solidarite", contribution_sociale_solidarite)
print("contribution_sociale_solidarite", simulation.calculate_add('contribution_sociale_solidarite', 2017))
