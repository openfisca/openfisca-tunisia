"""Conventions collectives sectorielles : cases versées des grilles du textile, du bâtiment et des assurances.

Chaque branche porte, sous `salaire_base`, la structure de sa grille : la grille quand la
convention en a plusieurs, la catégorie ou l'échelle, puis l'échelon. Les cinq grilles — deux du
textile, deux du bâtiment, une des assurances — sont versées en entier. Quatre choses sont
éprouvées :

- les valeurs, la veille et le jour d'une date d'effet ;
- les dates sans valeur : une date à laquelle le salaire change sans que son montant soit publié
  porte une valeur vide, pour que la valeur précédente ne se prolonge pas ; de même une case que la
  grille publie mais qui est illisible sur le fascicule ;
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

CONVENTIONS = (
    TunisiaTaxBenefitSystem().parameters.marche_travail.conventions_collectives
)

VALEURS = [
    # Textile : agents payés à l'heure, catégorie I échelon 0 et catégorie IV-2 échelon 0
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "1994-05-01",
        0.749,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "1996-04-30",
        0.787,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "1996-05-01",
        0.825,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2005-06-14",
        1.140,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2005-06-15",
        1.178,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2025-12-31",
        3.035,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2026-01-01",
        3.248,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2026-12-31",
        3.248,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "1998-05-01",
        1.242,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "1999-04-30",
        1.242,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2002-05-01",
        1.494,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2003-04-30",
        1.494,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2008-05-01",
        1.912,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2016-08-01",
        2.767,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2026-01-01",
        4.644,
    ),
    # Textile, catégorie IV-2 : dates relues à l'image, d'abord laissées vides
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "1999-05-01",
        1.305,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2003-05-01",
        1.559,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2005-06-15",
        1.692,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "2015-09-01",
        2.610,
    ),
    # Textile : la grille du 1er janvier 2026 est la dernière valeur
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0",
        "2027-01-01",
        3.248,
    ),
    # Textile, grille entière : coins de la grille, veille et jour d'une date d'effet
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_2.echelon_0",
        "1994-05-01",
        0.816,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_1.echelon_16",
        "1998-05-01",
        1.135,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_1.echelon_16",
        "1999-04-30",
        1.135,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_1.echelon_16",
        "1999-05-01",
        1.188,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_16",
        "1998-05-01",
        1.414,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_20",
        "1999-05-01",
        1.031,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_17",
        "1999-05-01",
        1.488,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_2.echelon_11",
        "2005-06-14",
        1.237,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_2.echelon_11",
        "2005-06-15",
        1.275,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_7",
        "2008-05-01",
        2.0,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_2.echelon_5",
        "2009-05-01",
        1.749,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_2.echelon_5",
        "2010-05-01",
        1.841,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_1",
        "2023-12-31",
        2.718,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_1",
        "2024-01-01",
        2.895,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_3.echelon_20",
        "2026-01-01",
        4.450,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_20",
        "2026-01-01",
        4.958,
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_20",
        "2027-01-01",
        4.958,
    ),
    # Textile, agents payés au mois : coins, colonne de stage, veille et jour d'une date d'effet
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.stage",
        "1994-05-01",
        156.032,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.echelon_1",
        "1994-05-01",
        156.032,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1b.stage",
        "1994-05-01",
        166.362,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_16",
        "1998-05-01",
        511.921,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_16",
        "1999-04-30",
        511.921,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_16",
        "1999-05-01",
        524.921,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_20",
        "1999-05-01",
        551.225,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_20",
        "2026-01-01",
        1554.837,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_20",
        "2027-01-01",
        1554.837,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_9.echelon_7",
        "2005-06-14",
        405.159,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_9.echelon_7",
        "2005-06-15",
        418.159,
    ),
    # La colonne de stage vaut l'échelon 1 jusqu'à la grille de 2007, et moins depuis celle de 2008
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.stage",
        "2007-05-01",
        264.032,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.echelon_1",
        "2007-05-01",
        264.032,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.stage",
        "2008-05-01",
        277.234,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_1a.echelon_1",
        "2008-05-01",
        280.928,
    ),
    # Catégorie 2, échelon 18 : illisible en 1999 et 2000, lu en 2001, illisible de 2002 à 2004, lu en 2005
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18",
        "2001-05-01",
        250.847,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18",
        "2002-04-30",
        250.847,
    ),
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18",
        "2005-06-15",
        284.847,
    ),
    # Catégorie 16, échelon 6 : illisible en 1994, lu en 1995
    (
        "textile.salaire_base.agents_payes_au_mois.categorie_16.echelon_6",
        "1995-05-01",
        374.2,
    ),
    # Bâtiment : personnel occasionnel, manœuvre ordinaire et chef d'équipe du 3e degré
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "1996-05-01",
        0.862,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "1999-04-30",
        0.950,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "1999-05-01",
        0.989,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "2021-11-30",
        2.410,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "2021-12-01",
        2.567,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "2024-01-01",
        2.925,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire",
        "2025-12-31",
        2.925,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2004-05-01",
        1.853,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2008-05-01",
        2.221,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2024-01-01",
        4.946,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2005-05-01",
        1.927,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2006-05-01",
        2.001,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre",
        "2007-05-01",
        2.077,
    ),
    # Bâtiment, grille horaire entière : autres lignes, scission de l'ouvrier hautement qualifié
    (
        "batiment.salaire_base.personnel_occasionnel.manoeuvre_specialise",
        "1996-05-01",
        0.896,
    ),
    ("batiment.salaire_base.personnel_occasionnel.aide_ouvrier", "1999-04-30", 1.027),
    ("batiment.salaire_base.personnel_occasionnel.aide_ouvrier", "1999-05-01", 1.07),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_qualifie_1re_categorie",
        "2012-05-01",
        1.942,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_qualifie_2e_categorie",
        "2024-01-01",
        3.536,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie",
        "1996-05-01",
        1.062,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie",
        "2008-04-30",
        1.626,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_1",
        "2008-05-01",
        1.722,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_2",
        "2008-05-01",
        1.856,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_2",
        "2025-12-31",
        4.007,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_1er_degre",
        "2021-12-01",
        3.766,
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.chef_equipe_2e_degre",
        "2023-01-01",
        4.276,
    ),
    # Bâtiment, grille mensuelle : coins, veille et jour d'une date d'effet
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_1.echelon_1",
        "1996-05-01",
        174.032,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_1.echelon_11",
        "1996-05-01",
        185.395,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_19.echelon_1",
        "1996-05-01",
        506.97,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_19.echelon_11",
        "2024-01-01",
        2084.729,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_19.echelon_11",
        "2025-12-31",
        2084.729,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_10.echelon_6",
        "2015-08-31",
        656.058,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_10.echelon_6",
        "2015-09-01",
        694.195,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_7.echelon_3",
        "2021-11-30",
        747.911,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_7.echelon_3",
        "2021-12-01",
        796.107,
    ),
    # Bâtiment, catégorie 9, échelon 7 : illisible en 1996 et en 1998, lue en 1997 et en 1999
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1997-05-01",
        318.916,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1998-04-30",
        318.916,
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1999-05-01",
        347.916,
    ),
    # Assurances, par mois : échelle 1 échelon 1 ; échelle 21, échelons 12, 13 et 14
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
    ("assurances.salaire_base.echelle_21.echelon_12", "2000-06-01", 835.276),
    ("assurances.salaire_base.echelle_21.echelon_12", "2014-06-01", 1616.276),
    ("assurances.salaire_base.echelle_21.echelon_12", "2021-06-01", 2881.276),
    ("assurances.salaire_base.echelle_21.echelon_13", "1999-06-01", 821.588),
    ("assurances.salaire_base.echelle_21.echelon_13", "2021-06-01", 2899.588),
    # Grille du 1er juin 2014, parue à part au JORT n° 4 de 2015
    ("assurances.salaire_base.echelle_1.echelon_1", "2014-06-01", 749.617),
    ("assurances.salaire_base.echelle_1.echelon_1", "2015-05-31", 749.617),
    ("assurances.salaire_base.echelle_21.echelon_14", "2014-06-01", 1652.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2018-06-01", 2296.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2019-06-01", 2484.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "1999-06-01", 839.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2018-05-31", 2108.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2020-10-01", 2682.9),
    ("assurances.salaire_base.echelle_21.echelon_14", "2021-06-01", 2917.9),
    # Assurances, grille entière : coins, ligne « Exceptionnel », veille et jour d'une date d'effet
    ("assurances.salaire_base.echelle_1.echelon_12", "1993-06-01", 245.852),
    ("assurances.salaire_base.echelle_21.echelon_1", "1993-06-01", 440.782),
    ("assurances.salaire_base.echelle_21.echelon_1", "2025-12-31", 2679.852),
    ("assurances.salaire_base.echelle_exceptionnelle.echelon_1", "1993-06-01", 200.027),
    (
        "assurances.salaire_base.echelle_exceptionnelle.echelon_14",
        "2021-06-01",
        1691.576,
    ),
    ("assurances.salaire_base.echelle_3.echelon_12", "1998-06-01", 335.54),
    ("assurances.salaire_base.echelle_3.echelon_13", "1999-06-01", 361.728),
    ("assurances.salaire_base.echelle_10.echelon_6", "2005-05-31", 604.766),
    ("assurances.salaire_base.echelle_10.echelon_6", "2005-06-01", 635.766),
    ("assurances.salaire_base.echelle_16.echelon_12", "1993-06-01", 538.442),
    ("assurances.salaire_base.echelle_13.echelon_9", "2012-06-01", 1171.31),
    ("assurances.salaire_base.echelle_13.echelon_9", "2014-05-31", 1171.31),
    ("assurances.salaire_base.echelle_13.echelon_9", "2014-06-01", 1286.31),
    ("assurances.salaire_base.echelle_7.echelon_14", "2020-09-30", 1649.529),
    ("assurances.salaire_base.echelle_7.echelon_14", "2020-10-01", 1804.529),
    # Assurances, échelle 4, échelon 1 : la valeur reprend après la case illisible du 1er juin 1996
    ("assurances.salaire_base.echelle_4.echelon_1", "1996-05-31", 246.578),
    ("assurances.salaire_base.echelle_4.echelon_1", "1997-06-01", 288.578),
]

# Dates auxquelles une grille prend effet sans que le salaire soit établi : la lecture rend None,
# et non la valeur de la grille précédente.
SANS_VALEUR = [
    # Cases illisibles de la grille mensuelle du textile : rien jusqu'à la première grille où la case est lue.
    ("textile.salaire_base.agents_payes_au_mois.categorie_16.echelon_6", "1994-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_16.echelon_6", "1995-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.stage", "1999-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.stage", "2001-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18", "1999-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18", "2000-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18", "2002-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_2.echelon_18", "2005-06-14"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_18", "2003-05-01"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_1a.echelon_18", "2004-05-01"),
    # Décret n° 2026-68 : hausse de 5 % des dernières grilles au 1er janvier 2026, grilles non publiées.
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "2026-01-01"),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "2026-01-01"),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_1",
        "2026-01-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_1.echelon_1",
        "2026-01-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_19.echelon_11",
        "2026-01-01",
    ),
    # La ligne unique de l'ouvrier hautement qualifié cesse le 1er mai 2008 : la grille la divise
    # en deux niveaux, et elle ne se prolonge dans aucun.
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie",
        "2008-05-01",
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie",
        "2024-01-01",
    ),
    # Cases illisibles de la grille mensuelle du bâtiment : rien jusqu'à la grille suivante.
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1996-05-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1997-04-30",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_9.echelon_7",
        "1998-05-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_14.echelon_8",
        "1996-05-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_18.echelon_5",
        "2001-05-01",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_18.echelon_4",
        "2005-04-30",
    ),
    ("assurances.salaire_base.echelle_1.echelon_1", "2026-01-01"),
    ("assurances.salaire_base.echelle_21.echelon_12", "2026-01-01"),
    ("assurances.salaire_base.echelle_21.echelon_13", "2026-01-01"),
    ("assurances.salaire_base.echelle_21.echelon_14", "2026-01-01"),
    ("assurances.salaire_base.echelle_exceptionnelle.echelon_7", "2026-01-01"),
    ("assurances.salaire_base.echelle_12.echelon_14", "2026-01-01"),
    # Case illisible sur le fascicule : échelle 4, échelon 1, grille du 1er juin 1996. Ni la valeur
    # de 1995 ni une valeur déduite : rien, jusqu'à la grille du 1er juin 1997.
    ("assurances.salaire_base.echelle_4.echelon_1", "1996-06-01"),
    ("assurances.salaire_base.echelle_4.echelon_1", "1997-05-31"),
]

# Veille de la première grille du segment continu de chaque branche.
AVANT_LA_SERIE = [
    ("textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_0", "1994-04-30"),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_0",
        "1994-04-30",
    ),
    ("batiment.salaire_base.personnel_occasionnel.manoeuvre_ordinaire", "1996-04-30"),
    ("batiment.salaire_base.personnel_occasionnel.chef_equipe_3e_degre", "1996-04-30"),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie",
        "1996-04-30",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_1.echelon_1",
        "1996-04-30",
    ),
    (
        "batiment.salaire_base.personnel_administratif_technique.categorie_19.echelon_11",
        "1996-04-30",
    ),
    # Bâtiment : les niveaux I et II de l'ouvrier hautement qualifié naissent le 1er mai 2008
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_1",
        "2008-04-30",
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_2",
        "2008-04-30",
    ),
    (
        "batiment.salaire_base.personnel_occasionnel.ouvrier_hautement_qualifie_2",
        "1996-05-01",
    ),
    ("assurances.salaire_base.echelle_1.echelon_1", "1993-05-31"),
    ("assurances.salaire_base.echelle_21.echelon_12", "1993-05-31"),
    # Textile : toutes les catégories commencent le 1er mai 1994
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_2.echelon_16",
        "1994-04-30",
    ),
    # Textile : les échelons 17 à 20 n'ont aucune valeur avant la grille du 1er mai 1999
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_1.echelon_17",
        "1999-04-30",
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_2.echelon_18",
        "1999-04-30",
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_3_3.echelon_19",
        "1999-04-30",
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_20",
        "1999-04-30",
    ),
    (
        "textile.salaire_base.agents_payes_a_l_heure.categorie_4_2.echelon_20",
        "1994-05-01",
    ),
    # Textile, agents payés au mois : tout commence le 1er mai 1994, les échelons 17 à 20 le 1er mai 1999
    ("textile.salaire_base.agents_payes_au_mois.categorie_1a.stage", "1994-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_16", "1994-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_1a.echelon_17", "1999-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_20", "1999-04-30"),
    ("textile.salaire_base.agents_payes_au_mois.categorie_17.echelon_20", "1994-05-01"),
    # Les 13e et 14e échelons naissent le 1er juin 1999
    ("assurances.salaire_base.echelle_21.echelon_13", "1999-05-31"),
    ("assurances.salaire_base.echelle_21.echelon_14", "1999-05-31"),
    # Assurances : toutes les lignes commencent le 1er juin 1993, leurs 13e et 14e échelons le 1er juin 1999
    ("assurances.salaire_base.echelle_exceptionnelle.echelon_1", "1993-05-31"),
    ("assurances.salaire_base.echelle_16.echelon_12", "1993-05-31"),
    ("assurances.salaire_base.echelle_16.echelon_12", "1990-06-01"),
    ("assurances.salaire_base.echelle_4.echelon_9", "1975-01-01"),
    ("assurances.salaire_base.echelle_1.echelon_13", "1999-05-31"),
    ("assurances.salaire_base.echelle_exceptionnelle.echelon_14", "1999-05-31"),
]

# Grille horaire du textile : sept catégories ; échelons 0 à 16 aux trente dates d'effet, échelons
# 17 à 20 aux vingt-cinq dates qui commencent le 1er mai 1999.
TEXTILE_CATEGORIES = [
    "categorie_1",
    "categorie_2",
    "categorie_3_1",
    "categorie_3_2",
    "categorie_3_3",
    "categorie_4_1",
    "categorie_4_2",
]
TEXTILE_ECHELONS = [f"echelon_{n}" for n in range(21)]

# Grille des assurances : 22 lignes dans l'ordre de la grille imprimée (la ligne « Exceptionnel »
# entre les échelles 3 et 4) ; échelons 1 à 12 aux vingt-huit dates d'effet qui commencent le
# 1er juin 1993, échelons 13 et 14 aux vingt-deux dates qui commencent le 1er juin 1999 ; chaque
# case porte en outre la date sans valeur du 1er janvier 2026.
ASSURANCES_ECHELLES = [
    "echelle_1",
    "echelle_2",
    "echelle_3",
    "echelle_exceptionnelle",
    *(f"echelle_{n}" for n in range(4, 22)),
]
ASSURANCES_ECHELONS = [f"echelon_{n}" for n in range(1, 15)]
# Cases illisibles sur le fascicule : une date sans valeur de plus.
ASSURANCES_ILLISIBLES = {("echelle_4", 1): ["1996-06-01"]}

# Bâtiment, personnel occasionnel : onze lignes dans l'ordre de la grille. Neuf valent aux
# vingt-six dates d'effet et portent la date sans valeur du 1er janvier 2026 ; la ligne unique de
# l'ouvrier hautement qualifié vaut aux douze premières et cesse le 1er mai 2008 ; ses niveaux I
# et II valent aux quatorze suivantes.
BATIMENT_LIGNES = {
    "manoeuvre_ordinaire": 27,
    "manoeuvre_specialise": 27,
    "aide_ouvrier": 27,
    "ouvrier_qualifie_1re_categorie": 27,
    "ouvrier_qualifie_2e_categorie": 27,
    "ouvrier_hautement_qualifie": 13,
    "ouvrier_hautement_qualifie_1": 15,
    "ouvrier_hautement_qualifie_2": 15,
    "chef_equipe_1er_degre": 27,
    "chef_equipe_2e_degre": 27,
    "chef_equipe_3e_degre": 27,
}
# Bâtiment, personnel administratif et technique : 19 catégories, 11 échelons, vingt-six dates.
BATIMENT_CATEGORIES = [f"categorie_{n}" for n in range(1, 20)]
BATIMENT_ECHELONS = [f"echelon_{n}" for n in range(1, 12)]
# Cases illisibles sur le fascicule, (catégorie, échelon) : dates.
BATIMENT_ILLISIBLES = {
    (9, 7): ["1996-05-01", "1998-05-01"],
    (10, 7): ["1996-05-01", "1998-05-01"],
    (11, 7): ["1996-05-01"],
    (12, 7): ["1996-05-01"],
    (13, 7): ["1996-05-01"],
    (14, 7): ["1996-05-01"],
    (14, 8): ["1996-05-01"],
    (1, 7): ["1998-05-01"],
    (2, 7): ["1998-05-01"],
    (6, 7): ["1998-05-01"],
    (18, 5): ["2001-05-01"],
    (9, 4): ["2002-05-01"],
    (9, 5): ["2003-05-01"],
    (18, 4): ["2004-05-01"],
}
# Textile, agents payés au mois : dix-huit lignes ; colonne de stage et échelons 1 à 16 aux trente
# dates d'effet, échelons 17 à 20 aux vingt-cinq dates qui commencent le 1er mai 1999. La colonne
# de stage est nommée `stage` : l'échelon 0 de la grille horaire est celui de la confirmation.
TEXTILE_MENSUEL_CATEGORIES = [
    "categorie_1a",
    "categorie_1b",
    *(f"categorie_{n}" for n in range(2, 18)),
]
TEXTILE_MENSUEL_COLONNES = ["stage", *(f"echelon_{n}" for n in range(1, 21))]
# Cases illisibles sur le fascicule, par date : catégorie → numéros de colonne (0 pour le stage).
TEXTILE_ILLISIBLES = {
    "1994-05-01": {
        "categorie_16": [6],
    },
    "1999-05-01": {
        "categorie_2": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
        ],
        "categorie_3": [2, 3, 5, 6, 7, 11, 12, 13],
        "categorie_4": [5, 6, 7, 8, 9, 10, 12, 13, 14],
        "categorie_5": [5, 6, 7, 8],
    },
    "2000-05-01": {
        "categorie_2": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
        ],
        "categorie_3": [0, 1, 2, 4, 5, 17, 18],
        "categorie_4": [0, 1, 4, 18],
    },
    "2002-05-01": {
        **{c: [18] for c in TEXTILE_MENSUEL_CATEGORIES},
    },
    "2003-05-01": {
        **{c: [18] for c in TEXTILE_MENSUEL_CATEGORIES},
    },
    "2004-05-01": {
        **{c: [18] for c in TEXTILE_MENSUEL_CATEGORIES},
    },
}
MENSUELLES = (
    "assurances.",
    "batiment.salaire_base.personnel_administratif_technique.",
    "textile.salaire_base.agents_payes_au_mois.",
)

# Nombre de dates d'effet et, parmi elles, de dates sans valeur.
DECOMPTE = [
    *(
        (
            f"textile.salaire_base.agents_payes_a_l_heure.{categorie}.echelon_{n}",
            30 if n <= 16 else 25,
            0,
        )
        for categorie in TEXTILE_CATEGORIES
        for n in range(21)
    ),
    *(
        (
            f"textile.salaire_base.agents_payes_au_mois.{categorie}.{colonne}",
            30 if n <= 16 else 25,
            sum(n in cases.get(categorie, []) for cases in TEXTILE_ILLISIBLES.values()),
        )
        for categorie in TEXTILE_MENSUEL_CATEGORIES
        for n, colonne in enumerate(TEXTILE_MENSUEL_COLONNES)
    ),
    *(
        (f"batiment.salaire_base.personnel_occasionnel.{ligne}", dates, 1)
        for ligne, dates in BATIMENT_LIGNES.items()
    ),
    *(
        (
            f"batiment.salaire_base.personnel_administratif_technique.categorie_{c}.echelon_{n}",
            27,
            1 + len(BATIMENT_ILLISIBLES.get((c, n), [])),
        )
        for c in range(1, 20)
        for n in range(1, 12)
    ),
    *(
        (
            f"assurances.salaire_base.{echelle}.echelon_{n}",
            29 if n <= 12 else 23,
            1 + len(ASSURANCES_ILLISIBLES.get((echelle, n), [])),
        )
        for echelle in ASSURANCES_ECHELLES
        for n in range(1, 15)
    ),
]


# Seules ces cases existent : les cinq grilles, en entier.
CASES = {
    "textile.salaire_base.agents_payes_a_l_heure": {
        c: set(TEXTILE_ECHELONS) for c in TEXTILE_CATEGORIES
    },
    "textile.salaire_base.agents_payes_au_mois": {
        c: set(TEXTILE_MENSUEL_COLONNES) for c in TEXTILE_MENSUEL_CATEGORIES
    },
    "batiment.salaire_base.personnel_occasionnel": dict.fromkeys(BATIMENT_LIGNES),
    "batiment.salaire_base.personnel_administratif_technique": {
        c: set(BATIMENT_ECHELONS) for c in BATIMENT_CATEGORIES
    },
    "assurances.salaire_base": {
        e: set(ASSURANCES_ECHELONS) for e in ASSURANCES_ECHELLES
    },
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
            assert (
                "JORT n°" in reference["note"]
            ), f"{chemin} au {date} : fascicule non cité"


@pytest.mark.parametrize(("chemin", "dates", "vides"), DECOMPTE)
def test_unites(chemin, dates, vides):
    attendu = "currency/mois" if chemin.startswith(MENSUELLES) else "currency/heure"
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


def test_la_grille_horaire_du_textile_compte_4270_valeurs():
    """119 cases aux cinq premières dates, 147 aux vingt-cinq suivantes, aucune vide."""
    par_date = {}
    for chemin, _, _ in DECOMPTE:
        if chemin.startswith("textile.salaire_base.agents_payes_a_l_heure."):
            for v in parametre(chemin).values_list:
                assert v.value is not None
                par_date[v.instant_str] = par_date.get(v.instant_str, 0) + 1
    assert len(par_date) == 30
    assert sum(par_date.values()) == 4270
    assert {d: n for d, n in par_date.items() if d < "1999-05-01"} == {
        "1994-05-01": 119,
        "1995-05-01": 119,
        "1996-05-01": 119,
        "1997-05-01": 119,
        "1998-05-01": 119,
    }
    assert {n for d, n in par_date.items() if d >= "1999-05-01"} == {147}


def test_la_grille_mensuelle_du_textile_compte_10853_valeurs():
    """306 cases aux cinq premières dates, 378 aux vingt-cinq suivantes ; 127 cases illisibles."""
    grille = parametre("textile.salaire_base.agents_payes_au_mois")
    lues, illisibles = {}, {}
    for categorie in TEXTILE_MENSUEL_CATEGORIES:
        for n, colonne in enumerate(TEXTILE_MENSUEL_COLONNES):
            for v in grille.children[categorie].children[colonne].values_list:
                if v.value is None:
                    illisibles.setdefault(v.instant_str, {}).setdefault(
                        categorie, []
                    ).append(n)
                else:
                    lues[v.instant_str] = lues.get(v.instant_str, 0) + 1
    assert illisibles == TEXTILE_ILLISIBLES
    assert len(lues) == 30
    assert sum(lues.values()) == 10853
    vides = {d: sum(len(c) for c in cases.values()) for d, cases in illisibles.items()}
    assert vides == {
        "1994-05-01": 1,
        "1999-05-01": 42,
        "2000-05-01": 30,
        "2002-05-01": 18,
        "2003-05-01": 18,
        "2004-05-01": 18,
    }
    for d, n in lues.items():
        assert n + vides.get(d, 0) == (306 if d < "1999-05-01" else 378), d


def test_les_cases_illisibles_du_textile_disent_leur_raison():
    grille = parametre("textile.salaire_base.agents_payes_au_mois")
    for date, cases in TEXTILE_ILLISIBLES.items():
        for categorie, colonnes in cases.items():
            for n in colonnes:
                p = grille.children[categorie].children[TEXTILE_MENSUEL_COLONNES[n]]
                (reference,) = {str(d): r for d, r in p.metadata["reference"].items()}[
                    date
                ]
                assert "case illisible sur le fascicule" in reference["note"]
                assert "dinars par mois" not in reference["note"]


def test_les_cases_du_textile_lues_sans_controle_croise_le_disent():
    """Six cases lues dont la voisine est illisible aux dates d'effet voisines : leur note le dit, et elles seules."""
    grille = parametre("textile.salaire_base.agents_payes_au_mois")
    trouvees = set()
    for categorie in TEXTILE_MENSUEL_CATEGORIES:
        for colonne in TEXTILE_MENSUEL_COLONNES:
            for date, (reference,) in (
                grille.children[categorie]
                .children[colonne]
                .metadata["reference"]
                .items()
            ):
                if "sans contrôle croisé" in reference["note"]:
                    trouvees.add((str(date), categorie, colonne))
    assert trouvees == {
        ("1999-05-01", "categorie_3", "echelon_17"),
        ("1999-05-01", "categorie_3", "echelon_18"),
        ("1999-05-01", "categorie_4", "echelon_18"),
        ("2001-05-01", "categorie_2", "echelon_18"),
        ("2001-05-01", "categorie_3", "echelon_18"),
        ("2001-05-01", "categorie_4", "echelon_18"),
    }


