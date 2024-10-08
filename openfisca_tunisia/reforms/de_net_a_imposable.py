from __future__ import division

from openfisca_tunisia.model.base import *

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_imposable, individu, period, requested_variable_names):
    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder(name).delete_arrays(period)

    # We're not wanting to calculate salaire_imposable again,
    # but instead manually set it as an input variable
    temp_individu.get_holder('salaire_imposable').set_input(period, salaire_imposable)

    # Force recomputing of salaire_net_a_payer
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays(period)
    net = temp_individu('salaire_net_a_payer', period)[0]

    return net


class salaire_imposable(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire imposable'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        # Use numerical inversion to calculate 'salaire_imposable' from 'salaire_net_a_payer'
        net = individu.get_holder('salaire_net_a_payer').get_array(period)
        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period

        # List of variables already calculated.
        # We will need it to remove their holders, that might contain undesired cache
        requested_variable_names = [stack_frame['name'] for stack_frame in individu.simulation.tracer.stack]

        def solve_func(net):
            def innerfunc(essai):
                return calculate_net_from(essai, individu, period, requested_variable_names) - net
            return innerfunc

        imposable_calcule = \
            fsolve(
                solve_func(net),
                net * 1.25,  # on entend souvent parler cette méthode...
                xtol = 1 / 100  # précision
                )

        return imposable_calcule


class de_net_a_imposable(Reform):
    name = 'Inversion du calcul imposable -> net'

    def apply(self):
        self.update_variable(salaire_imposable)
