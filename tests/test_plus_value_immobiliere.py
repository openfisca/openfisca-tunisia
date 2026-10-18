"""Plus-value immobilière : taux selon la durée de détention, durée qui sépare les deux taux,
retenue à la source sur le prix de cession, et exclusion du local d'habitation.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : loi de
finances pour 1995 (articles 55 et 100), loi n° 98-73 du 4 août 1998 (articles 1 et 3, exécutoire
le 17 août 1998), lois de finances pour 2005, 2013 et 2014, décret-loi n° 2022-79 (article 43).
Sont éprouvés, feuille par feuille :

- la valeur la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- la note des séries dont les états antérieurs ne sont pas versés ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du sous-arbre, et le système des pensions qui ne le charge pas.

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

PLUS_VALUE = (
    TunisiaTaxBenefitSystem().parameters.impot_revenu.foncier.plus_value_immobiliere
)

LF_1995 = ("JORT n° 103 des 30-31 décembre 1994", "/1994/1994F/Jo10394.pdf")
LOI_98_73 = ("JORT n° 64 du 11 août 1998", "/1998/1998F/Jo06498.pdf")
LF_2005 = ("JORT n° 105 du 31 décembre 2004", "/2004/2004F/Jo1052004.pdf")
LF_2013 = ("JORT n° 1 du 1er janvier 2013", "/2013/2013F/Jo0012013.pdf")
LF_2014 = ("JORT n° 105 du 31 décembre 2013", "/2013/2013F/Jo1052013.pdf")
LF_2023 = (
    "JORT n° 141 du 23 décembre 2022, édition arabe",
    "/2022/2022A/Ja1412022.pdf",
)

# Chemin : unité, et suite des (date, valeur, texte).
SERIES = {
    "taux_avant_seuil": (
        "/1",
        [
            ("1998-08-17", 0.10, LOI_98_73),
            ("2013-01-01", 0.15, LF_2013),
        ],
    ),
    "taux_apres_seuil": (
        "/1",
        [
            ("1998-08-17", 0.05, LOI_98_73),
            ("2013-01-01", 0.10, LF_2013),
        ],
    ),
    "duree_detention_seuil": (
        "year",
        [
            ("1998-08-17", 10, LOI_98_73),
            ("2013-01-01", 5, LF_2013),
        ],
    ),
    "taux_retenue_source": (
        "/1",
        [
            ("1995-01-01", 0.025, LF_1995),
            ("2013-01-01", 0.025, LF_2013),
        ],
    ),
    "exclusion_logement.superficie_maximum": (
        "m2",
        [
            ("1998-08-17", 1000, LOI_98_73),
            ("2005-01-01", 1000, LF_2005),
            ("2014-01-01", 1000, LF_2014),
        ],
    ),
    "exclusion_logement.prix_cession_seuil": (
        "currency",
        [
            ("2023-01-01", 500000, LF_2023),
        ],
    ),
}

# Séries dont des états antérieurs à la première date existent et ne sont pas versés.
INCOMPLETES = {"taux_avant_seuil", "taux_apres_seuil", "duree_detention_seuil"}


def parametre(chemin):
    noeud = PLUS_VALUE
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


LECTURES = []
for chemin, (_, suite) in SERIES.items():
    for rang, (date, valeur, _) in enumerate(suite):
        LECTURES.append((chemin, date, valeur))
        if rang > 0:
            LECTURES.append((chemin, veille(date), suite[rang - 1][1]))


@pytest.mark.parametrize(("chemin", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(chemin, instant, attendu):
    assert parametre(chemin)(instant) == pytest.approx(attendu)


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
    note = parametre(chemin).metadata.get("note")
    if chemin in INCOMPLETES:
        assert note == "Série incomplète : états antérieurs à 1998 non versés."
    else:
        assert note is None


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def test_le_sous_arbre_ne_porte_que_les_feuilles_attendues():
    feuilles = {
        d.name.removeprefix(f"{PLUS_VALUE.name}.")
        for d in PLUS_VALUE.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    for noeud in (PLUS_VALUE, PLUS_VALUE.children["exclusion_logement"]):
        assert set(noeud.children) == set(noeud.metadata["order"])


def test_etat_au_1er_janvier_2026():
    """15 % avant cinq ans, 10 % au-delà ; retenue de 2,5 % ; local de 1 000 m² vendu moins de
    500 000 dinars."""
    etat = PLUS_VALUE("2026-01-01")
    assert etat.taux_avant_seuil == pytest.approx(0.15)
    assert etat.taux_apres_seuil == pytest.approx(0.10)
    assert etat.duree_detention_seuil == 5
    assert etat.taux_retenue_source == pytest.approx(0.025)
    assert etat.exclusion_logement.superficie_maximum == 1000
    assert etat.exclusion_logement.prix_cession_seuil == 500000


def test_seul_le_systeme_fiscal_lit_l_impot_sur_le_revenu():
    assert "impot_revenu" not in SOUS_ARBRES_PENSION