def test_la_grille_mensuelle_du_textile_est_croissante():
    """À chaque date, le salaire croît avec la colonne dans une ligne (le stage ne dépasse pas l'échelon 1), et
    d'une ligne à la suivante à colonne égale. Les cases sans valeur sont sautées.
    """
    grille = parametre("textile.salaire_base.agents_payes_au_mois")
    dates = [
        v.instant_str
        for v in grille.children["categorie_1a"].children["stage"].values_list
    ]
    assert len(dates) == 30
    for date in dates:
        colonnes = (
            TEXTILE_MENSUEL_COLONNES
            if date >= "1999-05-01"
            else TEXTILE_MENSUEL_COLONNES[:17]
        )
        table = [
            [grille.children[c].children[e](date) for e in colonnes]
            for c in TEXTILE_MENSUEL_CATEGORIES
        ]
        for ligne in table:
            if ligne[0] is not None and ligne[1] is not None:
                assert ligne[0] <= ligne[1], date
                assert (ligne[0] == ligne[1]) == (date < "2008-05-01"), date
            lues = [x for x in ligne[1:] if x is not None]
            assert all(a < b for a, b in zip(lues, lues[1:])), date
        for colonne in zip(*table):
            lues = [x for x in colonne if x is not None]
            assert all(a <= b for a, b in zip(lues, lues[1:])), date


