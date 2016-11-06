# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


class revenu_disponible_individuel(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Revenu disponible individuel"

    def function(self, simulation, period):
        '''
        Revenu disponible
        'ind'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        revenus_du_travail = simulation.calculate('revenus_du_travail', period = period)
        pen = simulation.calculate('pen', period = period)
        revenus_du_capital = simulation.calculate('revenus_du_capital', period = period)
        psoc = simulation.calculate('psoc', period = period)
        impo = simulation.calculate('impots_directs', period = period)

        return period, revenus_du_travail + pen + revenus_du_capital + psoc + impo


class revenu_disponible(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Revenu disponible du ménage"

    def function(self, simulation, period):
        '''
        Revenu disponible - ménage
        'men'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        revenu_disponible_individuel = simulation.calculate('revenu_disponible_individuel', period = period)

        return period, self.sum_by_entity(revenu_disponible_individuel)


class revenus_du_travail(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"revenus_du_travail"

    def function(self, simulation, period):
        '''Revenu du travail'''
        period = period.start.offset('first-of', 'month').period('year')
        sali = simulation.calculate('sali', period = period)

        return period, sali  # + beap + bic + bnc  TODO


class revenus_du_capital(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"revenus_du_capital"

    def function(self, simulation, period):
        '''Revenus du patrimoine'''  # TODO
        period = period.start.offset('first-of', 'month').period('year')
        rfon = simulation.calculate('rfon', period = period)

        return period, rfon


class impots_directsVariable):
    column = FloatCol()
    entity_class = Menages
    label = u"Impôts directs"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        irpp = simulation.calculate('irpp', period = period)

        return period, irpp
