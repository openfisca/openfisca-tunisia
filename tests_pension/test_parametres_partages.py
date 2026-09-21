"""Un sous-arbre de paramètres a un propriétaire, et un seul.

Les deux paquets tunisiens ont longtemps porté chacun leur `marche_travail`, et les
copies ont divergé sans que rien ne le signale : le SMIG s'était arrêté ici au 1er mai
2019 quand celui d'openfisca-tunisia courait jusqu'au 1er janvier 2025. Les pensions
minimales étant indexées dessus, elles étaient fausses pour 2020-2026 — une valeur
périmée, pas une valeur manquante, donc silencieuse.

Ces tests interdisent le retour de cette situation, et vérifient que la greffe fait ce
qu'on attend d'elle.
"""

import os
from pathlib import Path

import openfisca_tunisia

from openfisca_tunisia_pension import SOUS_ARBRES_PARTAGES, TunisiaPensionTaxBenefitSystem


PARAMETRES_PENSION = Path(__file__).parent.parent / "openfisca_tunisia_pension" / "parameters"
PARAMETRES_TUNISIA = Path(os.path.dirname(os.path.abspath(openfisca_tunisia.__file__))) / "parameters"


def _chemins(racine: Path) -> set[str]:
    return {
        str(f.relative_to(racine))
        for f in racine.rglob("*.yaml")
        if f.name != "index.yaml"
    }


def test_aucun_parametre_n_existe_dans_les_deux_paquets():
    communs = sorted(_chemins(PARAMETRES_PENSION) & _chemins(PARAMETRES_TUNISIA))
    assert communs == [], (
        "Ces paramètres existent dans les deux paquets et vont diverger. "
        "Un sous-arbre a un propriétaire et un seul : `retraite/` appartient à "
        "openfisca-tunisia-pension, `marche_travail/` à openfisca-tunisia. "
        f"À trancher : {communs}"
    )


def test_les_sous_arbres_partages_ne_sont_pas_recopies_ici():
    for nom in SOUS_ARBRES_PARTAGES:
        assert not (PARAMETRES_PENSION / nom).exists(), (
            f"« {nom} » est greffé depuis openfisca-tunisia : en garder une copie ici "
            "rouvre la dérive que la greffe ferme."
        )


def test_la_greffe_rend_les_sous_arbres_accessibles():
    tbs = TunisiaPensionTaxBenefitSystem()
    for nom in SOUS_ARBRES_PARTAGES:
        assert nom in tbs.parameters.children, f"« {nom} » n'a pas été greffé."
    assert "retraite" in tbs.parameters.children, "L'arbre propre a disparu."


def test_le_smig_ne_s_arrete_plus_en_2019():
    tbs = TunisiaPensionTaxBenefitSystem()
    en_2019 = tbs.get_parameters_at_instant("2019-06-01").marche_travail.smig_40h_mensuel
    en_2025 = tbs.get_parameters_at_instant("2025-06-01").marche_travail.smig_40h_mensuel
    assert en_2025 > en_2019, (
        "Le SMIG est de nouveau figé : la greffe ne lit plus openfisca-tunisia, "
        f"ou sa série s'est arrêtée ({en_2019} en 2019, {en_2025} en 2025)."
    )
