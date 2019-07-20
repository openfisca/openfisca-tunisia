# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_tunisia.model.base import Reform, Variable, Individu, MONTH, set_input_divide_by_period 


try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None

i=0

def calculate_net_from(salaire_de_base, individu, period, requested_variable_names):
    global i
    print(">>> ", i)
    i += 1

    # We're not wanting to calculate salaire_imposable again, 
    # but instead manually set it as an input variable
    print('requested_variable_names >>> ', requested_variable_names)
    
    ## print('salaire_de_base >>>', individu.get_holder('salaire_de_base').get_array(period))
    ## print('salaire_de_base', salaire_de_base)
    ###  individu.get_holder('salaire_de_base').set_input(period, salaire_de_base)

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu
    temp_individu.get_holder('salaire_de_base').delete_arrays(period)
    temp_individu.get_holder('salaire_de_base').set_input(period, salaire_de_base)

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder(name).delete_arrays()
        temp_simulation.computation_stack = temp_simulation.computation_stack[-1:]
        print(temp_simulation.computation_stack)

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

        ### print("salaire_net_a_payer", individu.get_holder('salaire_net_a_payer').get_array(period))
        # print("assiette_cotisations_sociales", individu.get_holder('assiette_cotisations_sociales').get_array(period))
        # print("salaire_imposable", individu.get_holder('salaire_imposable').get_array(period))
        # print("salaire_de_base", individu.get_holder('salaire_de_base').get_array(period))
        net = individu.get_holder('salaire_net_a_payer').get_array(period)

        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period
        # List of variables already calculated. We will need it to remove their holders,
        # that might contain undesired cache
        ## requested_variable_names = list(simulation.requested_periods_by_variable_name.keys())
        requested_variable_names = [variable_period[0] for variable_period in simulation.computation_stack]
        print("requested_variable_names", requested_variable_names)
        print("simulation.computation_stack", simulation.computation_stack)
        if requested_variable_names:
            # requested_variable_names.remove('assiette_cotisations_sociales')
            # requested_variable_names.remove('salaire_imposable')
            requested_variable_names.remove('salaire_de_base')
            
        
        # Clean 'requested_periods_by_variable_name', that is used by -core to check for computation cycles.
        # avant : requested_periods_by_variable_name = {variable_name: [period1, period2]}
        # maintenant : computation_stack = [('variable_name', 'period1'), ('variable_name', 'period2')]



        # This variable, salaire_imposable, might have been called from variable X,
        # that will be calculated again in our iterations to compute the salaire_net requested
        # as an input variable, hence producing a cycle error
        simulation.requested_periods_by_variable_name = dict()

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
    name = u'Inversion du calcul brut (salaire_de_base) -> net'

    def apply(self):
        self.update_variable(salaire_de_base)
