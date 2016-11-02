# -*- coding: utf-8 -*-


from datetime import date

from openfisca_core.columns import (AgeCol, BoolCol, DateCol, EnumCol, FloatCol, IntCol,
    PeriodSizeIndependentIntCol, StrCol)
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import dated_function
from openfisca_core.variables import (DatedVariable, EntityToPersonColumn, PersonToEntityColumn,
    Variable)

from openfisca_tunisia.entities import FoyersFiscaux, Individus, Menages


__all__ = [
    'AgeCol',
    'BoolCol',
    'CONJ',
    'CREF',
    'date',
    'DateCol',
    'dated_function',
    'DatedVariable',
    'EntityToPersonColumn',
    'Enum',
    'EnumCol',
    'FloatCol',
    'FoyersFiscaux',
    'Individus',
    'IntCol',
    'Menages',
    'PAC1',
    'PAC2',
    'PAC3',
    'PeriodSizeIndependentIntCol',
    'PersonToEntityColumn',
    'PREF',
    'QUIFOY',
    'QUIMEN',
    'StrCol',
    'Variable',
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
