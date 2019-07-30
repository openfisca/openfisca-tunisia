import pytest
import datetime

from openfisca_tunisia.model.base import *
from openfisca_tunisia.scenarios import init_single_entity


scenarios_arguments = [
    dict(
        period = year,
        parent1 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            regime_securite_sociale = 'rsna',
            ),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        )
    for year in range(2012, 2007, -1)
    ]


def check_run(simulation, period):
    assert simulation.calculate('revenu_disponible', period = period) is not None, \
        "Can't compute revenu_disponible on period {}".format(period)
    assert simulation.calculate_add('salaire_super_brut', period = period) is not None, \
        "Can't compute salaire_super_brut on period {}".format(period)


@pytest.mark.parametrize('one_scenario_arguments', scenarios_arguments)
def test_basics(one_scenario_arguments):
    scenario = init_single_entity(
        base.tax_benefit_system.new_scenario(),
        **one_scenario_arguments
        )
    simulation = scenario.new_simulation(debug = False)
    period = one_scenario_arguments['period']
    check_run(simulation, period)