def test_la_grille_horaire_du_textile_est_croissante():
    """À chaque date, le salaire croît avec l'échelon dans une catégorie, et avec la catégorie à échelon égal."""
    grille = parametre("textile.salaire_base.agents_payes_a_l_heure")
    dates = [
        v.instant_str
        for v in grille.children["categorie_1"].children["echelon_0"].values_list
    ]
    for date in dates:
        echelons = TEXTILE_ECHELONS if date >= "1999-05-01" else TEXTILE_ECHELONS[:17]
        table = [
            [grille.children[c].children[e](date) for e in echelons]
            for c in TEXTILE_CATEGORIES
        ]
        for ligne in table:
            assert all(a < b for a, b in zip(ligne, ligne[1:])), date
        for bas, haut in zip(table, table[1:]):
            assert all(a <= b for a, b in zip(bas, haut)), date


def test_la_grille_des_assurances_compte_8359_valeurs():
    """264 cases aux six premières dates, 308 aux vingt-deux suivantes ; une seule case illisible."""
    par_date, illisibles = {}, []
    for chemin, _, _ in DECOMPTE:
        if chemin.startswith("assurances."):
            for v in parametre(chemin).values_list:
                if v.instant_str == "2026-01-01":
                    assert v.value is None
                elif v.value is None:
                    illisibles.append((chemin, v.instant_str))
                else:
                    par_date[v.instant_str] = par_date.get(v.instant_str, 0) + 1
    assert illisibles == [("assurances.salaire_base.echelle_4.echelon_1", "1996-06-01")]
    assert len(par_date) == 28
    assert sum(par_date.values()) == 8359
    assert {d: n for d, n in par_date.items() if d < "1999-06-01"} == {
        "1993-06-01": 264,
        "1994-06-01": 264,
        "1995-06-01": 264,
        "1996-06-01": 263,
        "1997-06-01": 264,
        "1998-06-01": 264,
    }
    assert {n for d, n in par_date.items() if d >= "1999-06-01"} == {308}


