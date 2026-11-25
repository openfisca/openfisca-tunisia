"""Différentiel complémentaire des petites pensions : seuil de 180 dinars par mois.

Décret-loi n° 2020-30 du 10 juin 2020, article premier ; entrée en vigueur à la date de sa
publication, le 10 juin 2020 (article 17). Sont éprouvés la valeur le jour même, l'absence de
valeur la veille, la référence à l'édition arabe et l'unité.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

DIFFERENTIEL = TunisiaPensionTaxBenefitSystem().parameters.retraite.differentiel_petites_pensions


def test_seuil():
    seuil = DIFFERENTIEL.seuil
    assert seuil("2020-06-09") is None
    assert seuil("2020-06-10") == 180
    assert seuil("2026-01-01") == 180
    assert seuil.metadata["unit"] == "currency/mois"
    references = seuil.metadata["reference"]
    assert [str(date) for date in references] == ["2020-06-10"]
    reference = references["2020-06-10"][0]
    assert reference["href"] == "https://www.pist.tn/jort/2020/2020A/Ja0542020.pdf"
    assert "p. 1408" in reference["note"]
    assert "p. 1413" in reference["note"]


def test_ordre_du_noeud():
    assert set(DIFFERENTIEL.children) == set(DIFFERENTIEL.metadata["order"])
