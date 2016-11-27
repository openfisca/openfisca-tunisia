# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class code_postal(Variable):
    column = PeriodSizeIndependentIntCol
    entity = Menage


class loyer(Variable):
    column = IntCol
    entity = Menage
    label = "loyer du logement"


class statut_occupation_logement(Variable):
    column = PeriodSizeIndependentIntCol
    entity = Menage
    label = "Statut d'occupation du logement"


