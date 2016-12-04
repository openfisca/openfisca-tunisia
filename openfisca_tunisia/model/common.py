# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


class revenu_disponible_individuel(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenu disponible individuel"

    def function(individu, period):
        period = period.this_year
        revenus_du_travail = individu('revenus_du_travail', period = period)
        revenu_assimile_pension = individu('revenu_assimile_pension', period = period)
        revenus_du_capital = individu('revenus_du_capital', period = period)
        prestations_sociales = individu('prestations_sociales', period = period)
        impots_directs = individu('impots_directs', period = period)

        return period, revenus_du_travail + revenu_assimile_pension + revenus_du_capital + prestations_sociales + impots_directs


class revenu_disponible(Variable):
    column = FloatCol()
    entity = Menage
    label = u"Revenu disponible du ménage"

    def function(menage, period):
        period = period.this_year
        revenu_disponible_individuels = menage.members('revenu_disponible_individuel', period = period)
        return period, menage.sum(revenu_disponible_individuels)


class revenus_du_travail(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenu du travail"

    def function(individu, period):
        period = period.this_year
        salaire_imposable = individu('salaire_imposable', period = period)
        return period, salaire_imposable  # + beap + bic + bnc  TODO


class revenus_du_capital(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenus du capital"

    def function(individu, period):
        period = period.this_year
        revenus_fonciers = individu.foyer_fiscal('revenus_fonciers', period = period)

        return period, revenus_fonciers


class impots_directs(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Impôts directs"

    def function(individu, period):
        period = period.this_year
        irpp = individu.foyer_fiscal('irpp', period = period)

        return period, irpp
