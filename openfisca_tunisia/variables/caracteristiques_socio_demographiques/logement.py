from openfisca_tunisia.variables.base import *


class code_postal(Variable):
    value_type = int
    entity = Menage
    label = 'Localisation du logement (code postal)'
    definition_period = ETERNITY


class loyer(Variable):
    value_type = int
    entity = Menage
    label = 'Loyer du logement'
    definition_period = YEAR


class statut_occupation_logement(Variable):
    value_type = int
    entity = Menage
    label = "Statut d'occupation du logement"
    definition_period = YEAR
