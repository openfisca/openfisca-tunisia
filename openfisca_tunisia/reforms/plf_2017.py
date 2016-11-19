# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation


def modify_legislation_json(reference_legislation_json_copy):
    reform_year = 2016
    reform_period = periods.period('year', reform_year)

    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'ir', 'children', 'bareme', 'brackets', 3, 'rate'),
        period = reform_period,
        value = .27,
        )
    return reference_legislation_json_copy


class plf_2017(Reform):
    name = u'Projet de Loi de Finances 2017 appliquée aux revenus 2016'
    key = 'plf_2017'

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)
