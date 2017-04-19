# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class code_postal(Variable):
    column = PeriodSizeIndependentIntCol
    entity = Menage
    label = u"Localisation du logement (code postal)"


class loyer(Variable):
    column = IntCol
    entity = Menage
    label = u"Loyer du logement"


class statut_occupation_logement(Variable):
    column = PeriodSizeIndependentIntCol
    entity = Menage
    label = u"Statut d'occupation du logement"


