"""Conventions collectives sectorielles : cases versées des grilles du textile, du bâtiment et des assurances.

Chaque branche porte, sous `salaire_base`, la structure de sa grille : la grille quand la
convention en a plusieurs, la catégorie ou l'échelle, puis l'échelon. Les grilles sont versées en
partie. Quatre choses sont éprouvées :

- les valeurs, la veille et le jour d'une date d'effet ;
- les dates sans valeur : une grille dont le salaire n'a pas été relevé, ou n'est pas publié,
  porte une valeur vide, pour que la valeur précédente ne se prolonge pas ;
- le début de chaque série : rien n'est lu avant la première grille du segment continu ;
- les cases : seules les cases lues existent, et une case non versée est une erreur.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Third Party
import pytest
from openfisca_core.errors import ParameterNotFoundError

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import SOUS_ARBRES_PENSION, charger_sous_ensemble

CONVENTIONS = TunisiaTaxBenefitSystem().parameters.marche_travail.conventions_collectives

VALEURS = [
    # Textile : agents payés à l'heure, catégorie I échelon 0 et catégorie IV-2 échelon 0
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "1994-05-01", 0.749),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "1996-04-30", 0.787),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "1996-05-01", 0.825),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2005-06-14", 1.140),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2005-06-15", 1.178),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2025-12-31", 3.035),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2026-01-01", 3.248),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2026-12-31", 3.248),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "1998-05-01", 1.242),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "1999-04-30", 1.242),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2002-05-01", 1.494),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2003-04-30", 1.494),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2008-05-01", 1.912),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2016-08-01", 2.767),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2026-01-01", 4.644),
    # Bâtiment : personnel occasionnel, manœuvre ordinaire et chef d'équipe du 3e degré
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "1996-05-01", 0.862),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "1999-04-30", 0.950),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "1999-05-01", 0.989),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2021-11-30", 2.410),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2021-12-01", 2.567),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2024-01-01", 2.925),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2025-12-31", 2.925),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2004-05-01", 1.853),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2008-05-01", 2.221),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2024-01-01", 4.946),
    # Assurances, par mois : échelle 1 échelon 1 ; échelle 21, 12e échelon jusqu'en 1999 et 14e ensuite
    ("assurances.salaire_base.echelle_1.echelon_1", "1993-06-01", 181.137),
    ("assurances.salaire_base.echelle_1.echelon_1", "2002-05-31", 321.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2002-06-01", 343.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2014-05-31", 670.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2015-06-01", 838.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2019-06-01", 1298.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2020-09-30", 1298.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2020-10-01", 1438.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2021-06-01", 1598.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2025-12-31", 1598.617),
    ("assurances.salaire_base.echelle_21.echelon_12", "1998-06-01", 771.276),
    ("assurances.salaire_base.echelle_21.echelon_12", "1999-05-31", 771.276),
    ("assurances.salaire_base.echelle_21.echelon_12", "1999-06-01", 803.276),
    ("assurances.salaire_base.echelle_21.echelon_12", "2000-05-31", 803.276),
    ("assurances.salaire_base.echelle_21.echelon_14", "1999-06-01", 839.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2018-05-31", 2108.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2020-10-01", 2682.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2021-06-01", 2917.9),
]

# Dates auxquelles une grille prend effet sans que le salaire soit établi : la lecture rend None,
# et non la valeur de la grille précédente.
SANS_VALEUR = [
    # Textile, catégorie IV-2 échelon 0 : non relevé de 1999 à 2001, de 2003 à 2007 et au 1er septembre 2015
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "1999-05-01"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2002-04-30"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2003-05-01"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2005-06-15"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2008-04-30"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2015-09-01"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2016-07-31"),
    # Bâtiment, chef d'équipe du 3e degré : non relevé de 2005 à 2007
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2005-05-01"),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2008-04-30"),
    # Assurances, 12e échelon de l'échelle 21 : non relevé à compter de la grille du 1er juin 2000
    ("assurances.salaire_base.echelle_21.echelon_12", "2000-06-01"),
    ("assurances.salaire_base.echelle_21.echelon_12", "2021-06-01"),
    # Assurances : grille du 1er juin 2014 annoncée par l'avenant n° 11, non imprimée
    ("assurances.salaire_base.echelle_1.echelon_1", "2014-06-01"),
    ("assurances.salaire_base.echelle_1.echelon_1", "2015-05-31"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2014-06-01"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2015-05-31"),
    # Assurances, 14e échelon de l'échelle 21 : non lu dans les grilles du 1er juin 2018 et du 1er juin 2019
    ("assurances.salaire_base.echelle_21.echelon_14", "2018-06-01"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2019-06-01"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2020-09-30"),
    # Textile : l'avenant n° 18 ne fixe aucune grille pour 2027, que le décret n° 2026-68 relève
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "2027-01-01"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "2027-01-01"),
    # Décret n° 2026-68 : hausse de 5 % des dernières grilles au 1er janvier 2026, grilles non publiées
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2026-01-01"),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2026-01-01"),
    ("assurances.salaire_base.echelle_1.echelon_1", "2026-01-01"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2026-01-01"),
]

# Veille de la première grille du segment continu de chaque branche.
AVANT_LA_SERIE = [
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "1994-04-30"),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", "1994-04-30"),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "1996-04-30"),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "1996-04-30"),
    ("assurances.salaire_base.echelle_1.echelon_1", "1993-05-31"),
    ("assurances.salaire_base.echelle_21.echelon_12", "1993-05-31"),
    # Le 14e échelon naît le 1er juin 1999
    ("assurances.salaire_base.echelle_21.echelon_14", "1999-05-31"),
]

# Nombre de dates d'effet et, parmi elles, de dates sans valeur.
DECOMPTE = [
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", 31, 1),
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0", 31, 10),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", 27, 1),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", 27, 4),
    ("assurances.salaire_base.echelle_1.echelon_1", 29, 2),
    ("assurances.salaire_base.echelle_21.echelon_12", 8, 1),
    ("assurances.salaire_base.echelle_21.echelon_14", 23, 4),
]


# Chaque grille est versée en partie : seules ces cases existent.
CASES = {
    "textile.salaire_base.agents_payes_a_l_heure": {"categorie_1": {"echelon_0"}, "categorie_4_2": {"echelon_0"}},
    "batiment.salaire_base.personnel_occasionnel": {"manoeuvre_ordinaire": None, "chef_equipe_3e_degre": None},
    "assurances.salaire_base": {"echelle_1": {"echelon_1"}, "echelle_21": {"echelon_12", "echelon_14"}},
}


def parametre(chemin):
    noeud = CONVENTIONS
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


@pytest.mark.parametrize(("chemin", "instant", "attendu"), VALEURS)
def test_valeur(chemin, instant, attendu):
    assert parametre(chemin)(instant) == pytest.approx(attendu)


@pytest.mark.parametrize(("chemin", "instant"), SANS_VALEUR)
def test_date_sans_valeur(chemin, instant):
    assert parametre(chemin)(instant) is None


@pytest.mark.parametrize(("chemin", "instant"), AVANT_LA_SERIE)
def test_rien_avant_le_segment_continu(chemin, instant):
    assert parametre(chemin)(instant) is None


@pytest.mark.parametrize(("chemin", "dates", "vides"), DECOMPTE)
def test_decompte(chemin, dates, vides):
    valeurs = [v.value for v in parametre(chemin).values_list]
    assert len(valeurs) == dates
    assert sum(v is None for v in valeurs) == vides


@pytest.mark.parametrize(("chemin", "dates", "vides"), DECOMPTE)
def test_chaque_date_porte_sa_reference(chemin, dates, vides):
    p = parametre(chemin)
    references = p.metadata["reference"]
    assert {v.instant_str for v in p.values_list} == {str(d) for d in references}
    for date, liste in references.items():
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert "JORT n°" in reference["note"], f"{chemin} au {date} : fascicule non cité"


@pytest.mark.parametrize(("chemin", "dates", "vides"), DECOMPTE)
def test_unites(chemin, dates, vides):
    attendu = "currency/mois" if chemin.startswith("assurances") else "currency/heure"
    assert parametre(chemin).metadata["unit"] == attendu


@pytest.mark.parametrize("branche", ["textile", "batiment", "assurances"])
def test_les_anciens_chemins_n_existent_plus(branche):
    """Le résumé « bas » et « haut » a cédé la place aux cases de la grille."""
    enfants = set(CONVENTIONS.children[branche].children)
    assert enfants == {"salaire_base"}
    assert not {"salaire_base_bas", "salaire_base_haut"} & enfants


@pytest.mark.parametrize(("grille", "cases"), CASES.items())
def test_seules_les_cases_lues_existent(grille, cases):
    """Une case non lue n'a pas d'entrée : la demander est une erreur, non une valeur."""
    noeud = parametre(grille)
    assert set(noeud.children) == set(cases)
    for categorie, echelons in cases.items():
        if echelons is not None:
            assert set(noeud.children[categorie].children) == echelons


def test_une_case_non_versee_est_une_erreur():
    echelle = parametre("assurances.salaire_base.echelle_21")
    with pytest.raises(ParameterNotFoundError):
        echelle("2021-06-01").echelon_13


def test_le_systeme_des_pensions_charge_le_meme_sous_arbre():
    """La pension lit `marche_travail/` en entier : le sous-arbre y est chargé, à l'identique."""
    pension = charger_sous_ensemble(SOUS_ARBRES_PENSION).marche_travail.conventions_collectives
    assert set(pension.children) == set(CONVENTIONS.children) == {"textile", "batiment", "assurances"}
    grille = pension.textile.salaire_base.agents_payes_a_l_heure
    assert grille.categorie_1.echelon_0("2026-01-01") == pytest.approx(3.248)
