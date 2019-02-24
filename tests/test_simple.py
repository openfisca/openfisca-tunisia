# -*- coding: utf-8 -*-


from tests.base import tax_benefit_system
from openfisca_tunisia.scenarios import init_single_entity


def test_simple():
    year = 2011
    simulation = init_single_entity(
        tax_benefit_system.new_scenario(),
        period = year,
        parent1 = dict(age = 40),
        ).new_simulation(debug = True)
    assert simulation.calculate('revenu_disponible', period = year) == 0


if __name__ == '__main__':
    test_simple()
