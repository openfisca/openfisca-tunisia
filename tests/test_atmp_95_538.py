"""Échelle des taux AT/MP de 1995 : décret n° 95-538, articles 1er et 2.

Le décret entre en vigueur le 1er janvier 1995 (article 28). Ses articles 1er et 2 sont
abrogés et remplacés par le décret n° 99-1010, en vigueur le 1er avril 1999 : l'échelle de 1995
cesse donc le 31 mars 1999. Les taux ont été lus dans les deux éditions du JORT n° 30 du
14 avril 1995 (pp. 690-691). Aucune variable ne lit ces paramètres, et un test YAML n'asserte
que des variables : ce test lit donc les paramètres aux bornes.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

ATMP_1995 = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux.atmp_1995

# (chemin, taux de l'article premier, taux de l'article 2) : bornes de l'échelle et chaque niveau.
POINTS = [
    ("services_de_bureaux", 0.006, 0.005),  # 1, le plus bas
    ("artisans", 0.01, 0.006),  # 4
    ("industries_agro_alimentaires.alimentaires_diverses", 0.023, 0.016),  # 6-8
    ("papier_et_arts_graphiques.imprimerie_transformation_papier_carton", 0.015, 0.01),  # 8-2
    ("mecaniques_fonderies_electriques.fonderie_siderurgie", 0.042, 0.028),  # 9-2
    ("industries_chimiques.grandes_industries_chimiques.raffineries_petrole", 0.072, 0.05),  # 15-1
    ("industries_chimiques.autres_industries_chimiques", 0.032, 0.021),  # 15-2
    ("transport_et_manutention", 0.065, 0.045),  # 17
    ("industries_extractives", 0.072, 0.05),  # 18, le plus haut
]


def bareme(cote, chemin, instant):
    noeud = ATMP_1995.children[cote]
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud.get_at_instant(instant)


@pytest.mark.parametrize(("chemin", "article_1", "article_2"), POINTS)
def test_echelle_de_1995(chemin, article_1, article_2):
    for cote, taux in (("avant_transfert", article_1), ("apres_transfert", article_2)):
        assert bareme(cote, chemin, "1994-12-31").rates == []
        assert bareme(cote, chemin, "1995-01-01").rates == [pytest.approx(taux)]
        assert bareme(cote, chemin, "1999-03-31").rates == [pytest.approx(taux)]
        assert bareme(cote, chemin, "1999-04-01").rates == []
