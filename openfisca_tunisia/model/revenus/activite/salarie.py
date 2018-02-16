# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Salaires


class salaire_de_base(Variable):
    value_type = float
    label = u"Salaire de base"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class primes(Variable):
    value_type = float
    label = u"Primes"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class salaire_en_nature(Variable):
    value_type = float
    label = u"Avantages en nature assimilables à des salaires"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class smig_dec(Variable):
    value_type = bool
    label = u"Salarié déclarant percevoir le SMIG ou le SMAG"
    entity = Individu
    definition_period = MONTH
