# -*- coding: utf-8 -*-


from __future__ import division

from numpy import zeros
from openfisca_core.taxscales import MarginalRateTaxScale

from openfisca_tunisia.model.base import *  # noqa analysis:ignore
from openfisca_tunisia.model.data import CAT


############################################################################
# Salaires
############################################################################

class salbrut(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires bruts"

    def function(self, simulation, period):
        '''
        Calcule le salaire brut à partir du salaire net
        '''
        period = period.start.offset('first-of', 'month').period('year')
        sali = simulation.calculate('sali', period = period)
        type_sal = simulation.calculate('type_sal', period = period)
        _defaultP = simulation.legislation_at(period.start, reference = True)

        smig = _defaultP.cotisations_sociales.gen.smig
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _defaultP.cotisations_sociales)

        plaf_ss = 12 * smig

        n = len(sali)
        salbrut = zeros(n)
        # TODO améliorer tout cela !!
        for categ in CAT:
            iscat = (type_sal == categ[1])
            if categ[0] == 're':
                return period, sali  # on retourne le sali pour les étudiants
            else:
                continue

            if 'sal' in cotisations_sociales[categ[0]]:
                sal = cotisations_sociales[categ[0]]['sal']
                baremes = sal.scale_tax_scales(plaf_ss)
                bar = combine_bracket(baremes)
                invbar = bar.inverse()
                temp = iscat * invbar.calc(sali)
                salbrut += temp
        return period, salbrut


class salsuperbrut(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires super bruts"

    def function(self, simulation, period):
        '''
        Salaire superbrut
        '''
        period = period.start.offset('first-of', 'month').period('year')
        salbrut = simulation.calculate('salbrut', period = period)
        cotpat = simulation.calculate('cotpat', period = period)

        return period, salbrut - cotpat


class cotpat(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"cotpat"

    def function(self, simulation, period):
        '''
        Cotisation sociales patronales
        '''
        period = period.start.offset('first-of', 'month').period('year')
        salbrut = simulation.calculate('salbrut', period = period)
        type_sal = simulation.calculate('type_sal', period = period)
        _P = simulation.legislation_at(period.start)

        # TODO traiter les différents régimes séparément ?

        smig = _P.cotisations_sociales.gen.smig
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)

        plaf_ss = 12 * smig
        # TODO: clean all this
        n = len(salbrut)
        cotpat = zeros(n)
        for categ in CAT:
            iscat = (type_sal == categ[1])
            if categ[0] == 're':
                return period, salbrut  # on retounre le salbrut pour les étudiants
            else:
                continue
            if 'pat' in cotisations_sociales[categ[0]]:
                pat = cotisations_sociales[categ[0]]['pat']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salbrut)
                cotpat += temp
        return period, cotpat


class cotsal(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"cotsal"

    def function(self, simulation, period):
        '''
        Cotisations sociales salariales
        '''
        period = period.start.offset('first-of', 'month').period('year')
        salbrut = simulation.calculate('salbrut', period = period)
        type_sal = simulation.calculate('type_sal', period = period)
        _P = simulation.legislation_at(period.start)

        # TODO traiter les différents régimes

        smig = _P.cotisations_sociales.gen.smig
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)
        plaf_ss = 12 * smig

        n = len(salbrut)
        cotsal = zeros(n)

        for categ in CAT:
            iscat = (type_sal == categ[1])

            if categ[0] == 're':
                return period, 0 * salbrut  # TODO: doit retounrer la bonne valeur les étudiants
            else:
                continue

            if 'sal' in cotisations_sociales[categ[0]]:
                pat = cotisations_sociales[categ[0]]['sal']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salbrut)
                cotsal += temp

        return period, cotsal
