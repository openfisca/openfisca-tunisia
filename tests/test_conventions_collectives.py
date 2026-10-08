"""Conventions collectives sectorielles : grille résumée du textile, du bâtiment et des assurances.

Chaque branche porte le salaire de base du bas et du haut de sa grille, à chaque date d'effet
énoncée par l'avenant. Trois choses sont éprouvées :

- les valeurs, la veille et le jour d'une date d'effet ;
- les dates sans valeur : une grille dont le salaire n'a pas été relevé, ou n'est pas publié,
  porte une valeur vide, pour que la valeur précédente ne se prolonge pas ;
- le début de chaque série : rien n'est lu avant la première grille du segment continu.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import SOUS_ARBRES_PENSION, charger_sous_ensemble

CONVENTIONS = TunisiaTaxBenefitSystem().parameters.marche_travail.conventions_collectives

VALEURS = [
    # Textile : agents payés à l'heure, catégorie I échelon 0 (bas), catégorie IV-2 échelon 0 (haut)
    ("textile", "salaire_base_bas", "1994-05-01", 0.749),
    ("textile", "salaire_base_bas", "1996-04-30", 0.787),
    ("textile", "salaire_base_bas", "1996-05-01", 0.825),
    ("textile", "salaire_base_bas", "2005-06-14", 1.140),
    ("textile", "salaire_base_bas", "2005-06-15", 1.178),
    ("textile", "salaire_base_bas", "2025-12-31", 3.035),
    ("textile", "salaire_base_bas", "2026-01-01", 3.248),
    ("textile", "salaire_base_bas", "2026-12-31", 3.248),
    ("textile", "salaire_base_haut", "1998-05-01", 1.242),
    ("textile", "salaire_base_haut", "1999-04-30", 1.242),
    ("textile", "salaire_base_haut", "2002-05-01", 1.494),
    ("textile", "salaire_base_haut", "2003-04-30", 1.494),
    ("textile", "salaire_base_haut", "2008-05-01", 1.912),
    ("textile", "salaire_base_haut", "2016-08-01", 2.767),
    ("textile", "salaire_base_haut", "2026-01-01", 4.644),
    # Bâtiment : personnel occasionnel, manœuvre ordinaire (bas), chef d'équipe du 3e degré (haut)
    ("batiment", "salaire_base_bas", "1996-05-01", 0.862),
    ("batiment", "salaire_base_bas", "1999-04-30", 0.950),
    ("batiment", "salaire_base_bas", "1999-05-01", 0.989),
    ("batiment", "salaire_base_bas", "2021-11-30", 2.410),
    ("batiment", "salaire_base_bas", "2021-12-01", 2.567),
    ("batiment", "salaire_base_bas", "2024-01-01", 2.925),
    ("batiment", "salaire_base_bas", "2025-12-31", 2.925),
    ("batiment", "salaire_base_haut", "2004-05-01", 1.853),
    ("batiment", "salaire_base_haut", "2008-05-01", 2.221),
    ("batiment", "salaire_base_haut", "2024-01-01", 4.946),
    # Assurances : échelle 1 échelon 1 (bas), échelle 21 dernier échelon (haut), par mois
    ("assurances", "salaire_base_bas", "1993-06-01", 181.137),
    ("assurances", "salaire_base_bas", "2002-05-31", 321.617),
    ("assurances", "salaire_base_bas", "2002-06-01", 343.617),
    ("assurances", "salaire_base_bas", "2014-05-31", 670.617),
    ("assurances", "salaire_base_bas", "2015-06-01", 838.617),
    ("assurances", "salaire_base_bas", "2019-06-01", 1298.617),
    ("assurances", "salaire_base_bas", "2020-09-30", 1298.617),
    ("assurances", "salaire_base_bas", "2020-10-01", 1438.617),
    ("assurances", "salaire_base_bas", "2021-06-01", 1598.617),
    ("assurances", "salaire_base_bas", "2025-12-31", 1598.617),
    ("assurances", "salaire_base_haut", "1998-06-01", 771.276),
    ("assurances", "salaire_base_haut", "1999-06-01", 839.9),
    ("assurances", "salaire_base_haut", "2018-05-31", 2108.9),
    ("assurances", "salaire_base_haut", "2020-10-01", 2682.9),
    ("assurances", "salaire_base_haut", "2021-06-01", 2917.9),
]

# Dates auxquelles une grille prend effet sans que le salaire soit établi : la lecture rend None,
# et non la valeur de la grille précédente.
SANS_VALEUR = [
    # Textile, haut : non relevé de 1999 à 2001, de 2003 à 2007 et au 1er septembre 2015
    ("textile", "salaire_base_haut", "1999-05-01"),
    ("textile", "salaire_base_haut", "2002-04-30"),
    ("textile", "salaire_base_haut", "2003-05-01"),
    ("textile", "salaire_base_haut", "2005-06-15"),
    ("textile", "salaire_base_haut", "2008-04-30"),
    ("textile", "salaire_base_haut", "2015-09-01"),
    ("textile", "salaire_base_haut", "2016-07-31"),
    # Bâtiment, haut : non relevé de 2005 à 2007
    ("batiment", "salaire_base_haut", "2005-05-01"),
    ("batiment", "salaire_base_haut", "2008-04-30"),
    # Assurances : grille du 1er juin 2014 annoncée par l'avenant n° 11, non imprimée
    ("assurances", "salaire_base_bas", "2014-06-01"),
    ("assurances", "salaire_base_bas", "2015-05-31"),
    ("assurances", "salaire_base_haut", "2014-06-01"),
    ("assurances", "salaire_base_haut", "2015-05-31"),
    # Assurances, haut : non lu dans les grilles du 1er juin 2018 et du 1er juin 2019
    ("assurances", "salaire_base_haut", "2018-06-01"),
    ("assurances", "salaire_base_haut", "2019-06-01"),
    ("assurances", "salaire_base_haut", "2020-09-30"),
    # Textile : l'avenant n° 18 ne fixe aucune grille pour 2027, que le décret n° 2026-68 relève
    ("textile", "salaire_base_bas", "2027-01-01"),
    ("textile", "salaire_base_haut", "2027-01-01"),
    # Décret n° 2026-68 : hausse de 5 % des dernières grilles au 1er janvier 2026, grilles non publiées
    ("batiment", "salaire_base_bas", "2026-01-01"),
    ("batiment", "salaire_base_haut", "2026-01-01"),
    ("assurances", "salaire_base_bas", "2026-01-01"),
    ("assurances", "salaire_base_haut", "2026-01-01"),
]

# Veille de la première grille du segment continu de chaque branche.
AVANT_LA_SERIE = [
    ("textile", "1994-04-30"),
    ("batiment", "1996-04-30"),
    ("assurances", "1993-05-31"),
]

# Nombre de dates d'effet et, parmi elles, de dates sans valeur.
DECOMPTE = [
    ("textile", "salaire_base_bas", 31, 1),
    ("textile", "salaire_base_haut", 31, 10),
    ("batiment", "salaire_base_bas", 27, 1),
    ("batiment", "salaire_base_haut", 27, 4),
    ("assurances", "salaire_base_bas", 29, 2),
    ("assurances", "salaire_base_haut", 29, 4),
]


def parametre(branche, nom):
    return CONVENTIONS.children[branche].children[nom]


@pytest.mark.parametrize(("branche", "nom", "instant", "attendu"), VALEURS)
def test_valeur(branche, nom, instant, attendu):
    assert parametre(branche, nom)(instant) == pytest.approx(attendu)


@pytest.mark.parametrize(("branche", "nom", "instant"), SANS_VALEUR)
def test_date_sans_valeur(branche, nom, instant):
    assert parametre(branche, nom)(instant) is None


@pytest.mark.parametrize(("branche", "instant"), AVANT_LA_SERIE)
@pytest.mark.parametrize("nom", ["salaire_base_bas", "salaire_base_haut"])
def test_rien_avant_le_segment_continu(branche, nom, instant):
    assert parametre(branche, nom)(instant) is None


@pytest.mark.parametrize(("branche", "nom", "dates", "vides"), DECOMPTE)
def test_decompte(branche, nom, dates, vides):
    valeurs = [v.value for v in parametre(branche, nom).values_list]
    assert len(valeurs) == dates
    assert sum(v is None for v in valeurs) == vides


@pytest.mark.parametrize(("branche", "nom", "dates", "vides"), DECOMPTE)
def test_chaque_date_porte_sa_reference(branche, nom, dates, vides):
    p = parametre(branche, nom)
    references = p.metadata["reference"]
    assert {v.instant_str for v in p.values_list} == {str(d) for d in references}
    for date, liste in references.items():
        assert liste, f"{branche}.{nom} : aucune référence au {date}"
        for reference in liste:
            assert "JORT n°" in reference["note"], f"{branche}.{nom} au {date} : fascicule non cité"


def test_unites():
    for branche, unite in (("textile", "currency/heure"), ("batiment", "currency/heure"),
                           ("assurances", "currency/mois")):
        for nom in ("salaire_base_bas", "salaire_base_haut"):
            assert parametre(branche, nom).metadata["unit"] == unite


def test_le_systeme_des_pensions_charge_le_meme_sous_arbre():
    """La pension lit `marche_travail/` en entier : le sous-arbre y est chargé, à l'identique."""
    pension = charger_sous_ensemble(SOUS_ARBRES_PENSION).marche_travail.conventions_collectives
    assert set(pension.children) == set(CONVENTIONS.children) == {"textile", "batiment", "assurances"}
    assert pension.textile.salaire_base_bas("2026-01-01") == pytest.approx(3.248)
