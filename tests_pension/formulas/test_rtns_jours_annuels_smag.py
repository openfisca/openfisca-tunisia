"""Durée annuelle de travail du SMAG, non-salariés agricoles : décrets n° 95-1166 et 96-1797.

Le décret n° 95-1166 fixe 300 jours (articles 7 et 25) et devient exécutoire le 19 juillet 1995.
Le décret n° 96-1797, exécutoire le 19 octobre 1996, y substitue 180 jours jusqu'au
31 décembre 1996, 260 jours en 1997, puis 300 jours à compter du 1er janvier 1998 selon
l'édition arabe, qui fait foi (l'édition française porte le 1er décembre 1998). Aucune variable
ne lit ce paramètre, et un test YAML n'asserte que des variables : ce test lit donc le paramètre,
la veille et le jour de chaque borne.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

JOURS = TunisiaPensionTaxBenefitSystem().parameters.retraite.rtns.revenu_reference.jours_annuels_smag


@pytest.mark.parametrize(
    ("instant", "jours"),
    [
        ("1995-07-18", None),  # avant le régime
        ("1995-07-19", 300),  # décret n° 95-1166, art. 7 et 25
        ("1996-10-18", 300),
        ("1996-10-19", 180),  # décret n° 96-1797, art. 1, exécutoire
        ("1996-12-31", 180),
        ("1997-01-01", 260),
        ("1997-12-31", 260),
        ("1998-01-01", 300),  # édition arabe ; l'édition française dit le 1er décembre
        ("1998-11-30", 300),
        ("1998-12-01", 300),
    ],
)
def test_jours_annuels_smag(instant, jours):
    assert JOURS(instant) == jours
