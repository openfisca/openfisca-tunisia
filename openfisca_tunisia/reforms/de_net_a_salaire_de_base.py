from openfisca_tunisia.variables.base import (
    Individu,
    MONTH,
    Reform,
    set_input_divide_by_period,
    Variable,
)

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_de_base, individu, period):
    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
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

    temp_individu.get_holder("salaire_de_base").set_input(period, salaire_de_base)
    net = temp_individu("salaire_net_a_payer", period)[0]

    return net


class salaire_de_base(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de base"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        # Use numerical inversion to calculate 'salaire_de_base' from 'salaire_net_a_payer'
        net = individu.get_holder("salaire_net_a_payer").get_array(period)

        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period

        def solve_func(net):
            def innerfunc(essai_salaire_de_base):
                calc_net = calculate_net_from(
                    essai_salaire_de_base,
                    individu,
                    period,
                )
                diff = calc_net - net
                print(
                    f"fsolve debug: essai={essai_salaire_de_base}, calc_net={calc_net}, diff={diff}"
                )
                return diff

            return innerfunc

        salaire_de_base_calcule = fsolve(
            solve_func(net),
            net * 1,  # first guess
            xtol=1 / 1000,  # précision au millime
        )

        return salaire_de_base_calcule


class de_net_a_salaire_de_base(Reform):
    name = "Inversion du calcul brut (salaire_de_base) -> net"

    def apply(self):
        self.update_variable(salaire_de_base)
