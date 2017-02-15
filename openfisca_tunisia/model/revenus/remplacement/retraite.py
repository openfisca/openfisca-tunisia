# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Pensions de retraite

class revenu_assimile_pension(Variable):
    column = IntCol
    label = u"Revenus assimilés à des pensions (pensions et rentes viagères)"
    entity = Individu


class avantages_nature_assimile_pension(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des pensions"
    entity = Individu

