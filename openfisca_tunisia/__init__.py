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
    """Create a country-specific TaxBenefitSystem."""
    from openfisca_core.columns import FloatCol
    from openfisca_core import taxbenefitsystems as core_taxbenefitsystems
    if qt:
        from openfisca_qt import widgets as qt_widgets

    from . import decompositions, entities, scenarios
    from .model.data import column_by_name
    from .model.datatrees import columns_name_tree_by_entity
    from .model.model import prestation_by_name
    if qt:
        from .widgets.Composition import CompositionWidget

    core_taxbenefitsystems.preproc_inputs = None


    class TaxBenefitSystem(core_taxbenefitsystems.AbstractTaxBenefitSystem):
        """Tunisian tax benefit system"""
        # AGGREGATES_DEFAULT_VARS = AGGREGATES_DEFAULT_VARS
        check_consistency = None  # staticmethod(utils.check_consistency)
        CURRENCY = CURRENCY
        # DATA_DIR = DATA_DIR
        # DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
        DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
        DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
        entities = [
            'foyers_fiscaux',
            'individus',
            'menages',
            ]
        ENTITIES_INDEX = ENTITIES_INDEX
        # entity_class_by_key_plural = entity_class_by_key_plural  # Done below to avoid "name is not defined" exception
        # FILTERING_VARS = FILTERING_VARS
        # column_by_name = column_by_name  # Done below to avoid "name is not defined" exception
        # columns_name_tree_by_entity = columns_name_tree_by_entity  # Done below to avoid "name is not defined" exception
        PARAM_FILE = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        # preprocess_legislation_parameters = preprocess_legislation_parameters  # Done below to avoid "name is not defined" exception
        # prestation_by_name = prestation_by_name  # Done below to avoid "name is not defined" exception
        REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
        REV_TYP = REV_TYP
        REVENUES_CATEGORIES = REVENUES_CATEGORIES
        Scenario = scenarios.Scenario
        WEIGHT = WEIGHT
        WEIGHT_INI = WEIGHT_INI

        def preproc_inputs(self, datatable):
            """Preprocess inputs table: country specific manipulations

            Parameters
            ----------
            datatable : a DataTable object
                        the DataTable containing the input variables of the model

            """
            try:
                datatable.propagate_to_members(WEIGHT, 'ind')
            #    datatable.propagate_to_members('rfr_n_2', 'ind')
            #    datatable.propagate_to_members('nbptr_n_2', 'ind')
            except:
                pass

    TaxBenefitSystem.column_by_name = column_by_name
    TaxBenefitSystem.columns_name_tree_by_entity = columns_name_tree_by_entity
    TaxBenefitSystem.entity_class_by_key_plural = dict(
        (entity_class.key_plural, entity_class)
        for entity_class in entities.entity_class_by_symbol.itervalues()
        )
    TaxBenefitSystem.preprocess_legislation_parameters = None  # staticmethod(preprocess_legislation_parameters)

    TaxBenefitSystem.prestation_by_name = prestation_by_name
    return TaxBenefitSystem