def test_une_case_illisible_dit_sa_raison():
    """La note d'une case illisible le dit, et ne cite aucune valeur."""
    for (echelle, n), dates in ASSURANCES_ILLISIBLES.items():
        references = parametre(
            f"assurances.salaire_base.{echelle}.echelon_{n}"
        ).metadata["reference"]
        for date in dates:
            (reference,) = {str(d): r for d, r in references.items()}[date]
            assert "case illisible sur le fascicule" in reference["note"]
            assert "dinars par mois" not in reference["note"]


def test_la_grille_des_assurances_est_croissante():
    """À chaque date, le salaire croît avec l'échelon dans une ligne, et d'une ligne à la suivante à échelon égal.

    Les cases sans valeur sont sautées : la comparaison porte sur les cases lues qui se suivent.
    """
    grille = parametre("assurances.salaire_base")
    dates = [
        v.instant_str
        for v in grille.children["echelle_1"].children["echelon_1"].values_list
        if v.value is not None
    ]
    for date in dates:
        echelons = (
            ASSURANCES_ECHELONS if date >= "1999-06-01" else ASSURANCES_ECHELONS[:12]
        )
        table = [
            [grille.children[e].children[n](date) for n in echelons]
            for e in ASSURANCES_ECHELLES
        ]
        for ligne in table:
            lues = [x for x in ligne if x is not None]
            assert all(a < b for a, b in zip(lues, lues[1:])), date
        for colonne in zip(*table):
            lues = [x for x in colonne if x is not None]
            assert all(a <= b for a, b in zip(lues, lues[1:])), date


