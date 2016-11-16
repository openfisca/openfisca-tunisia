# -*- coding: utf-8 -*-

from numpy import datetime64


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


class age(Variable):
    column = AgeCol(val_type = "age")
    entity_class = Individus
    label = u"Âge (en années)"

    def function(self, simulation, period):
        date_naissance = simulation.get_array('date_naissance', period)
        if date_naissance is None:
            age_en_mois = simulation.get_array('age_en_mois', period)
            if age_en_mois is not None:
                return period, age_en_mois // 12
            date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.date) - date_naissance).astype('timedelta64[Y]')


class age_en_mois(Variable):
    column = AgeCol(val_type = "months")
    entity_class = Individus
    label = u"Âge (en mois)"

    def function(self, simulation, period):
        date_naissance = simulation.get_array('date_naissance', period)
        if date_naissance is None:
            age = simulation.get_array('age', period)
            if age is not None:
                return period, age * 12
            date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.date) - date_naissance).astype('timedelta64[M]')


class date_naissance(Variable):
    column = DateCol(is_permanent = True)
    entity_class = Individus
    label = u"Année de naissance"


class statut_marital(Variable):
    column = PeriodSizeIndependentIntCol(default = 2)
    entity_class = Individus


class chef_de_famille(Variable):
    column = BoolCol()
    entity_class = Individus
    # Du point de vue fiscal, est considéré chef de famille :
    # - L’époux ;
    # - Le divorcé ou la divorcée qui a la garde des enfants ;
    # - Le veuf ou la veuve même sans enfants à charge ;
    # - L’adoptant ou l’adoptante.
    # Cependant, l’épouse a la qualité de chef de famille dans les deux cas suivants :
    # - Lorsqu’elle justifie que le mari ne dispose d’aucune source de revenu durant l’année de réalisation du
    #   revenu. Tel est le cas d’une femme qui dispose d’un revenu et dont le mari, poursuivant des études, ne dispose
    #   d’aucun revenu propre.
    # - Lorsque remariée, elle a la garde d’enfants issus d’un précédent mariage.
    # Compte tenu de ce qui précède, n’est pas considéré comme chef de famille et ne bénéficie d’aucune déduction :
    # - Le célibataire ou la célibataire ;
    # - Le divorcé ou la divorcée qui n’a pas la garde des enfants ;
    # - La femme durant le mariage (sauf si elle dispose d’un revenu alors que son mari ne dispose d’aucun revenu) ;
    # - L’époux qui ne dispose pas d’une source de revenu. Dans ce cas, l’épouse acquiert la qualité de chef de famille
    #   au cas où elle réalise des revenus.
