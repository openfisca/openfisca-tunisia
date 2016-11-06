# -*- coding: utf-8 -*-


from openfisca_tunisia.tests.base import tax_benefit_system


def test_simple():
    year = 2011
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(agem = 40 * 12 + 6),
        ).new_simulation(debug = True)
    assert simulation.calculate('revenu_disponible') == 0


if __name__ == '__main__':
    test_simple()
