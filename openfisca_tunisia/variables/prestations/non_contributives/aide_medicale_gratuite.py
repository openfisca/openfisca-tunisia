'''Aide médicale gratuite.'''


from openfisca_tunisia.variables.base import *


class amg_1(Variable):
    value_type = bool
    entity = Menage
    label = 'Aide médicale gratuite pour les ménages pauvres - AMG1'
    definition_period = MONTH


class amg_2(Variable):
    value_type = bool
    entity = Menage
    label = 'Programme d’assistance médicale à tarifs réduits les ménages vulnérables - AMG2'
    definition_period = MONTH
