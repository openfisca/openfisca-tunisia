# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


class impots_directs(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Impôts directs"
    definition_period = YEAR

    def function(individu, period):
        irpp = individu.foyer_fiscal('irpp', period = period)

        return irpp


class prestations_sociales(Variable):
    column = IntCol
    entity = Individu
    label = u"Prestations sociales"
    definition_period = YEAR


class revenu_disponible(Variable):
    column = FloatCol()
    entity = Menage
    label = u"Revenu disponible du ménage"
    definition_period = YEAR

    def function(menage, period):
        revenu_disponible_individuels = menage.members('revenu_disponible_individuel', period = period)
        return menage.sum(revenu_disponible_individuels)


class revenu_disponible_individuel(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenu disponible individuel"
    definition_period = YEAR

    def function(individu, period):
        revenus_du_travail = individu('revenus_du_travail', period = period)
        revenu_assimile_pension = individu('revenu_assimile_pension', period = period)
        revenus_du_capital = individu('revenus_du_capital', period = period)
        prestations_sociales = individu('prestations_sociales', period = period)
        impots_directs = individu('impots_directs', period = period)

        return revenus_du_travail + revenu_assimile_pension + revenus_du_capital + prestations_sociales + impots_directs


class revenus_du_capital(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenus du capital"
    definition_period = YEAR

    def function(individu, period):
        revenus_fonciers = individu.foyer_fiscal('revenus_fonciers', period = period)
        return revenus_fonciers


class revenus_du_travail(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Revenus du travail"
    definition_period = YEAR

    def function(individu, period):
        salaire_imposable = individu('salaire_imposable', period = period, options = [ADD])
        return salaire_imposable  # + beap + bic + bnc  TODO
