# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013 OpenFisca Team
# https://github.com/openfisca/openfisca
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

import openfisca_tunisia
openfisca_tunisia.init_country()

from openfisca_core.simulations import ScenarioSimulation


def test_case(year):
    simulation = ScenarioSimulation()
    simulation.set_config(year = year, reforme=False, nmen = 3, maxrev = 12*400, x_axis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime.date(1975,1,1), 'conj', 'part')

    simulation.scenario.addIndiv(2, datetime.date(2000,1,1), 'pac', 'enf')
    simulation.scenario.addIndiv(3, datetime.date(2000,1,1), 'pac', 'enf')

    simulation.set_param()
    df = simulation.get_results_dataframe()
    print df.to_string()

    # Save example to excel
    # destination_dir = "c:/users/utilisateur/documents/"
    # fname = "Example_%s.%s" %(str(yr), "xls")
    # df.to_excel(destination_dir = destination_dir + fname)


if __name__ == '__main__':
    test_case(2011)

