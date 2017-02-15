# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Salaires


class salaire_de_base(Variable):
    column = FloatCol
    label = u"Salaire de base"
    entity = Individu


class primes(Variable):
    column = FloatCol
    label = u"Primes"
    entity = Individu


class salaire_en_nature(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des salaires"
    entity = Individu


class smig_dec(Variable):
    column = BoolCol
    label = u"Salarié déclarant percevoir le SMIG ou le SMAG"
    entity = Individu
