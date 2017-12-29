# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import periods
from openfisca_core.reforms import Reform


def modify_parameters(parameters):
    reform_year = 2016
    reform_period = periods.period(reform_year)

    parameters.impot_revenu.bareme[3].rate.update(
        period = reform_period,
        value = .27,
        )
    return parameters


class plf_2017(Reform):
    name = u'Projet de Loi de Finances 2017 appliquée aux revenus 2016'
    key = 'plf_2017'

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
