"""Régimes des non-salariés antérieurs à 1995 : décrets n° 82-1359, 82-1360 et 89-1611.

Les deux régimes de 1982 prennent effet le 1er juillet 1982 ; le décret n° 89-1611 devient
exécutoire le 22 octobre 1989, un jour franc après sa publication ; le décret n° 95-1166 les
abroge et devient exécutoire le 19 juillet 1995. Aucune variable ne lit ces paramètres, et un
test YAML n'asserte que des variables : ce test lit donc les paramètres à l'instant même, la
veille et le jour de chaque borne.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

RTNS = TunisiaPensionTaxBenefitSystem().parameters.retraite.rtns
NON_AGRICOLE = RTNS.avant_1995.non_agricole
AGRICOLE = RTNS.avant_1995.agricole

BORNES = ["1982-06-30", "1982-07-01", "1989-10-21", "1989-10-22", "1995-07-18", "1995-07-19"]
EN_VIGUEUR = [False, True, True, True, True, False]


@pytest.mark.parametrize(
    ("feuille", "valeur"),
    [
        ("age_legal", 65),  # décret n° 82-1359, art. 18
        ("age_depart_anticipe", 60),  # art. 18
        ("decote_par_trimestre", 0.005),  # art. 18
        ("stage_mois", 120),  # art. 20
        ("taux_base", 0.3),  # art. 20
        ("majoration_par_trimestre", 0.005),  # art. 20
        ("plafond_taux", 0.8),  # art. 20
        ("plancher_taux", 0.5),  # art. 22
        ("heures_annuelles_smig", 2400),  # art. 22
    ],
)
def test_non_agricole(feuille, valeur):
    parametre = NON_AGRICOLE.children[feuille]
    for instant, en_vigueur in zip(BORNES, EN_VIGUEUR):
        assert parametre(instant) == (valeur if en_vigueur else None), instant


def test_invalidite_non_agricole():
    for instant, en_vigueur in zip(BORNES, EN_VIGUEUR):  # art. 21
        assert NON_AGRICOLE.invalidite.taux_base(instant) == (0.3 if en_vigueur else None)
        assert NON_AGRICOLE.invalidite.stage_mois(instant) == (60 if en_vigueur else None)


@pytest.mark.parametrize(
    ("instant", "dinars", "smig"),
    [
        ("1982-06-30", None, None),
        ("1982-07-01", [660, 2000, 4000, 6000, 8500, 15000], None),  # art. 7
        ("1989-10-21", [660, 2000, 4000, 6000, 8500, 15000], None),
        ("1989-10-22", None, [0.666667, 1, 1.5, 2, 4, 6, 9, 12, 15]),  # art. 7 nouveau
        ("1995-07-18", None, [0.666667, 1, 1.5, 2, 4, 6, 9, 12, 15]),
        ("1995-07-19", None, None),  # décret n° 95-1166, art. 39
    ],
)
def test_classes_non_agricole(instant, dinars, smig):
    valeurs_dinars = [NON_AGRICOLE.classes_dinars.children[f"classe_{i}"](instant) for i in range(1, 7)]
    valeurs_smig = [NON_AGRICOLE.classes_smig.children[f"classe_{i}"](instant) for i in range(1, 10)]
    assert valeurs_dinars == (dinars or [None] * 6)
    assert valeurs_smig == (smig or [None] * 9)


@pytest.mark.parametrize(
    ("feuille", "valeur"),
    [
        ("age_legal", 65),  # décret n° 82-1360, art. 8
        ("jours_annuels_smag", 300),  # art. 8
        ("allocation_vieillesse_trimestres", 10),  # art. 17
    ],
)
def test_agricole(feuille, valeur):
    parametre = AGRICOLE.children[feuille]
    for instant, en_vigueur in zip(BORNES, EN_VIGUEUR):
        assert parametre(instant) == (valeur if en_vigueur else None), instant


def test_coefficients_agricoles():
    for instant, en_vigueur in zip(BORNES, EN_VIGUEUR):  # art. 5
        valeurs = [AGRICOLE.coefficients.children[f"categorie_{i}"](instant) for i in range(1, 4)]
        assert valeurs == ([1, 1.5, 2] if en_vigueur else [None] * 3), instant


def test_le_regime_fusionne_prend_le_relais():
    assert RTNS.age_legal("1995-07-18") is None
    assert RTNS.age_legal("1995-07-19") == 65
    assert RTNS.plancher_taux("1995-07-19") == 0.3
