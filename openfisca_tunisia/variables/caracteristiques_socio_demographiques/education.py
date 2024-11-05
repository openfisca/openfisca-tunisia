from openfisca_tunisia.variables.base import *


class boursier(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR


class eleve(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR


class etudiant(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
