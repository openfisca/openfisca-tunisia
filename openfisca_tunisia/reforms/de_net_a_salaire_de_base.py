# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_tunisia.model.base import *


try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_de_base, individu, period):
    # We're not wanting to calculate salaire_imposable again, but instead manually set it as an input variable
    individu.get_holder('salaire_de_base').put_in_cache(salaire_de_base, period)

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Force recomputing of salaire_net_a_payer
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays()
    net = temp_individu('salaire_net_a_payer', period)[0]

    return net


class salaire_de_base(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire de base"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        # Calcule le salaire de base à partir du salaire net par inversion numérique.
        net = individu.get_holder('salaire_net_a_payer').get_array(period)

        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period
        def solve_func(net):
            def innerfunc(essai_salaire_de_base):
                return calculate_net_from(essai_salaire_de_base, individu, period) - net
            return innerfunc

        salaire_de_base_calcule = \
            fsolve(
                solve_func(net),
                net * 1,  # first guess
                xtol = 1 / 1000,  # précision au millime
                )

        return salaire_de_base_calcule


class de_net_a_salaire_de_base(Reform):
    name = u'Inversion du calcul brut -> net'

    def apply(self):
        self.update_variable(salaire_de_base)
