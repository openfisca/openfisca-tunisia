# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime

import numpy as np
import openfisca_tunisia


TaxBenefitSystem = openfisca_tunisia.init_country()
tax_benefit_system = TaxBenefitSystem()


def check_1_parent(year = 2013):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    simulation.calculate('revdisp')
    sali = simulation.get_holder('sali').new_test_case_array()
    assert (sali - np.linspace(0, 100000, 3)).all() == 0, sali


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
