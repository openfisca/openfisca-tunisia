"""Taux de cotisation AT/MP des employeurs affiliés à la CNSS : décret n° 99-1010.

L'article premier du décret n° 99-1010 du 10 mai 1999 remplace l'article 2 du décret
n° 95-538, qui fixe les taux une fois opéré le transfert d'un point des cotisations du
régime général. Le décret entre en vigueur le 1er avril 1999 (article 2). Les taux ont été
lus à l'image dans les deux éditions du JORT n° 40 du 18 mai 1999 (pp. 733-734 et 897-898).
Aucune variable ne lit ces paramètres, et un test YAML n'asserte que des variables : ce test
lit donc les paramètres, la veille et le jour de l'entrée en vigueur.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

ATMP = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux.atmp

# Un point par borne de l'échelle et par niveau de l'arborescence (point de l'article 2 nouveau).
POINTS = [
    ("services_de_bureaux", 0.004),  # 1, le plus bas
    ("commerce.commerce_de_detail", 0.005),  # 3-2
    ("agriculture_et_peche", 0.006),  # 5
    ("industries_agro_alimentaires.abattoirs", 0.016),  # 6-9
    ("industries_chimiques.industrie_de_la_synthese_organique", 0.03),  # 22-4
    ("industries_chimiques.fabrication_de_produits_pharmaceutiques", 0.025),  # 22-5
    ("batiment_et_travaux_publics", 0.038),  # 23
    ("transport_et_manutention.transports_terrestres", 0.04),  # 27-1, le plus haut
    ("auto_ecole", 0.04),  # 28, le plus haut
    ("industries_extractives", 0.035),  # 29
    ("activites_sportives", 0.015),  # 37, le dernier
]


def bareme(chemin, instant):
    noeud = ATMP
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud.get_at_instant(instant)


@pytest.mark.parametrize(("chemin", "valeur"), POINTS)
def test_taux_au_1er_avril_1999(chemin, valeur):
    assert bareme(chemin, "1999-03-31").rates == []
    assert bareme(chemin, "1999-04-01").rates == [pytest.approx(valeur)]
    assert bareme(chemin, "2004-08-01").rates == [pytest.approx(valeur)]
