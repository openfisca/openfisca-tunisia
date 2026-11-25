"""Taux AT/MP de l'article premier nouveau du décret n° 95-538 (décret n° 99-1010).

L'article premier du décret n° 99-1010 du 10 mai 1999 remplace les articles 1er et 2 du décret
n° 95-538. L'article premier nouveau fixe les taux de cotisation au régime selon les secteurs
d'activité, avant le transfert d'un point des cotisations du régime général ; l'article 2
nouveau, porté par `atmp`, les fixe après ce transfert. Le décret entre en vigueur le 1er avril
1999. Les taux ont été lus à l'image dans les deux éditions du JORT n° 40 du 18 mai 1999.
Aucune variable ne lit ces paramètres, et un test YAML n'asserte que des variables : ce test
lit donc les paramètres.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

PARAMETRES = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux
BRUT = PARAMETRES.atmp_avant_transfert
NET = PARAMETRES.atmp

# (chemin, taux de l'article premier nouveau) : bornes de l'échelle et chaque niveau.
POINTS = [
    ("services_de_bureaux", 0.005),  # 1, le plus bas
    ("commerce.commerce_de_gros", 0.007),  # 3-1
    ("industries_agro_alimentaires.abattoirs", 0.023),  # 6-9
    ("industries_chimiques.fabrication_de_produits_pharmaceutiques", 0.047),  # 22-5
    ("batiment_et_travaux_publics", 0.055),  # 23
    ("transport_et_manutention.transports_terrestres", 0.06),  # 27-1, le plus haut
    ("auto_ecole", 0.06),  # 28, le plus haut
    ("activites_sportives", 0.022),  # 37, le dernier
]


def bareme(racine, chemin, instant):
    noeud = racine
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud.get_at_instant(instant)


@pytest.mark.parametrize(("chemin", "valeur"), POINTS)
def test_taux_avant_transfert(chemin, valeur):
    assert bareme(BRUT, chemin, "1999-03-31").rates == []
    assert bareme(BRUT, chemin, "1999-04-01").rates == [pytest.approx(valeur)]


def feuilles(noeud, prefixe=""):
    for nom, enfant in noeud.children.items():
        if hasattr(enfant, "children"):
            yield from feuilles(enfant, f"{prefixe}{nom}.")
        else:
            yield f"{prefixe}{nom}"


def test_meme_arborescence_que_atmp():
    assert sorted(feuilles(BRUT)) == sorted(feuilles(NET))


def test_le_taux_avant_transfert_n_est_jamais_inferieur():
    for chemin in feuilles(NET):
        brut = bareme(BRUT, chemin, "1999-04-01").rates[0]
        net = bareme(NET, chemin, "1999-04-01").rates[0]
        assert brut >= net, chemin
