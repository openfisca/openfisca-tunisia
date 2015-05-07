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

import os


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"DT"
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
            'sal': 'Salaire imposable',
            'salbrut': 'Salaire brut',
            'salaire_net': 'Salaire net',
            'salsuperbrut': 'Salaire super brut',
            },
        'typ_tot_default': 'sal',
        },
    }


def init_country(qt = False):
    """Create a country-specific TaxBenefitSystem."""
    from openfisca_core.taxbenefitsystems import LegacyTaxBenefitSystem

    from . import decompositions, entities, scenarios
    from .model import datatrees
    from .model import data  # Load input variables into entities. # noqa
    from .model import model  # Load output variables into entities. # noqa

    class TaxBenefitSystem(LegacyTaxBenefitSystem):
        """Tunisian tax benefit system"""
        # AGGREGATES_DEFAULT_VARS = AGGREGATES_DEFAULT_VARS
        check_consistency = None  # staticmethod(utils.check_consistency)
        columns_name_tree_by_entity = datatrees.columns_name_tree_by_entity
        CURRENCY = CURRENCY
        # DATA_DIR = DATA_DIR
        # DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
        DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
        DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
        entity_class_by_key_plural = dict(
            (entity_class.key_plural, entity_class)
            for entity_class in entities.entity_class_by_symbol.itervalues()
            )
        # FILTERING_VARS = FILTERING_VARS
        # column_by_name = column_by_name  # Done below to avoid "name is not defined" exception
        # columns_name_tree_by_entity = columns_name_tree_by_entity  # Done below to avoid "name is not defined"
        # exception
        legislation_xml_file_path = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        # preprocess_compact_legislation = preprocess_compact_legislation  # Done below to avoid "name is not defined"
        # exception
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

    return TaxBenefitSystem
