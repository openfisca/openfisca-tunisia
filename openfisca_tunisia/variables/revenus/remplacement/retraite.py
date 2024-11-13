from openfisca_tunisia.variables.base import *


# Pensions de retraite

class pension(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class revenu_assimile_pension(Variable):
    value_type = float
    label = 'Revenus assimilés à des pensions (pensions et rentes viagères)'
    entity = Individu
    definition_period = YEAR

    def formula(individu, period):
        return individu('pension', period, options = [ADD])


class avantages_nature_assimile_pension(Variable):
    value_type = float
    label = 'Avantages en nature assimilables à des pensions'
    entity = Individu
    definition_period = YEAR
