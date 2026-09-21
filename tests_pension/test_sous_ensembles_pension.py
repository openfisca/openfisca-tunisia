"""Le système des pensions lit sa part de l'arbre commun, et cohabite avec le système fiscal.

Ces tests vivent ici, et non dans `tests/`, parce qu'ils importent le paquet de la pension,
qui exige numba : la suite du système fiscal doit pouvoir tourner sans lui.
"""

import importlib.metadata

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import SOUS_ARBRES_PENSION
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


def test_la_pension_lit_exactement_sa_liste():
    """Ni plus, ni moins : la pension ne doit pas lire les impôts, ni la fiscalité la retraite."""
    lus = set(TunisiaPensionTaxBenefitSystem().parameters.children)
    assert lus == set(SOUS_ARBRES_PENSION), (
        f"en trop : {sorted(lus - set(SOUS_ARBRES_PENSION))} ; "
        f"manquants : {sorted(set(SOUS_ARBRES_PENSION) - lus)}"
    )


def test_les_deux_systemes_cohabitent_sans_se_capturer_leurs_entites():
    """openfisca-core inscrit dans chaque entité une référence vers le système qui la
    construit. Si les deux systèmes partageaient leurs objets d'entité, le second construit
    capturerait ceux du premier. Chaque paquet garde donc son `entities.py` ; ce test le
    vérifie en construisant les deux dans l'ordre, puis en calculant avec le PREMIER.
    """
    fiscal = TunisiaTaxBenefitSystem()
    pension = TunisiaPensionTaxBenefitSystem()

    for systeme in (fiscal, pension):
        for entite in systeme.entities:
            assert entite._tax_benefit_system is systeme, (
                f"l'entité « {entite.key} » de {type(systeme).__name__} appartient à "
                f"{type(entite._tax_benefit_system).__name__}"
            )

    # Chaque système calcule une variable qui n'existe que chez lui. Si ses entités avaient
    # été capturées par l'autre système, la variable y serait cherchée, et introuvable.
    # Côté fiscal : l'âge, déduit de la date de naissance.
    simulation = SimulationBuilder().build_from_entities(
        fiscal, {"individus": {"a": {"date_naissance": {"ETERNITY": "1960-06-15"}}}}
    )
    assert simulation.calculate("age", "2020-01")[0] == 59

    # Côté pension : l'âge légal du cadre commun, lu dans `retraite/`. 60 ans avant la loi
    # n° 2019-37, 62 ans après — ce qui éprouve aussi le sous-ensemble de paramètres chargé.
    # (L'`age` de la pension n'a pas de formule : c'est une donnée d'entrée, nulle par défaut.)
    simulation = SimulationBuilder().build_from_entities(pension, {"individus": {"a": {}}})
    assert simulation.calculate("cnrps_age_requis", "2015")[0] == 60
    assert simulation.calculate("cnrps_age_requis", "2021")[0] == 62


def test_les_metadonnees_de_paquet_sont_celles_de_la_distribution():
    """Sans correction, openfisca-core avale l'erreur et annonce une version 0.0.0."""
    metadonnees = TunisiaPensionTaxBenefitSystem().get_package_metadata()
    assert metadonnees["version"] == importlib.metadata.version("openfisca-tunisia")
    assert metadonnees["version"] != "0.0.0"
    assert metadonnees["repository_url"].startswith("https://github.com/openfisca/")
