from __future__ import division
from openfisca_tunisia.model.base import Reform, Variable, Individu, MONTH, set_input_divide_by_period 


try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_de_base, individu, period, requested_variable_names):
    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder(name).delete_arrays(period)

    # Clean 'computation_stack', that is used by -core to check for computation cycles.
    # The variable 'salaire_imposable' might have been called from variable X,
    # that will be calculated again in our iterations to compute the 'salaire_net_a_payer'
    # requested as an input variable, hence producing a cycle error
    temp_simulation.computation_stack = []

    temp_individu.get_holder('salaire_de_base').set_input(period, salaire_de_base)

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
        # Use numerical inversion to calculate 'salaire_de_base' from 'salaire_net_a_payer'
        net = individu.get_holder('salaire_net_a_payer').get_array(period)

        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period

        # List of variables already calculated. 
        # We will need it to remove their holders, that might contain undesired cache
        requested_variable_names = [variable_period[0] for variable_period in simulation.computation_stack]

        def solve_func(net):
            def innerfunc(essai_salaire_de_base):
                return calculate_net_from(essai_salaire_de_base, individu, period, requested_variable_names) - net
            return innerfunc

        salaire_de_base_calcule = \
            fsolve(
                solve_func(net),
                net * 1,  # first guess
                xtol = 1 / 1000,  # précision au millime
                )

        return salaire_de_base_calcule


class de_net_a_salaire_de_base(Reform):
    name = 'Inversion du calcul brut (salaire_de_base) -> net'

    def apply(self):
        self.update_variable(salaire_de_base)
