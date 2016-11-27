# -*- coding: utf-8 -*-

from numpy import datetime64


from openfisca_tunisia.model.base import *


class idmen(Variable):
    column = IntCol(is_permanent = True)
    entity = Individu
    # 600001, 600002,


class idfoy(Variable):
    column = IntCol(is_permanent = True)
    entity = Individu
    # idmen + noi du déclarant


class quimen(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity = Individu


class quifoy(Variable):
    column = EnumCol(QUIFOY, is_permanent = True)
    entity = Individu


class age(Variable):
    column = AgeCol(val_type = "age")
    entity = Individu
    label = u"Âge (en années)"

    def function(self, simulation, period):
        date_naissance = simulation.get_array('date_naissance', period)
        return period, (datetime64(period.date) - date_naissance).astype('timedelta64[Y]')


class date_naissance(Variable):
    column = DateCol(default = date(1970, 1, 1))
    entity = Individu
    is_permanent = True
    label = u"Date de naissance"


class male(Variable):
    column = BoolCol()
    entity = Individu
    label = u"Mâle"


class marie(Variable):
    column = BoolCol
    entity = Individu
    label = u"Marié(e)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)

        return period, (statut_marital == 1)


class celibataire(Variable):
    column = BoolCol
    entity = Individu
    label = u"Célibataire"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)

        return period, (statut_marital == 2)


class divorce(Variable):
    column = BoolCol
    entity = Individu
    label = u"Divorcé(e)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)
        return period, (statut_marital == 3)


class veuf(Variable):
    column = BoolCol
    entity = Individu
    label = u"Veuf(ve)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)
        return period, statut_marital == 4


class statut_marital(Variable):
    column = PeriodSizeIndependentIntCol(default = 2)
    entity = Individu
