"""RSNA : âge avant lequel le remariage suspend la pension du conjoint survivant.

Décret n° 90-1455 du 10 septembre 1990, article premier (article 32 nouveau du décret
n° 74-499), exécutoire le 23 septembre 1990. Avant cette date, le remariage supprime la
pension quel que soit l'âge (article 32 de 1974) : aucun âge n'est versé. Sont éprouvés la
valeur le jour même, l'absence de valeur la veille, la référence et l'unité.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

SURVIVANTS = TunisiaPensionTaxBenefitSystem().parameters.retraite.rsna.survivants


def test_age_remariage_suspensif():
    age = SURVIVANTS.age_remariage_suspensif
    assert age("1974-01-01") is None
    assert age("1990-09-22") is None
    assert age("1990-09-23") == 55
    assert age("2026-01-01") == 55
    assert age.metadata["unit"] == "year"
    references = age.metadata["reference"]
    assert [str(date) for date in references] == ["1990-09-23"]
    reference = references["1990-09-23"][0]
    assert reference["href"] == "https://www.pist.tn/jort/1990/1990F/Jo06090.pdf"
    assert "p. 1358" in reference["note"]
    assert "article 32 nouveau" in reference["title"]
