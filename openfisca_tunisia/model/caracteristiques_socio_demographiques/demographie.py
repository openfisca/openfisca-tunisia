# -*- coding: utf-8 -*-

from numpy import datetime64


from openfisca_tunisia.model.base import *


class age(Variable):
    column = AgeCol(val_type = "age")
    entity = Individu
    label = u"Âge (en années)"
    definition_period = YEAR

    def function(individu, period):
        date_naissance = individu('date_naissance', period)
        return (datetime64(period.date) - date_naissance).astype('timedelta64[Y]')


class date_naissance(Variable):
    column = DateCol(default = date(1970, 1, 1))
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY


class male(Variable):
    column = BoolCol()
    entity = Individu
    label = u"Mâle"
    definition_period = ETERNITY


class marie(Variable):
    column = BoolCol
    entity = Individu
    label = u"Marié(e)"
    definition_period = YEAR

    def function(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 1)


class celibataire(Variable):
    column = BoolCol
    entity = Individu
    label = u"Célibataire"
    definition_period = YEAR

    def function(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 2)


class divorce(Variable):
    column = BoolCol
    entity = Individu
    label = u"Divorcé(e)"
    definition_period = YEAR

    def function(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 3)


class veuf(Variable):
    column = BoolCol
    entity = Individu
    label = u"Veuf(ve)"
    definition_period = YEAR

    def function(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return statut_marital == 4


class statut_marital(Variable):
    column = IntCol(default = 2)
    entity = Individu
    label = u"Statut marital"
    definition_period = ETERNITY


class invalide(Variable):
    column = BoolCol
    label = u"Invalide"
    entity = Individu
    definition_period = ETERNITY


class activite(Variable):
    column = IntCol
    entity = Individu
    label = u"Activité"
    definition_period = ETERNITY



class boursier(Variable):
    column = BoolCol()
    entity = Individu
    definition_period = ETERNITY


