from openfisca_tunisia.variables.base import *


# Salaires


class salaire_de_base(Variable):
    value_type = float
    label = 'Salaire de base'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class primes(Variable):
    value_type = float
    label = 'Primes'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class salaire_en_nature(Variable):
    value_type = float
    label = 'Avantages en nature assimilables à des salaires'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class smig_dec(Variable):
    value_type = bool
    label = 'Salarié déclarant percevoir le SMIG ou le SMAG'
    entity = Individu
    definition_period = MONTH
