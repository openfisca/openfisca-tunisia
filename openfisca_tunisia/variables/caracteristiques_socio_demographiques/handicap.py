from openfisca_tunisia.variables.base import *


class invalide(Variable):
    value_type = bool
    label = 'Invalide (handicap lourd)'
    entity = Individu
    definition_period = ETERNITY
