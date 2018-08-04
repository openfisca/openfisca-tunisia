from openfisca_tunisia.model.base import *
from openfisca_tunisia.model.prestations_familiales import age_en_mois_benjamin
from tests import base

import datetime
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def test_age_en_mois_benjamin():
    year = 2011
    month = '2011-01'
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(age = 40),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        enfants = [
            dict(
                date_naissance = '1992-01-01',
                ),
            dict(
                date_naissance = '2002-01-01',
                ),
            ],
        ).new_simulation(debug = True)

    ages_en_mois = simulation.menage.members('age_en_mois', period = month)
    assert age_en_mois_benjamin(ages_en_mois) == 107


if __name__ == '__main__':
    test_age_en_mois_benjamin()



