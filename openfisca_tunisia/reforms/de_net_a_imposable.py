# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_tunisia.model.base import *
from numpy.ma.testutils import assert_not_equal
from urllib2 import Request

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None

from .. import entities


def calculate_net_from(salaire_imposable, individu, period, requested_variable_names):
    # We're not wanting to calculate salaire_imposable again, but instead manually set it as an input variable
    # To avoid possible conflicts, remove its function
    holder = individu.get_holder('salaire_imposable')
    holder.formula.function = None
    holder.array = salaire_imposable

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder(name).delete_arrays()

    # Force recomputing of salaire_net
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays()
    net = temp_individu('salaire_net_a_payer', period)[0]

    return net


class salaire_imposable(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire imposable"
    definition_period = MONTH
    set_input = set_input_divide_by_period


    def formula(individu, period):
        # Calcule le salaire brut à partir du salaire net par inversion numérique.
        net = individu.get_holder('salaire_net_a_payer').get_array(period)
        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period
        # List of variables already calculated. We will need it to remove their holders,
        # that might contain undesired cache
        requested_variable_names = simulation.requested_periods_by_variable_name.keys()
        if requested_variable_names:
            requested_variable_names.remove(u'salaire_imposable')
        # Clean 'requested_periods_by_variable_name', that is used by -core to check for computation cycles.
        # This variable, salaire_imposable, might have been called from variable X,
        # that will be calculated again in our iterations to compute the salaire_net requested
        # as an input variable, hence producing a cycle error
        simulation.requested_periods_by_variable_name = dict()

        def solve_func(net):
            def innerfunc(essai):
                return calculate_net_from(essai, individu, period, requested_variable_names) - net
            return innerfunc

        brut_calcule = \
            fsolve(
                solve_func(net),
                net * 1.25,  # on entend souvent parler cette méthode...
                xtol = 1 / 100  # précision
                )

        return brut_calcule


class de_net_a_imposable(Reform):
    name = u'Inversion du calcul brut -> net'

    def apply(self):
        self.update_variable(salaire_imposable)
