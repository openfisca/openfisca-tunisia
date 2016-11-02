# -*- coding: utf-8 -*-

import glob
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from . import decompositions, entities, scenarios
from .model import datatrees

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class TunisiaTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian tax benefit system"""
    CURRENCY = u"DT"
    DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
    REV_TYP = None
    REVENUES_CATEGORIES = {
        'imposable': ['sal'],
        }

    columns_name_tree_by_entity = datatrees.columns_name_tree_by_entity

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities.entities)
        self.Scenario = scenarios.Scenario

        legislation_xml_file_path = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        self.add_legislation_params(legislation_xml_file_path)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        for extension_dir in EXTENSIONS_DIRECTORIES:
            self.load_extension(extension_dir)
