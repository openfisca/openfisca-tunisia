# -*- coding: utf-8 -*-


from __future__ import division

from numpy import zeros
from openfisca_core.taxscales import MarginalRateTaxScale

from openfisca_tunisia.model.base import *  # noqa analysis:ignore
from openfisca_tunisia.model.data import CAT


############################################################################
# Salaires
############################################################################

class salaire_brut(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaires bruts"

    def function(individu, period, legislation):
        '''
        Calcule le salaire brut à partir du salaire net
        '''
        period = period.this_year
        salaire_imposable = individu('salaire_imposable', period = period)
        categorie_salarie = individu('categorie_salarie', period = period)
        _defaultP = legislation(period.start, reference = True)

        smig = _defaultP.cotisations_sociales.gen.smig_40h_mensuel
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _defaultP.cotisations_sociales)

        plaf_ss = 12 * smig

        n = len(salaire_imposable)
        salaire_brut = zeros(n)
        # TODO améliorer tout cela !!
        for categ in CAT:
            iscat = (categorie_salarie == categ[1])
            if categ[0] == 're':
                return period, salaire_imposable  # on retourne le salaire_imposable pour les étudiants
            else:
                continue

            if 'sal' in cotisations_sociales[categ[0]]:
                sal = cotisations_sociales[categ[0]]['sal']
                baremes = sal.scale_tax_scales(plaf_ss)
                bar = combine_bracket(baremes)
                invbar = bar.inverse()
                temp = iscat * invbar.calc(salaire_imposable)
                salaire_brut += temp
        return period, salaire_brut


class salaire_super_brut(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaires super bruts"

    def function(individu, period):
        period = period.this_year
        salaire_brut = individu('salaire_brut', period = period)
        cotpat = individu('cotpat', period = period)

        return period, salaire_brut - cotpat


class cotpat(Variable):
    column = FloatCol
    entity = Individu
    label = u"cotpat"

    def function(individu, period, legislation):
        '''
        Cotisation sociales patronales
        '''
        period = period.this_year
        salaire_brut = individu('salaire_brut', period = period)
        categorie_salarie = individu('categorie_salarie', period = period)
        _P = legislation(period.start)

        # TODO traiter les différents régimes séparément ?

        smig = _P.cotisations_sociales.gen.smig_40h_mensuel
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)

        plaf_ss = 12 * smig
        # TODO: clean all this
        n = len(salaire_brut)
        cotpat = zeros(n)
        for categ in CAT:
            iscat = (categorie_salarie == categ[1])
            if categ[0] == 're':
                return period, salaire_brut  # on retounre le salaire_brut pour les étudiants
            else:
                continue
            if 'pat' in cotisations_sociales[categ[0]]:
                pat = cotisations_sociales[categ[0]]['pat']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salaire_brut)
                cotpat += temp
        return period, cotpat


class cotsal(Variable):
    column = FloatCol
    entity = Individu
    label = u"cotsal"

    def function(individu, period, legislation):
        '''
        Cotisations sociales salariales
        '''
        period = period.this_year
        salaire_brut = individu('salaire_brut', period = period)
        categorie_salarie = individu('categorie_salarie', period = period)
        _P = legislation(period.start)

        # TODO traiter les différents régimes

        smig = _P.cotisations_sociales.gen.smig
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)
        plaf_ss = 12 * smig

        n = len(salaire_brut)
        cotsal = zeros(n)

        for categ in CAT:
            iscat = (categorie_salarie == categ[1])

            if categ[0] == 're':
                return period, 0 * salaire_brut  # TODO: doit retounrer la bonne valeur les étudiants
            else:
                continue

            if 'sal' in cotisations_sociales[categ[0]]:
                pat = cotisations_sociales[categ[0]]['sal']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salaire_brut)
                cotsal += temp

        return period, cotsal
