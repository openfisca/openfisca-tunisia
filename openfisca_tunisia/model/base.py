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


from datetime import date
import functools

from openfisca_core.accessors import law
from openfisca_core.columns import (AgeCol, BoolCol, build_column, DateCol, EnumCol, FloatCol, IntCol, PeriodSizeIndependentIntCol,
    StrCol)
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import (dated_function, DatedFormulaColumn, EntityToPersonColumn,
                                     make_reference_formula_decorator, PersonToEntityColumn, reference_input_variable, SimpleFormulaColumn)

from ..entities import entity_class_by_symbol, FoyersFiscaux, Individus, Menages


__all__ = [
    'AgeCol',
    'build_column',
    'BoolCol',
    'CONJ',
    'CREF',
    'date',
    'DateCol',
    'dated_function',
    'DatedFormulaColumn',
    'EntityToPersonColumn',
    'Enum',
    'EnumCol',
    'FloatCol',
    'FoyersFiscaux',
    'Individus',
    'IntCol',
    'law',
    'Menages',
    'PAC1',
    'PAC2',
    'PAC3',
    'PeriodSizeIndependentIntCol',
    'PersonToEntityColumn',
    'PREF',
    'QUIFOY',
    'QUIMEN',
    'reference_formula',
    'reference_input_variable',
    'SimpleFormulaColumn',
    'StrCol',
    'VOUS',
    ]

QUIFOY = Enum(['vous', 'conj', 'pac1', 'pac2', 'pac3', 'pac4', 'pac5', 'pac6', 'pac7', 'pac8', 'pac9'])
QUIMEN = Enum(['pref', 'cref', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])

CONJ = QUIFOY['conj']
CREF = QUIMEN['cref']
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


# Functions and decorators


build_column = functools.partial(
    build_column,
    entity_class_by_symbol = entity_class_by_symbol,
    )


reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)
