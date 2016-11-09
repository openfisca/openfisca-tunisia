# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class code_postal(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Menages


class loyer(Variable):
    column = IntCol
    entity_class = Menages
    label = "loyer du logement"


class statut_occupation_logement(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Menages
    label = "Statut d'occupation du logement"


