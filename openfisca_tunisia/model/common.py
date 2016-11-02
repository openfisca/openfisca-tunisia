# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


class revdisp_i(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Revenu disponible individuel"

    def function(self, simulation, period):
        '''
        Revenu disponible
        'ind'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        rev_trav = simulation.calculate('rev_trav', period = period)
        pen = simulation.calculate('pen', period = period)
        rev_cap = simulation.calculate('rev_cap', period = period)
        psoc = simulation.calculate('psoc', period = period)
        impo = simulation.calculate('impo', period = period)

        return period, rev_trav + pen + rev_cap + psoc + impo


class revdisp(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"Revenu disponible du ménage"

    def function(self, simulation, period):
        '''
        Revenu disponible - ménage
        'men'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        revdisp_i = simulation.calculate('revdisp_i', period = period)

        return period, self.sum_by_entity(revdisp_i)


class rev_trav(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"rev_trav"

    def function(self, simulation, period):
        '''Revenu du travail'''
        period = period.start.offset('first-of', 'month').period('year')
        sali = simulation.calculate('sali', period = period)

        return period, sali  # + beap + bic + bnc  TODO


class rev_cap(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"rev_cap"

    def function(self, simulation, period):
        '''Revenus du patrimoine'''  # TODO
        period = period.start.offset('first-of', 'month').period('year')
        rfon = simulation.calculate('rfon', period = period)

        return period, rfon


class impo(Variable):
    column = FloatCol()
    entity_class = Menages
    label = u"impo"

    def function(self, simulation, period):
        '''Impôts directs'''
        period = period.start.offset('first-of', 'month').period('year')
        irpp = simulation.calculate('irpp', period = period)

        return period, irpp
