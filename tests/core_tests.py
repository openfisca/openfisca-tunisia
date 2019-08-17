import pytest
import datetime


from openfisca_tunisia.scenarios import init_single_entity


from tests.base import tax_benefit_system


@pytest.mark.parametrize('year', range(2009, datetime.date.today().year + 1))
def test_1_parent(year):
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
    simulation.calculate('revenu_disponible', period = year)
