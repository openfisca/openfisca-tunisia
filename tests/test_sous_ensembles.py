"""L'arbre de paramètres est unique ; chaque système n'en lit qu'une partie.

Ces tests confrontent les listes de `openfisca_tunisia/sous_ensembles.py` à l'arbre réel.
Ils prennent le relais de l'ancien garde-fou de la pension, qui interdisait qu'un même
chemin existe dans deux dépôts : il n'y a plus qu'un arbre, la question est désormais de
savoir qui en lit quoi.
"""

import os

from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_FISCAL, SYSTEMES


def _sous_arbres_presents():
    return {
        nom for nom in os.listdir(RACINE_PARAMETRES)
        if os.path.isdir(os.path.join(RACINE_PARAMETRES, nom))
    }


def test_aucun_sous_arbre_orphelin():
    """Un sous-arbre que personne ne lit est un paramètre mort, ou un oubli de liste."""
    lus = set().union(*SYSTEMES.values())
    orphelins = _sous_arbres_presents() - lus
    assert not orphelins, f"sous-arbres lus par aucun système : {sorted(orphelins)}"


def test_chaque_sous_arbre_declare_existe():
    presents = _sous_arbres_presents()
    for systeme, liste in SYSTEMES.items():
        manquants = set(liste) - presents
        assert not manquants, f"{systeme} déclare des sous-arbres absents : {sorted(manquants)}"


def test_le_systeme_fiscal_lit_exactement_sa_liste():
    """Ni plus, ni moins : un sous-arbre en trop serait lu en silence."""
    lus = set(TunisiaTaxBenefitSystem().parameters.children)
    assert lus == set(SOUS_ARBRES_FISCAL), (
        f"en trop : {sorted(lus - set(SOUS_ARBRES_FISCAL))} ; "
        f"manquants : {sorted(set(SOUS_ARBRES_FISCAL) - lus)}"
    )
