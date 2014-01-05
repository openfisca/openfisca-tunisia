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

import os


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"DT"
ENTITIES_INDEX = ['men', 'foy']
REV_TYP = {
    'brut': ['salbrut'],
    'imposable': ['sal'],
    'superbrut': ['salsuperbrut'],
    }
REVENUES_CATEGORIES = {
    'imposable': ['sal'],
    }
WEIGHT = "wprm"
WEIGHT_INI = "wprm_init"
X_AXES_PROPERTIES = {
    'sali': {
        'name': 'sal',
        'typ_tot': {
            'sal':  'Salaire imposable',
            'salbrut': 'Salaire brut',
            'salnet': 'Salaire net',
            'salsuperbrut': 'Salaire super brut',
            },
        'typ_tot_default' : 'sal',
        },
    }


def init_country(qt = False):
    """Add country-specific content to OpenFisca-Core package."""
    from openfisca_core import model as core_model

    from openfisca_core import simulations as core_simulations
    from openfisca_core import taxbenefitsystems as core_taxbenefitsystems
    from openfisca_core.xaxes import XAxis

    if qt:
        from openfisca_qt import widgets as qt_widgets

    from . import decompositions, scenarios
    from .model.data import column_by_name
    from .model.model import prestation_by_name
    if qt:
        from .widgets.Composition import CompositionWidget

    core_taxbenefitsystems.preproc_inputs = None

    core_model.AGGREGATES_DEFAULT_VARS = None # AGGREGATES_DEFAULT_VARS
    core_model.CURRENCY = CURRENCY
    core_model.DATA_DIR = None
    core_model.DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    core_model.DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    core_model.DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
    core_model.ENTITIES_INDEX = ENTITIES_INDEX
    core_model.FILTERING_VARS = None # FILTERING_VARS
    core_model.column_by_name = column_by_name
    core_model.prestation_by_name = prestation_by_name
    core_model.PARAM_FILE = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
    core_model.REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')

    core_model.REV_TYP = REV_TYP  
    core_model.REVENUES_CATEGORIES = REVENUES_CATEGORIES
    core_model.Scenario = scenarios.Scenario
    core_model.WEIGHT = WEIGHT
    core_model.WEIGHT_INI = WEIGHT_INI

    core_model.x_axes = dict(
        (col_name, XAxis(col_name = col_name, label = column_by_name[col_name].label, **properties))
        for col_name, properties in X_AXES_PROPERTIES.iteritems()
        )

    if qt:
        qt_widgets.CompositionWidget = CompositionWidget

