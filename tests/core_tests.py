# -*- coding: utf-8 -*-


import datetime

from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.scenarios import init_single_entity


tax_benefit_system = TunisiaTaxBenefitSystem()


def check_1_parent(year = 2011):
    scenario = init_single_entity(
        tax_benefit_system.new_scenario(),
        axes = [dict(
            count = 3,
            name = 'salaire_imposable',
            max = 100000,
            min = 0,
            )],
        period = year,
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        )
    simulation = scenario.new_simulation()
    revenu_disponible = simulation.calculate('revenu_disponible', period = year)


def test_1_parent():
    for year in range(2009, 2011):
        yield check_1_parent, year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_1_parent()
#     test_1_parent_2_enfants()
#     test_1_parent_2_enfants_1_column()
