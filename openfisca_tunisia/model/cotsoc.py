# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

from numpy import  zeros
from openfisca_core.taxscales import TaxScaleDict, combine_tax_scales, scale_tax_scales

from .data import CAT


class Object(object):
    def __init__(self):
        object.__init__(self)

############################################################################
## Salaires
############################################################################

def _salbrut(sali, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire net
    '''

    smig = _defaultP.cotsoc.gen.smig
    cotsoc = TaxScaleDict('cotsoc', _defaultP.cotsoc)

    plaf_ss = 12*smig

    n = len(sali)
    salbrut = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        if 'sal' in  cotsoc[categ[0]]:
            sal = cotsoc[categ[0]]['sal']
            baremes = scale_tax_scales(sal, plaf_ss)
            bar = combine_tax_scales(baremes)
            invbar = bar.inverse()
            temp =  iscat*(invbar.calc(sali))
            salbrut += temp
    return salbrut


def _salsuperbrut(salbrut, cotpat):
    '''
    Salaire superbrut
    '''
    return salbrut - cotpat

def _cotpat(salbrut, type_sal, _P):
    '''
    Cotisation sociales patronales
    '''
    # TODO traiter les différents régimes séparément ?


    smig = _P.cotsoc.gen.smig
    cotsoc = TaxScaleDict('cotsoc', _P.cotsoc)

    plaf_ss = 12*smig


    n = len(salbrut)
    cotpat = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        if 'pat' in  cotsoc[categ[0]]:
            pat = cotsoc[categ[0]]['pat']
            baremes = scale_tax_scales(pat, plaf_ss)
            bar = combine_tax_scales(baremes)
            temp = - (iscat*bar.calc(salbrut))
            cotpat += temp
    return cotpat


def _cotsal(salbrut, type_sal, _P):
    '''
    Cotisations sociales salariales
    '''
    # TODO traiter les différents régimes

    smig = _P.cotsoc.gen.smig
    cotsoc = TaxScaleDict('cotsoc', _P.cotsoc)
    plaf_ss = 12*smig

    n = len(salbrut)
    cotsal = zeros(n)

    for categ in CAT:
        iscat = (type_sal == categ[1])
        if 'sal' in  cotsoc[categ[0]]:
            pat = cotsoc[categ[0]]['sal']
            baremes = scale_tax_scales(pat, plaf_ss)
            bar = combine_tax_scales(baremes)
            temp = - (iscat*bar.calc(salbrut))
            cotsal += temp

    return cotsal
