# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


class revenu_disponible_individuel(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Revenu disponible individuel"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenus_du_travail = simulation.calculate('revenus_du_travail', period = period)
        revenu_assimile_pension = simulation.calculate('revenu_assimile_pension', period = period)
        revenus_du_capital = simulation.calculate('revenus_du_capital', period = period)
        psoc = simulation.calculate('psoc', period = period)
        impots_directs = simulation.calculate('impots_directs', period = period)

        return period, revenus_du_travail + revenu_assimile_pension + revenus_du_capital + psoc + impots_directs


class revenu_disponible(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Revenu disponible du ménage"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenu_disponible_individuel = simulation.calculate('revenu_disponible_individuel', period = period)
        return period, self.sum_by_entity(revenu_disponible_individuel)


class revenus_du_travail(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Revenu du travail"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        salaire_imposable = simulation.calculate('salaire_imposable', period = period)

        return period, salaire_imposable  # + beap + bic + bnc  TODO


class revenus_du_capital(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Revenus du patrimoine"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenus_fonciers = simulation.calculate('revenus_fonciers', period = period)

        return period, revenus_fonciers


class impots_directs(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Impôts directs"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        irpp = simulation.calculate('irpp', period = period)

        return period, irpp
