# -*- coding: utf-8 -*-


import datetime


from openfisca_tunisia.model.base import tax_benefit_system


def test_age_from_agem():
    year = 2011
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(agem = 40 * 12 + 6),
        ).new_simulation(debug = True)
    assert simulation.calculate('age') == 40


def test_age_from_birth():
    year = 2011
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    assert simulation.calculate('age') == 40
    assert simulation.calculate('agem') == 40 * 12


def test_agem_from_age():
    year = 2011
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(age = 40),
        ).new_simulation(debug = True)
    assert simulation.calculate('agem') == 40 * 12


def test_agem_from_birth():
    year = 2011
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    assert simulation.calculate('agem') == 40 * 12
    assert simulation.calculate('age') == 40


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_age_from_agem()
    test_age_from_birth()
    test_agem_from_age()
    test_agem_from_birth()
