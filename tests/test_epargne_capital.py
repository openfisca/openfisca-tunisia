"""Revenus de l'épargne et du capital : retenues à la source sur les revenus de capitaux
mobiliers et sur les revenus distribués, taux et franchise de la plus-value de cession de titres.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : code de
1990 (article 52), lois de finances pour 1992 (article 31, exécutoire le 2 janvier 1992), 1997,
2002, 2004, 2014, 2018, 2021 et 2022, décret-loi n° 2020-30 (article 12), loi de finances pour 2023
(article 42) ; pour les non-résidents, les jetons de présence et les actions cotées, lois de
finances pour 1995, 2005, 2011, 2012, 2017, 2019 et 2025 et loi de finances complémentaire pour
2012. Sont éprouvés, feuille par feuille :

- la valeur la veille et le jour de chaque date d'effet, clôtures comprises ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- la note des séries dont les états antérieurs ne sont pas versés ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme des sous-arbres, et le système des pensions qui ne les charge pas.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Standard Library
import datetime

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

IMPOT_REVENU = TunisiaTaxBenefitSystem().parameters.impot_revenu

CODE_1990 = ("JORT n° 1 des 2-5 janvier 1990", "/1990/1990F/Jo00190.pdf")
LF_1992 = ("JORT n° 90 du 31 décembre 1991", "/1991/1991F/Jo09091.pdf")
LF_1997 = ("JORT n° 105 du 31 décembre 1996", "/1996/1996F/Jo10596.pdf")
LF_2002 = ("JORT n° 104 du 28 décembre 2001", "/2001/2001F/Jo1042001.pdf")
LF_2004 = ("JORT n° 104 du 30 décembre 2003", "/2003/2003F/Jo1042003.pdf")
LF_2014 = ("JORT n° 105 du 31 décembre 2013", "/2013/2013F/Jo1052013.pdf")
LF_2018 = ("JORT n° 101 du 19 décembre 2017", "/2017/2017F/Jo1012017.pdf")
DL_2020_30 = (
    "JORT n° 54 du 10 juin 2020, édition arabe",
    "/2020/2020A/Ja0542020.pdf",
)
LF_2021 = ("JORT n° 128 du 25 décembre 2020", "/2020/2020F/Jo1282020.pdf")
LF_2022 = ("JORT n° 119 du 28 décembre 2021", "/2021/2021F/Jo1192021.pdf")
LF_2023 = (
    "JORT n° 141 du 23 décembre 2022, édition arabe",
    "/2022/2022A/Ja1412022.pdf",
)
LF_1995 = ("JORT n° 103 des 30-31 décembre 1994", "/1994/1994F/Jo10394.pdf")
LF_2005 = ("JORT n° 105 du 31 décembre 2004", "/2004/2004F/Jo1052004.pdf")
LF_2011 = ("JORT n° 102 du 21 décembre 2010", "/2010/2010F/Jo1022010.pdf")
LF_2012 = ("JORT n° 1 du 3 janvier 2012", "/2012/2012F/Jo0012012.pdf")
LFC_2012 = ("JORT n° 39 du 18 mai 2012", "/2012/2012F/Jo0392012.pdf")
LF_2017 = ("JORT n° 105 du 27 décembre 2016", "/2016/2016F/Jo1052016.pdf")
LF_2019 = (
    "JORT n° 104 du 28 décembre 2018, édition arabe",
    "/2018/2018A/Ja1042018.pdf",
)
# Édition française lue sur une copie locale ; pist.tn ne sert que l'édition arabe.
LF_2025 = ("JORT n° 149 du 10 décembre 2024", "/2024/2024A/Ja1492024.pdf")

RETENUE = "capitaux_mobiliers.retenue_source"
NON_RESIDENTS = "capitaux_mobiliers.non_residents"
DISTRIBUES = "valeurs_mobilieres.revenus_distribues"
JETONS = "valeurs_mobilieres.jetons_presence"
PLUS_VALUE = "valeurs_mobilieres.plus_value_cession_titres"
COTEES = f"{PLUS_VALUE}.actions_cotees"
PV_NON_RESIDENTS = f"{PLUS_VALUE}.non_residents"

# Chemin sous impot_revenu : unité, et suite des (date, valeur, texte). None : clôture.
SERIES = {
    f"{RETENUE}.taux_imputable": (
        "/1",
        [
            ("1990-01-01", 0.15, CODE_1990),
            ("1992-01-02", 0.15, LF_1992),
            ("1997-01-01", 0.20, LF_1997),
            ("2021-01-01", None, LF_2021),
            ("2022-01-01", 0.20, LF_2022),
        ],
    ),
    f"{RETENUE}.taux_liberatoire": (
        "/1",
        [
            ("2021-01-01", 0.20, LF_2021),
            ("2022-01-01", None, LF_2022),
        ],
    ),
    f"{RETENUE}.taux_comptes_speciaux_epargne": (
        "/1",
        [
            ("1990-01-01", 0.10, CODE_1990),
            ("1992-01-02", 0.15, LF_1992),
            ("1997-01-01", None, LF_1997),
        ],
    ),
    f"{RETENUE}.taux_obligations_porteur_anonymes": (
        "/1",
        [
            ("1992-01-02", 0.25, LF_1992),
            ("1997-01-01", None, LF_1997),
        ],
    ),
    f"{RETENUE}.taux_titres_porteur_anonymes": (
        "/1",
        [
            ("1990-01-01", 0.35, CODE_1990),
            ("1992-01-02", 0.35, LF_1992),
            ("1997-01-01", None, LF_1997),
        ],
    ),
    f"{RETENUE}.taux_depots_terme": (
        "/1",
        [
            ("2020-06-10", 0.35, DL_2020_30),
            ("2021-01-01", None, LF_2021),
        ],
    ),
    f"{RETENUE}.depots_terme_ecart_taux_marche_monetaire": (
        "/1",
        [
            ("2020-06-10", 0.01, DL_2020_30),
            ("2021-01-01", None, LF_2021),
        ],
    ),
    f"{DISTRIBUES}.taux_retenue_source": (
        "/1",
        [
            ("2015-01-01", 0.05, LF_2014),
            ("2018-01-01", 0.10, LF_2018),
        ],
    ),
    f"{DISTRIBUES}.plafond_revenus_restitution": (
        "currency",
        [
            ("2015-01-01", 10000, LF_2014),
        ],
    ),
    f"{PLUS_VALUE}.taux": (
        "/1",
        [
            ("2004-01-01", 0.10, LF_2004),
            ("2023-01-01", 0.10, LF_2023),
        ],
    ),
    f"{PLUS_VALUE}.taux_non_cotes_detention_courte": (
        "/1",
        [
            ("2023-01-01", 0.15, LF_2023),
        ],
    ),
    f"{PLUS_VALUE}.franchise": (
        "currency",
        [
            ("2004-01-01", 10000, LF_2004),
            ("2023-01-01", None, LF_2023),
        ],
    ),
    # Retenue définitive des organismes exonérés et des fonds (article 52, II-2).
    f"{RETENUE}.taux_definitif_organismes_exoneres": (
        "/1",
        [
            ("1992-01-02", 0.20, LF_1992),
            ("2002-01-01", 0.20, LF_2002),
            ("2021-01-01", None, LF_2021),
            ("2022-01-01", 0.20, LF_2022),
        ],
    ),
    # Comptes d'épargne-emprunts obligataires (loi de finances pour 1992, article 33).
    f"{RETENUE}.taux_comptes_epargne_emprunts_obligataires": (
        "/1",
        [
            ("1992-01-02", 0.15, LF_1992),
            ("1997-01-01", None, LF_1997),
        ],
    ),
    f"{RETENUE}.taux_complementaire_retrait_epargne_emprunts_obligataires": (
        "/1",
        [
            ("1992-01-02", 0.10, LF_1992),
            ("1997-01-01", None, LF_1997),
        ],
    ),
    # Non-résidents : revenus de capitaux mobiliers, intérêts des prêts bancaires, paradis.
    f"{NON_RESIDENTS}.taux_revenus_capitaux_mobiliers": (
        "/1",
        [
            ("1990-01-01", 0.15, CODE_1990),
            ("1992-01-02", 0.15, LF_1992),
            ("1997-01-01", 0.20, LF_1997),
        ],
    ),
    f"{NON_RESIDENTS}.taux_interets_prets_banques_non_etablies": (
        "/1",
        [
            ("1995-01-01", 0.025, LF_1995),
            ("2011-01-01", 0.05, LF_2011),
            ("2018-01-01", 0.10, LF_2018),
        ],
    ),
    f"{NON_RESIDENTS}.taux_etats_regime_fiscal_privilegie": (
        "/1",
        [
            ("2014-01-01", 0.25, LF_2014),
            ("2019-01-01", 0.25, LF_2019),
        ],
    ),
    # Jetons de présence.
    f"{JETONS}.taux_retenue_source": (
        "/1",
        [
            ("1995-01-01", 0.15, LF_1995),
            ("2005-01-01", 0.20, LF_2005),
            ("2017-01-01", 0.20, LF_2017),
        ],
    ),
    # Actions cotées : exonération et condition de détention (article 38, point 17).
    f"{COTEES}.taux_detention_longue": (
        "/1",
        [
            ("2004-01-01", 0, LF_2004),
            ("2011-01-01", 0, LF_2011),
        ],
    ),
    f"{COTEES}.taux_detention_courte": (
        "/1",
        [
            ("2004-01-01", 0, LF_2004),
            ("2011-01-01", 0.10, LF_2011),
            ("2023-01-01", 0.10, LF_2023),
        ],
    ),
    f"{COTEES}.annees_detention": (
        "year",
        [
            ("2011-01-01", 1, LF_2011),
        ],
    ),
    # Plus-value des non-résidents (article 52, I-e en 2011, I-e bis depuis 2012).
    f"{PV_NON_RESIDENTS}.taux_retenue_prix_personnes_morales": (
        "/1",
        [
            ("2011-01-01", 0.05, LF_2011),
            ("2012-01-01", None, LF_2012),
        ],
    ),
    f"{PV_NON_RESIDENTS}.taux_retenue_prix_personnes_physiques": (
        "/1",
        [
            ("2011-01-01", 0.025, LF_2011),
            ("2012-01-01", None, LF_2012),
        ],
    ),
    f"{PV_NON_RESIDENTS}.taux_personnes_morales": (
        "/1",
        [
            ("2012-01-01", 0.30, LF_2012),
            ("2014-01-01", 0.25, LF_2014),
            ("2021-01-01", 0.15, LF_2021),
            ("2025-01-01", 0.20, LF_2025),
        ],
    ),
    f"{PV_NON_RESIDENTS}.taux_personnes_physiques": (
        "/1",
        [
            ("2012-01-01", 0.10, LF_2012),
        ],
    ),
    f"{PV_NON_RESIDENTS}.plafond_prix_personnes_morales": (
        "/1",
        [
            ("2012-05-25", 0.05, LFC_2012),
        ],
    ),
    f"{PV_NON_RESIDENTS}.plafond_prix_personnes_physiques": (
        "/1",
        [
            ("2012-05-25", 0.025, LFC_2012),
        ],
    ),
}

# Séries dont des états antérieurs à la première date existent et ne sont pas versés.
INCOMPLETES = {
    f"{RETENUE}.taux_imputable",
    f"{RETENUE}.taux_titres_porteur_anonymes",
    f"{NON_RESIDENTS}.taux_revenus_capitaux_mobiliers",
}


def parametre(chemin):
    noeud = IMPOT_REVENU
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


def egal(lu, attendu):
    if attendu is None:
        return lu is None
    return lu == pytest.approx(attendu)


LECTURES = []
for chemin, (_, suite) in SERIES.items():
    for rang, (date, valeur, _) in enumerate(suite):
        LECTURES.append((chemin, date, valeur))
        if rang > 0:
            LECTURES.append((chemin, veille(date), suite[rang - 1][1]))


@pytest.mark.parametrize(("chemin", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(chemin, instant, attendu):
    assert egal(parametre(chemin)(instant), attendu)


@pytest.mark.parametrize("chemin", SERIES)
def test_rien_avant_la_premiere_date(chemin):
    premiere = SERIES[chemin][1][0][0]
    assert parametre(chemin)(veille(premiere)) is None


@pytest.mark.parametrize("chemin", SERIES)
def test_chaque_date_porte_sa_reference(chemin):
    p = parametre(chemin)
    suite = SERIES[chemin][1]
    dates = {date for date, _, _ in suite}
    references = {str(d): liste for d, liste in p.metadata["reference"].items()}
    assert {v.instant_str for v in p.values_list} == dates
    assert set(references) == dates
    for date, _, (fascicule, lien) in suite:
        liste = references[date]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert (
                "rticle" in reference["title"]
            ), f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert (
                fascicule in reference["note"]
            ), f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]


@pytest.mark.parametrize("chemin", SERIES)
def test_note_des_series_incompletes(chemin):
    """La note est portée à la première date de la série, seule date de `notes`."""
    notes = {
        str(d): liste
        for d, liste in parametre(chemin).metadata.get("notes", {}).items()
    }
    if chemin in INCOMPLETES:
        premiere = SERIES[chemin][1][0][0]
        assert notes == {
            premiere: [
                {"note": "Série incomplète : états antérieurs à 1990 non versés."}
            ]
        }
    else:
        assert notes == {}


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def test_les_sous_arbres_ne_portent_que_les_feuilles_attendues():
    feuilles = set()
    for racine in ("capitaux_mobiliers", "valeurs_mobilieres"):
        noeud = IMPOT_REVENU.children[racine]
        feuilles |= {
            d.name.removeprefix(f"{IMPOT_REVENU.name}.")
            for d in noeud.get_descendants()
            if not hasattr(d, "children")
        }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [
        IMPOT_REVENU.children["capitaux_mobiliers"],
        parametre(RETENUE),
        parametre(NON_RESIDENTS),
        IMPOT_REVENU.children["valeurs_mobilieres"],
        parametre(DISTRIBUES),
        parametre(JETONS),
        parametre(PLUS_VALUE),
        parametre(COTEES),
        parametre(PV_NON_RESIDENTS),
    ]
    for noeud in noeuds:
        assert set(noeud.children) == set(noeud.metadata["order"])
    ordre = IMPOT_REVENU.metadata["order"]
    assert "capitaux_mobiliers" in ordre
    assert "valeurs_mobilieres" in ordre


# État du droit à des dates repères, pour une personne physique résidente :
# (retenue imputable, retenue libératoire, titres au porteur anonymes hors obligations,
#  revenus distribués, plus-value taux, plus-value non cotés détention courte, franchise).
ETATS = [
    ("1990-01-01", 0.15, None, 0.35, None, None, None, None),
    ("1992-01-02", 0.15, None, 0.35, None, None, None, None),
    ("1997-01-01", 0.20, None, None, None, None, None, None),
    ("2004-01-01", 0.20, None, None, None, 0.10, None, 10000),
    ("2015-01-01", 0.20, None, None, 0.05, 0.10, None, 10000),
    ("2018-01-01", 0.20, None, None, 0.10, 0.10, None, 10000),
    ("2020-06-10", 0.20, None, None, 0.10, 0.10, None, 10000),
    ("2021-01-01", None, 0.20, None, 0.10, 0.10, None, 10000),
    ("2022-01-01", 0.20, None, None, 0.10, 0.10, None, 10000),
    ("2023-01-01", 0.20, None, None, 0.10, 0.10, 0.15, None),
    ("2026-01-01", 0.20, None, None, 0.10, 0.10, 0.15, None),
]


@pytest.mark.parametrize(
    (
        "instant",
        "imputable",
        "liberatoire",
        "anonymes",
        "distribues",
        "plus_value",
        "plus_value_courte",
        "franchise",
    ),
    ETATS,
)
def test_etats_aux_dates_reperes(
    instant,
    imputable,
    liberatoire,
    anonymes,
    distribues,
    plus_value,
    plus_value_courte,
    franchise,
):
    lus = [
        parametre(f"{RETENUE}.taux_imputable")(instant),
        parametre(f"{RETENUE}.taux_liberatoire")(instant),
        parametre(f"{RETENUE}.taux_titres_porteur_anonymes")(instant),
        parametre(f"{DISTRIBUES}.taux_retenue_source")(instant),
        parametre(f"{PLUS_VALUE}.taux")(instant),
        parametre(f"{PLUS_VALUE}.taux_non_cotes_detention_courte")(instant),
        parametre(f"{PLUS_VALUE}.franchise")(instant),
    ]
    attendus = [
        imputable,
        liberatoire,
        anonymes,
        distribues,
        plus_value,
        plus_value_courte,
        franchise,
    ]
    for lu, attendu in zip(lus, attendus):
        assert egal(lu, attendu), (instant, lus, attendus)


def test_seul_le_systeme_fiscal_lit_l_impot_sur_le_revenu():
    assert "impot_revenu" not in SOUS_ARBRES_PENSION
