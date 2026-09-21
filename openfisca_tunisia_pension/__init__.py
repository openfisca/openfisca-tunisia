"""OpenFisca Tunisia Pension tax-benefit system."""

# Standard Library
import importlib.metadata
import logging
import os

# Third Party
try:
    import numba  # noqa: F401
except ImportError as erreur:
    msg = (
        "Le système des pensions exige numba. "
        "Installer l'extra : pip install 'openfisca-tunisia[pension]'."
    )
    raise ImportError(msg) from erreur
from openfisca_core.taxbenefitsystems import TaxBenefitSystem

# First Party
from openfisca_tunisia.sous_ensembles import SOUS_ARBRES_PENSION, charger_sous_ensemble
from openfisca_tunisia_pension import entities
from openfisca_tunisia_pension.scripts_ast import script_ast

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))

# La distribution qui livre ce paquet depuis la fusion des dépôts.
DISTRIBUTION = "openfisca-tunisia"

# Les paramètres ne vivent plus dans ce paquet : ils sont dans l'arbre unique
# d'openfisca-tunisia, dont ce système ne lit que sa part — voir
# `openfisca_tunisia/sous_ensembles.py`. Les deux paquets ont longtemps porté chacun leur
# `marche_travail`, et les copies ont divergé sans que rien ne le signale : le SMIG s'était
# arrêté ici au 1er mai 2019 quand celui d'openfisca-tunisia courait jusqu'en 2025. Un seul
# arbre rend cette divergence impossible.

logging.getLogger("numba.core.ssa").disabled = True
logging.getLogger("numba.core.byteflow").disabled = True
logging.getLogger("numba.core.interpreter").disabled = True

# Convert regimes classes to OpenFisca variables.
script_ast.main(verbose=False)


class TunisiaPensionTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian pensions tax benefit system"""

    CURRENCY = "DT"

    def __init__(self):
        super(TunisiaPensionTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, "variables"))

        # Sa part de l'arbre commun, et elle seule.
        parameters = charger_sous_ensemble(SOUS_ARBRES_PENSION, avec_index=False)
        if self.preprocess_parameters is not None:
            parameters = self.preprocess_parameters(parameters)
        self.parameters = parameters

    def get_package_metadata(self) -> dict[str, str]:
        """Les métadonnées de la distribution qui livre ce paquet : `openfisca-tunisia`.

        openfisca-core les chercherait sous le nom du paquet d'import, qui n'est plus celui
        d'une distribution depuis la fusion des dépôts.
        """
        if self.baseline:
            return self.baseline.get_package_metadata()
        metadata = importlib.metadata.metadata(DISTRIBUTION)
        depot = next(
            (
                url.split("Repository, ")[-1]
                for url in (metadata.get_all("Project-URL") or [])
                if url.startswith("Repository")
            ),
            "",
        )
        return {
            "name": metadata["Name"],
            "version": metadata["Version"],
            "repository_url": depot,
            "location": os.path.dirname(COUNTRY_DIR),
        }


CountryTaxBenefitSystem = TunisiaPensionTaxBenefitSystem
