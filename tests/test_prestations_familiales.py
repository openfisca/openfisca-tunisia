from openfisca_tunisia.model.base import *
from openfisca_tunisia.scenarios import init_single_entity
from tests import base

import datetime


def test_contribution_frais_creche():
    year = 2011
    month = '2011-01'
    simulation = init_single_entity(
        base.tax_benefit_system.new_scenario(),
        period = year,
        parent1 = dict(age = 40),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        enfants = [
            dict(
                # id = 'Behija',
                date_naissance = '1992-01-01',
                ),
            dict(
                # id = 'Hassen',
                date_naissance = '2002-01-01',
                ),
            dict(
                # id = 'Thoura',
                date_naissance = '2008-12-31',
                )
            ]
        ).new_simulation(debug = True)

    ages_en_mois = simulation.menage.members('age_en_mois', period = month)
    age_benjamin = simulation.menage.min(ages_en_mois)[0]
    assert age_benjamin == 24
    assert age_benjamin <= base.tax_benefit_system.parameters(year).prestations_familiales.creche.age_max

    contribution_frais_creche = simulation.calculate('contribution_frais_creche', period = year)
    assert contribution_frais_creche != 0


if __name__ == '__main__':
    test_contribution_frais_creche()
