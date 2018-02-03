# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class poids(Variable):
    default_value = 1
    is_period_size_independent = True
    value_type = float
    entity = Individu
    label = u"Poids de l'individu"
    definition_period = YEAR


class poids_menage(Variable):
    is_period_size_independent = True
    value_type = float
    entity = Menage
    label = u"Poids du ménage"
    definition_period = YEAR


class poids_foyer_fiscal(Variable):
    is_period_size_independent = True
    value_type = float
    entity = FoyerFiscal
    label = u"Poids du foyer fiscal"
    definition_period = YEAR

