from openfisca_tunisia.variables.base import *

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_imposable, individu, period):
    # Work in isolation just like the similar function in
    # de_net_a_salaire_de_base.py. Clone the simulation so that
    # computations do not pollute the original state.
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above).
    # We delete arrays for *all* variables that have a formula, which
    # mirrors the behaviour added in the salaire_de_base reform.
    for name in temp_simulation.tax_benefit_system.variables.keys():
        try:
            pop = temp_simulation.get_variable_population(name)
            holder = pop.get_holder(name)
            # Only delete arrays if the variable is calculated (formula exists)
            if holder.variable.formulas:
                holder.delete_arrays()
        except Exception:
            pass

    # Clean 'computation_stack', that is used by -core to check for computation cycles.
    temp_simulation.computation_stack = []

    temp_individu.get_holder("salaire_imposable").set_input(period, salaire_imposable)
    net = temp_individu("salaire_net_a_payer", period)[0]

    return net


class salaire_imposable(Variable):
    value_type = float
    entity = Individu
    label = "Salaire imposable"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        # Use numerical inversion to calculate 'salaire_imposable' from 'salaire_net_a_payer'
        net = individu.get_holder("salaire_net_a_payer").get_array(period)
        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period

        # There is no need to track already calculated variables any
        # more: the helper above clears every calculated tier, just as in
        # de_net_a_salaire_de_base.

        def solve_func(net):
            def innerfunc(essai):
                calc = calculate_net_from(essai, individu, period)
                diff = calc - net
                # keep a minimal debug print comparable to the salary_de_base
                print(f"fsolve debug: essai={essai}, calc_net={calc}, diff={diff}")
                return diff

            return innerfunc

        imposable_calcule = fsolve(
            solve_func(net),
            net * 1.25,  # keep the historical heuristic initial guess
            xtol=1 / 100,  # précision
        )

        return imposable_calcule


class de_net_a_imposable(Reform):
    name = "Inversion du calcul imposable -> net"

    def apply(self):
        self.update_variable(salaire_imposable)
