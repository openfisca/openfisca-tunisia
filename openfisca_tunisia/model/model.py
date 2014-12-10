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


from functools import partial

from openfisca_core.columns import AgeCol, BoolCol, FloatCol
from openfisca_core.formulas import (
    build_alternative_formula,
    build_dated_formula,
    build_select_formula,
    )

from .. import entities

# Import model modules.
from . import common as cm
from . import cotsoc as cs
from . import irpp as ir
from . import pfam as pf


build_alternative_formula = partial(
    build_alternative_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_dated_formula = partial(
    build_dated_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_select_formula = partial(
    build_select_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


build_alternative_formula(
    'age',
    [
        ir._age_from_birth,
        ir._age_from_agem,
        ],
    AgeCol(label = u"Âge (en années)", val_type = "age"),
    )
build_alternative_formula(
    'agem',
    [
        ir._agem_from_birth,
        ir._agem_from_age,
        ],
    AgeCol(label = u"Âge (en mois)", val_type = "months"),
    )