def test_les_grilles_du_batiment_comptent_248_et_5418_valeurs():
    """Horaire : 9 cases aux douze premières dates, 10 aux quatorze suivantes. Mensuelle : 209 moins les illisibles."""
    horaire, mensuelle, illisibles = {}, {}, {}
    for chemin, _, _ in DECOMPTE:
        if not chemin.startswith("batiment."):
            continue
        par_date = mensuelle if chemin.startswith(MENSUELLES) else horaire
        for v in parametre(chemin).values_list:
            if v.value is not None:
                par_date[v.instant_str] = par_date.get(v.instant_str, 0) + 1
            elif v.instant_str != "2026-01-01" and chemin.startswith(MENSUELLES):
                _, c, n = chemin.rsplit("_", 2)
                illisibles.setdefault((int(c.split(".")[0]), int(n)), []).append(
                    v.instant_str
                )
    assert len(horaire) == len(mensuelle) == 26
    assert sum(horaire.values()) == 248
    assert {n for d, n in horaire.items() if d < "2008-05-01"} == {9}
    assert {n for d, n in horaire.items() if d >= "2008-05-01"} == {10}
    assert sum(mensuelle.values()) == 5418
    assert {
        case: sorted(dates) for case, dates in illisibles.items()
    } == BATIMENT_ILLISIBLES
    assert {d: 209 - n for d, n in mensuelle.items() if n != 209} == {
        "1996-05-01": 7,
        "1998-05-01": 5,
        "2001-05-01": 1,
        "2002-05-01": 1,
        "2003-05-01": 1,
        "2004-05-01": 1,
    }


