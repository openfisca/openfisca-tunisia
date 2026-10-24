"""Limite d'âge des membres du Tribunal administratif et de la Cour des comptes.

Décret n° 73-459 du 3 octobre 1973 et décret n° 74-820 du 28 août 1974, article premier :
65 ans, par dérogation au décret n° 59-78. Aucun ne fixe de date d'effet ; les dates sont celles
du jour franc après la publication. Sont éprouvés la valeur le jour même, l'absence de valeur la
veille, la référence et l'unité.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

CIVIL = TunisiaPensionTaxBenefitSystem().parameters.retraite.cnrps.age_legal.civil

CAS = [
    ("magistrats_tribunal_administratif", "1973-10-06", "1973-10-07", "/1973/1973F/Jo03773.pdf", "p. 1532"),
    ("magistrats_cour_des_comptes", "1974-08-31", "1974-09-01", "/1974/1974F/Jo05574.pdf", "p. 1919"),
]


@pytest.mark.parametrize(("feuille", "veille", "jour", "fascicule", "page"), CAS)
def test_limite_d_age(feuille, veille, jour, fascicule, page):
    parametre = CIVIL.children[feuille]
    assert parametre(veille) is None
    assert parametre(jour) == 65
    assert parametre("2026-01-01") == 65
    assert parametre.metadata["unit"] == "year"
    references = parametre.metadata["reference"]
    assert [str(date) for date in references] == [jour]
    reference = references[jour][0]
    assert reference["href"] == f"https://www.pist.tn/jort{fascicule}"
    assert page in reference["note"]


def test_ordre_du_noeud():
    assert set(CIVIL.children) == set(CIVIL.metadata["order"])
