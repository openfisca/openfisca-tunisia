# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation


def modify_legislation_json(reference_legislation_json_copy):
    reform_year = 2017
    reform_legislation_subtree = {
        '@type': 'Scale',
        'description': "Tranches de l'IR",
        'brackets': [
            {
                'threshold': [{'start': u'2017-01-01'}, {'value': 0.0}],
                'rate': [{'start': u'2017-01-01'}, {'value': 0.0}],
                },
            {
                'threshold': [{'start': u'2017-01-01'}, {'value': 5000}],
                'rate': [{'start': u'2017-01-01'}, {'value': 0.27}],
                },
            {
                'threshold': [{'start': u'2017-01-01'}, {'value': 25000}],
                'rate': [{'start': u'2017-01-01'}, {'value': .30}],
                },
            {
                'threshold': [{'start': u'2017-01-01'}, {'value': 50000}],
                'rate': [{'start': u'2017-01-01'}, {'value': 0.35}],
                },
            ],
        }

    reference_legislation_json_copy['children']['impot_revenu']['children']['bareme'] = reform_legislation_subtree
    return reference_legislation_json_copy


class plf_2017(Reform):
    name = u'Projet de Loi de Finances 2017 appliquée aux revenus 2016'
    key = 'plf_2017'

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)
