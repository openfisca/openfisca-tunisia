"""Retenues à la source sur les sommes servies aux non-résidents, hors revenus de l'épargne :
rémunérations des non domiciliés ni établis (article 52, paragraphe I, alinéa b, troisième tiret)
et sommes revenant aux non-résidents établis sans déclaration d'existence (article 52,
paragraphe II, alinéa 4).

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : code de
1990 (article 52), lois de finances pour 1992 (article 31, exécutoire le 2 janvier 1992), 2003
(article 47), 2016 (article 28) et 2019 (article 50). Sont éprouvés, feuille par feuille : la
valeur la veille et le jour de chaque date, le début de chaque série, la référence de chaque
date, la note des séries incomplètes, les unités et la forme du sous-arbre.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Standard Library
import datetime

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES

NOEUD = TunisiaTaxBenefitSystem().parameters.impot_revenu.retenue_source_non_residents

CODE_1990 = ("JORT n° 1 des 2-5 janvier 1990", "/1990/1990F/Jo00190.pdf")
LF_1992 = ("JORT n° 90 du 31 décembre 1991", "/1991/1991F/Jo09091.pdf")
LF_2003 = ("JORT n° 102 du 17 décembre 2002", "/2002/2002F/Jo1022002.pdf")
LF_2016 = (
    "JORT n° 104 du 29 décembre 2015, édition arabe",
    "/2015/2015A/Ja1042015.pdf",
)
LF_2019 = (
    "JORT n° 104 du 28 décembre 2018, édition arabe",
    "/2018/2018A/Ja1042018.pdf",
)

SERIES = {
    "taux_remunerations": [
        ("1990-01-01", 0.15, CODE_1990),
        ("1992-01-02", 0.15, LF_1992),
        ("2003-01-01", 0.15, LF_2003),
    ],
    "taux_etablis_sans_declaration_existence": [
        ("2016-01-01", 0.15, LF_2016),
    ],
    "taux_etablis_sans_declaration_existence_regime_fiscal_privilegie": [
        ("2019-01-01", 0.25, LF_2019),
    ],
}

INCOMPLETES = {"taux_remunerations"}


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


LECTURES = []
for nom, suite in SERIES.items():
    for rang, (date, valeur, _) in enumerate(suite):
        LECTURES.append((nom, date, valeur))
        if rang > 0:
            LECTURES.append((nom, veille(date), suite[rang - 1][1]))


@pytest.mark.parametrize(("nom", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(nom, instant, attendu):
    assert NOEUD.children[nom](instant) == pytest.approx(attendu)


@pytest.mark.parametrize("nom", SERIES)
def test_rien_avant_la_premiere_date(nom):
    assert NOEUD.children[nom](veille(SERIES[nom][0][0])) is None


@pytest.mark.parametrize("nom", SERIES)
def test_chaque_date_porte_sa_reference(nom):
    p = NOEUD.children[nom]
    dates = {date for date, _, _ in SERIES[nom]}
    references = {str(d): liste for d, liste in p.metadata["reference"].items()}
    assert {v.instant_str for v in p.values_list} == dates
    assert set(references) == dates
    for date, _, (fascicule, lien) in SERIES[nom]:
        for reference in references[date]:
            assert "rticle" in reference["title"]
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"]
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]


@pytest.mark.parametrize("nom", SERIES)
def test_note_des_series_incompletes(nom):
    notes = {
        str(d): liste
        for d, liste in NOEUD.children[nom].metadata.get("notes", {}).items()
    }
    if nom in INCOMPLETES:
        assert notes == {
            SERIES[nom][0][0]: [
                {"note": "Série incomplète : états antérieurs à 1990 non versés."}
            ]
        }
    else:
        assert notes == {}


@pytest.mark.parametrize("nom", SERIES)
def test_unites(nom):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    assert NOEUD.children[nom].metadata["unit"] == "/1"
    assert "/1" in enregistrees


def test_le_noeud_ne_porte_que_les_feuilles_attendues_dans_l_ordre_declare():
    assert set(NOEUD.children) == set(SERIES)
    assert NOEUD.metadata["order"] == list(SERIES)
