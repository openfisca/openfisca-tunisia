from openfisca_tunisia.variables.base import *


# Pensions


class pension_cnss(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pension_cnrps(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pension_de_retraite(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pension_orphelin(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pension_d_invalidite(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pension(Variable):
    value_type = float
    label = 'Pension'
    entity = Individu
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return (
            individu('pension_de_retraite', period, options = [ADD])
            + individu('pension_d_invalidite', period, options = [ADD])
            + individu('pension_orphelin', period, options = [ADD])
            )


class revenu_assimile_pension(Variable):
    value_type = float
    label = 'Revenus assimilés à des pensions (pensions et rentes viagères)'
    entity = Individu
    definition_period = YEAR

    def formula_2025_01(individu, period):
        return individu('pension_de_retraite', period, options = [ADD])

    def formula(individu, period):
        return individu('pension', period, options = [ADD])


class avantages_nature_assimile_pension(Variable):
    value_type = float
    label = 'Avantages en nature assimilables à des pensions'
    entity = Individu
    definition_period = YEAR
