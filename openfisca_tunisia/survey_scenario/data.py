# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class poids(Variable):
    value_type = float
    entity = Individu
    label = u"Poids de l'individu"
    definition_period = YEAR
    is_period_size_independent = True
    default_value = 1


class poids_menage(Variable):
    value_type = float
    entity = Menage
    label = u"Poids du ménage"
    definition_period = YEAR
    is_period_size_independent = True


class poids_foyer_fiscal(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Poids du foyer fiscal"
    definition_period = YEAR
    is_period_size_independent = True

