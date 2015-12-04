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

# from openfisca_core.statshelpers import mark_weighted_percentiles

from .base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIMEN]


# def _typ_men(isol, af_nbenf):
#    '''
#    type de menage
#    'men'
#    TODO: prendre les enfants du ménages et non ceux de la famille
#    '''
#    _0_kid = af_nbenf == 0
#    _1_kid = af_nbenf == 1
#    _2_kid = af_nbenf == 2
#    _3_kid = af_nbenf >= 3
#
#    return period, (0*(isol & _0_kid) + # Célibataire
#            1*(not_(isol) & _0_kid) + # Couple sans enfants
#            2*(not_(isol) & _1_kid) + # Couple un enfant
#            3*(not_(isol) & _2_kid) + # Couple deux enfants
#            4*(not_(isol) & _3_kid) + # Couple trois enfants et plus
#            5*(isol & _1_kid) + # Famille monoparentale un enfant
#            6*(isol & _2_kid) + # Famille monoparentale deux enfants
#            7*(isol & _3_kid) ) # Famille monoparentale trois enfants et plus


class revdisp_i(Variable):
    column = FloatCol(default = 0)
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
    column = FloatCol(default = 0)
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
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_trav"

    def function(self, simulation, period):
        '''Revenu du travail'''
        period = period.start.offset('first-of', 'month').period('year')
        sali = simulation.calculate('sali', period = period)

        return period, sali  # + beap + bic + bnc  TODO


# def _pen(rstnet, alr, alv, rto):
#    '''Pensions'''
#    return period, rstnet #+ alr + alv + rto TODO
#
# def _rstnet(pen):
#    '''Retraites nettes'''
#    return period, pen


class rev_cap(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"rev_cap"

    def function(self, simulation, period):
        '''Revenus du patrimoine'''  # TODO
        period = period.start.offset('first-of', 'month').period('year')
        rfon = simulation.calculate('rfon', period = period)

        return period, rfon


# def _psoc(pfam):
#    '''Prestations sociales'''
#    return period, pfam
#
# def _pfam(af,s):
#    ''' Prestations familiales '''
#    return period, af


class impo(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"impo"

    def function(self, simulation, period):
        '''Impôts directs'''
        period = period.start.offset('first-of', 'month').period('year')
        irpp = simulation.calculate('irpp', period = period)

        return period, irpp


## def _decile(nivvie, wprm):
##     '''
##     Décile de niveau de vie
##     'men'
##     '''
##     labels = arange(1, 11)
##     method = 2
##     decile = mark_weighted_percentiles(nivvie, labels, wprm, method, return_quantiles = False)
##     return period, decile
