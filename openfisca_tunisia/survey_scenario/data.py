from openfisca_tunisia.variables.base import *


class poids(Variable):
    value_type = float
    entity = Individu
    label = "Poids de l'individu dans l'enquête"
    definition_period = YEAR
    is_period_size_independent = True
    default_value = 1


class poids_menage(Variable):
    value_type = float
    entity = Menage
    label = "Poids du ménage dans l'enquête"
    definition_period = YEAR
    is_period_size_independent = True
    default_value = 1


class poids_foyer_fiscal(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Poids du foyer fiscal dans l'enquête"
    definition_period = YEAR
    is_period_size_independent = True
    default_value = 1
