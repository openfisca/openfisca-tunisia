# -*- coding: utf-8 -*-

from numpy import datetime64


from openfisca_tunisia.model.base import *


class age(Variable):
    value_type = int
    entity = Individu
    label = u"Âge (en années)"
    definition_period = YEAR
    is_period_size_independent = True
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        date_naissance = individu('date_naissance', period)
        return (datetime64(period.date) - date_naissance).astype('timedelta64[Y]')


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY


class male(Variable):
    value_type = bool
    entity = Individu
    label = u"Mâle"
    definition_period = ETERNITY


class marie(Variable):
    value_type = bool
    entity = Individu
    label = u"Marié(e)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 1)


class celibataire(Variable):
    value_type = bool
    entity = Individu
    label = u"Célibataire"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 2)


class divorce(Variable):
    value_type = bool
    entity = Individu
    label = u"Divorcé(e)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return (statut_marital == 3)


class veuf(Variable):
    value_type = bool
    entity = Individu
    label = u"Veuf(ve)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu('statut_marital', period = period)
        return statut_marital == 4


class statut_marital(Variable):
    value_type = int
    default_value = 2
    entity = Individu
    label = u"Statut marital"
    definition_period = ETERNITY


class invalide(Variable):
    value_type = bool
    label = u"Invalide"
    entity = Individu
    definition_period = ETERNITY


class activite(Variable):
    value_type = int
    entity = Individu
    label = u"Activité"
    definition_period = ETERNITY



class boursier(Variable):
    value_type = bool
    entity = Individu
    definition_period = ETERNITY


