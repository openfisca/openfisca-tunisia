import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_tunisia import entities
from openfisca_tunisia.sous_ensembles import SOUS_ARBRES_FISCAL, charger_sous_ensemble
# from openfisca_tunisia.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class TunisiaTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian tax benefit system"""

    CURRENCY = "DT"  # code iso is TND see https://fr.wikipedia.org/wiki/Dinar_tunisien
    REFORMS_DIR = os.path.join(COUNTRY_DIR, "reformes")

    def __init__(self):
        # We initialize our tax and benefit system with the general constructor
        super(TunisiaTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, "variables"))
        # self.cache_blacklist = conf_cache_blacklist
        # Le système ne lit que ses sous-arbres de l'arbre commun, et non le répertoire
        # entier : voir `openfisca_tunisia/sous_ensembles.py`.
        parameters = charger_sous_ensemble(SOUS_ARBRES_FISCAL)
        if self.preprocess_parameters is not None:
            parameters = self.preprocess_parameters(parameters)
        self.parameters = parameters
