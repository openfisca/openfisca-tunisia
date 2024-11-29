'''Aide médicale gratuite.'''


from openfisca_tunisia.variables.base import *


class amg1(Variable):
    value_type = bool
    entity = Menage
    label = 'Aide médicale gratuite - AMG1'
    definition_period = MONTH


class amg2(Variable):
    value_type = bool
    entity = Menage
    label = 'Programme d’assistance médicale à tarifs réduits - AMG2'
    definition_period = MONTH
