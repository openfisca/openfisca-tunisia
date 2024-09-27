from openfisca_tunisia.model.base import *


# Pensions de retraite

class revenu_assimile_pension(Variable):
    value_type = int
    label = 'Revenus assimilés à des pensions (pensions et rentes viagères)'
    entity = Individu
    definition_period = YEAR


class avantages_nature_assimile_pension(Variable):
    value_type = int
    label = 'Avantages en nature assimilables à des pensions'
    entity = Individu
    definition_period = YEAR
