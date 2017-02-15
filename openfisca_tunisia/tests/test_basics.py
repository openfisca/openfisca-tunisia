# -*- coding: utf-8 -*-

from __future__ import division

import datetime

from openfisca_tunisia.model.data import CAT
from openfisca_tunisia.tests import base


scenarios_arguments = [
    dict(
        period = year,
        parent1 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            categorie_salarie = CAT['rsna'],
            ),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        )
    for year in range(2012, 2007, -1)
    ]


def check_run(simulation, period):
    assert simulation.calculate('revenu_disponible') is not None, "Can't compute revdisp on period {}".format(period)
    assert simulation.calculate('salaire_super_brut') is not None, \
        "Can't compute salaire_super_brut on period {}".format(period)


def test_basics():
    for scenario_arguments in scenarios_arguments:
        scenario = base.tax_benefit_system.new_scenario()
        scenario.init_single_entity(**scenario_arguments)
        simulation = scenario.new_simulation(debug = False)
        period = scenario_arguments['period']
        yield check_run, simulation, period


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    for _, simulation, period in test_basics():
        check_run(simulation, period)
    print u'OpenFisca-Tunisia basic test was executed successfully.'.encode('utf-8')
