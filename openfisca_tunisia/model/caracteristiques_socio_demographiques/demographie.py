# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


class idmen(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # 600001, 600002,


class idfoy(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # idmen + noi du déclarant


class quimen(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity_class = Individus


class quifoy(Variable):
    column = EnumCol(QUIFOY, is_permanent = True)
    entity_class = Individus


class date_naissance(Variable):
    column = DateCol(is_permanent = True)
    entity_class = Individus
    label = u"Année de naissance"


class statut_marital(Variable):
    column = PeriodSizeIndependentIntCol(default = 2)
    entity_class = Individus


class chef(Variable):
    column = BoolCol()
    entity_class = Individus
