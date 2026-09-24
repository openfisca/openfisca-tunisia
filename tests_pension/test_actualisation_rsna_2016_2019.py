"""Barèmes d'actualisation des salaires du RSNA de 2016, 2017 et 2019 : chargement aux bornes.

Arrêtés du ministre des affaires sociales du 1er mars 2016 (JORT n° 20, p. 686), du
10 avril 2017 (JORT n° 32, pp. 1497-1498) et du 5 mars 2019 (JORT n° 21, édition arabe,
p. 783). Chacun s'applique, selon son article 2, aux pensions dont le droit est ouvert à
compter du 1er janvier de son année.

Aucune formule ne lit ces coefficients : un test YAML, qui porte sur des variables, ne peut
pas les atteindre. D'où ce test Python, qui lit les paramètres de part et d'autre de chaque
date d'effet. Les valeurs attendues sont celles des barèmes publiés.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

ACTUALISATION = TunisiaPensionTaxBenefitSystem().parameters.retraite.rsna.salaire_reference.actualisation


CAS = [
    # (date, année de salaire, coefficient attendu)
    # Veille et jour d'effet du barème de 2016.
    ("2015-12-31", 1961, 14.35578),  # barème de 2015
    ("2016-01-01", 1961, 15.03350),  # barème de 2016
    ("2016-01-01", 1968, 11.77057),  # imprimé « 1l.77057 » dans l'édition française
    ("2016-01-01", 2014, 1.04721),
    ("2016-01-01", 2015, 1.00000),
    # Veille et jour d'effet du barème de 2017.
    ("2016-12-31", 1961, 15.03350),
    ("2017-01-01", 1961, 15.59374),
    ("2017-01-01", 2015, 1.03727),
    ("2017-01-01", 2016, 1.00000),
    # Veille du barème de 2019 : le barème de 2018 est encore en vigueur.
    ("2018-12-31", 1961, 16.42349),
    ("2018-12-31", 2017, 1.00000),
    # Jour d'effet du barème de 2019.
    ("2019-01-01", 1961, 17.64780),
    ("2019-01-01", 2017, 1.07455),
    ("2019-01-01", 2018, 1.00000),
    # Le barème de 2020, déjà versé, prend le relais.
    ("2019-12-31", 1961, 17.64780),
    ("2020-01-01", 1961, 18.84722),
]


@pytest.mark.parametrize("date, annee, attendu", CAS)
def test_coefficient_aux_bornes(date, annee, attendu):
    assert getattr(ACTUALISATION, f"annee_{annee}")(date) == pytest.approx(attendu, abs=1e-9)


@pytest.mark.parametrize(
    "annee, veille",
    [
        (2015, "2015-12-31"),  # premier coefficient des salaires de 2015 : barème de 2016
        (2016, "2016-12-31"),  # des salaires de 2016 : barème de 2017
        (2018, "2018-12-31"),  # des salaires de 2018 : barème de 2019
    ],
)
def test_pas_de_coefficient_avant_le_premier_bareme(annee, veille):
    assert getattr(ACTUALISATION, f"annee_{annee}")(veille) is None
