# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import zeros
from openfisca_core.taxscales import MarginalRateTaxScale

from .base import *  # noqa analysis:ignore
from .data import CAT


############################################################################
# Salaires
############################################################################

@reference_formula
class salbrut(SimpleFormulaColumn):
    column = FloatCol(default = 0)
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

        smig = _defaultP.cotsoc.gen.smig
        cotsoc = MarginalRateTaxScale('cotsoc', _defaultP.cotsoc)

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

            if 'sal' in cotsoc[categ[0]]:
                sal = cotsoc[categ[0]]['sal']
                baremes = sal.scale_tax_scales(plaf_ss)
                bar = combine_bracket(baremes)
                invbar = bar.inverse()
                temp = iscat * invbar.calc(sali)
                salbrut += temp
        return period, salbrut


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol(default = 0)
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


@reference_formula
class cotpat(SimpleFormulaColumn):
    column = FloatCol(default = 0)
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

        smig = _P.cotsoc.gen.smig
        cotsoc = MarginalRateTaxScale('cotsoc', _P.cotsoc)

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
            if 'pat' in cotsoc[categ[0]]:
                pat = cotsoc[categ[0]]['pat']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salbrut)
                cotpat += temp
        return period, cotpat


@reference_formula
class cotsal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
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

        smig = _P.cotsoc.gen.smig
        cotsoc = MarginalRateTaxScale('cotsoc', _P.cotsoc)
        plaf_ss = 12 * smig

        n = len(salbrut)
        cotsal = zeros(n)

        for categ in CAT:
            iscat = (type_sal == categ[1])

            if categ[0] == 're':
                return period, 0 * salbrut  # TODO: doit retounrer la bonne valeur les étudiants
            else:
                continue

            if 'sal' in cotsoc[categ[0]]:
                pat = cotsoc[categ[0]]['sal']
                baremes = scale_tax_scales(pat, plaf_ss)
                bar = combine_tax_scales(baremes)
                temp = - iscat * bar.calc(salbrut)
                cotsal += temp

        return period, cotsal
