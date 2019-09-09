# -*- coding: utf-8 -*-

import glob
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_tunisia import decompositions, entities


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class TunisiaTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian tax benefit system"""
    CURRENCY = "DT"
    DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE

    def __init__(self):
        # We initialize our tax and benefit system with the general constructor
        super(TunisiaTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_path)
