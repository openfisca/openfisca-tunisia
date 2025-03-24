from openfisca_tunisia.variables.base import *


# class TypesHandicap(Enum):
#     __order__ = 'neant leger intermediaire lourd'
#     # Needed to preserve the enum order in Python 2
#     neant = 'Néant'
#     leger = 'Léger'
#     intermediaire = 'Intermédiaire'
#     lourd = 'Lourd'


# class handicap(Variable):
#     value_type = Enum
#     possible_values = TypesHandicap
#     default_value = TypesHandicap.neant
#     label = 'Niveau de handicap'
#     entity = Individu
#     definition_period = ETERNITY


class handicap(Variable):
    value_type = int
    default_value = 0
    label = 'Niveau de handicap (0-Néant, 1-Léger, 2-Intermédiraire, 3-Lourd)'
    entity = Individu
    definition_period = ETERNITY