def test_les_cases_illisibles_du_batiment_disent_leur_raison():
    for (c, n), dates in BATIMENT_ILLISIBLES.items():
        chemin = f"batiment.salaire_base.personnel_administratif_technique.categorie_{c}.echelon_{n}"
        references = {
            str(d): r for d, r in parametre(chemin).metadata["reference"].items()
        }
        for date in dates:
            (reference,) = references[date]
            assert "case illisible sur le fascicule" in reference["note"]
            assert "dinars par mois" not in reference["note"]


def test_l_avenant_16_du_batiment_est_lu_sur_une_reproduction():
    """Aux trois dates de l'avenant n° 16, chaque note dit la reproduction, et aucun lien n'est donné."""
    for chemin, _, _ in DECOMPTE:
        if not chemin.startswith("batiment.") or chemin.endswith(
            ".ouvrier_hautement_qualifie"
        ):
            continue
        references = {
            str(d): r for d, r in parametre(chemin).metadata["reference"].items()
        }
        for date in ("2021-12-01", "2023-01-01", "2024-01-01"):
            (reference,) = references[date]
            assert "reproduction" in reference["note"] and "href" not in reference


def test_les_grilles_du_batiment_sont_croissantes():
    """À chaque date : les lignes de la grille horaire croissent ; dans la grille mensuelle, le salaire croît
    avec l'échelon dans une catégorie, et avec la catégorie à échelon égal. Les cases sans valeur sont sautées.
    """
    horaire = parametre("batiment.salaire_base.personnel_occasionnel")
    mensuelle = parametre("batiment.salaire_base.personnel_administratif_technique")
    dates = [
        v.instant_str
        for v in horaire.children["manoeuvre_ordinaire"].values_list
        if v.value is not None
    ]
    for date in dates:
        lignes = [
            x
            for x in (horaire.children[ligne](date) for ligne in BATIMENT_LIGNES)
            if x is not None
        ]
        assert len(lignes) == (9 if date < "2008-05-01" else 10)
        assert all(a < b for a, b in zip(lignes, lignes[1:])), date
        table = [
            [mensuelle.children[c].children[e](date) for e in BATIMENT_ECHELONS]
            for c in BATIMENT_CATEGORIES
        ]
        for ligne in table:
            lues = [x for x in ligne if x is not None]
            assert all(a < b for a, b in zip(lues, lues[1:])), date
        for colonne in zip(*table):
            lues = [x for x in colonne if x is not None]
            assert all(a <= b for a, b in zip(lues, lues[1:])), date


def test_une_case_non_versee_est_une_erreur():
    echelle = parametre("assurances.salaire_base.echelle_21")
    with pytest.raises(ParameterNotFoundError):
        echelle("2021-06-01").echelon_15


def test_le_systeme_des_pensions_charge_le_meme_sous_arbre():
    """La pension lit `marche_travail/` en entier : le sous-arbre y est chargé, à l'identique."""
    pension = charger_sous_ensemble(
        SOUS_ARBRES_PENSION
    ).marche_travail.conventions_collectives
    assert (
        set(pension.children)
        == set(CONVENTIONS.children)
        == {"textile", "batiment", "assurances"}
    )
    grille = pension.textile.salaire_base.agents_payes_a_l_heure
    assert grille.categorie_1.echelon_0("2026-01-01") == pytest.approx(3.248)
