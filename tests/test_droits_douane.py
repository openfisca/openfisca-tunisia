"""Droits de douane : redevance de prestations douanières, minimum de perception, taxe scanner.

Les valeurs attendues sont écrites en clair, tirées des fascicules du Journal officiel : lois de
finances pour 1987, 1988, 1994, 1998, 1999, 2013, 2014, 2018 et 2024. Sont éprouvés, feuille par
feuille :

- la valeur la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- la note des séries incomplètes ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du sous-arbre : aucune feuille hors de la liste, ordre déclaré.

Aucune variable ne calcule les droits de douane : ce test lit les paramètres. Un test YAML
n'asserte que des variables.
"""

# Standard Library
import datetime
import re

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

RACINE = TunisiaTaxBenefitSystem().parameters.fiscalite_indirecte.droits_douane

# Date d'effet, fascicule, lien (sous https://www.pist.tn/jort).
LF_1987 = (
    "1987-01-02",
    "JORT n° 78 des 30-31 décembre 1986",
    "/1986/1986F/Jo07886.pdf",
)
LF_1988 = (
    "1988-01-02",
    "JORT n° 91 des 29-31 décembre 1987",
    "/1987/1987F/Jo09187.pdf",
)
LF_1994 = ("1994-01-01", "JORT n° 100 du 31 décembre 1993", "/1993/1993F/Jo10093.pdf")
LF_1998 = (
    "1998-01-01",
    "JORT n° 104 des 30-31 décembre 1997",
    "/1997/1997F/Jo10497.pdf",
)
LF_1999 = (
    "1999-01-01",
    "JORT n° 104 des 29-31 décembre 1998",
    "/1998/1998F/Jo10498.pdf",
)
LF_2013 = ("2013-01-01", "JORT n° 1 du 1er janvier 2013", "/2013/2013F/Jo0012013.pdf")
LF_2014 = ("2014-01-01", "JORT n° 105 du 31 décembre 2013", "/2013/2013F/Jo1052013.pdf")
LF_2018 = ("2018-01-01", "JORT n° 101 du 19 décembre 2017", "/2017/2017F/Jo1012017.pdf")
# Édition arabe : l'édition française du fascicule n'est pas en ligne.
LF_2024 = ("2024-01-01", "JORT n° 144 du 12 décembre 2023", "/2023/2023A/Ja1442023.pdf")


def suite(*couples):
    return [(texte[0], valeur, texte) for texte, valeur in couples]


R = "redevance_prestations_douanieres."
M = "minimum_perception."
S = "taxe_scanner."

# Chemin sous droits_douane : unité, et suite des (date, valeur, texte).
SERIES = {
    R + "importation.taux_sur_droits_et_taxes": (
        "/1",
        suite((LF_1988, 0.015), (LF_1994, 0.02), (LF_1998, 0.03)),
    ),
    R + "importation.minimum_par_article": (
        "currency/unit",
        suite((LF_1988, 1), (LF_1994, 5), (LF_2013, 10), (LF_2024, 20)),
    ),
    R + "exportation.taux_sur_valeur_en_douane": (
        "/1",
        suite((LF_1988, 0.015), (LF_1999, 0.015)),
    ),
    R + "exportation.minimum_par_article": (
        "currency/unit",
        suite((LF_1988, 1), (LF_1999, 1)),
    ),
    R + "transit_terrestre.par_declaration": ("currency/unit", suite((LF_2014, 100))),
    M + "taux_general": ("/1", suite((LF_1987, 0.10), (LF_1988, 0.15))),
    M + "biens_equipement": ("/1", suite((LF_1987, 0.15), (LF_1988, 0.22))),
    S + "conteneur_20_pieds_au_plus": ("currency/unit", suite((LF_2018, 100))),
    S + "autre_unite": ("currency/unit", suite((LF_2018, 200))),
}

# Séries dont les états antérieurs ou postérieurs ne sont pas tous versés : la note est portée à
# la première date, et elle seule.
INCOMPLETES = {
    R
    + "transit_terrestre.par_declaration": "Série incomplète : états antérieurs à 2014 non versés.",
}
# Notes de contenu, portées à la première date : on vérifie qu'elles existent et ce qu'elles disent.
NOTES_DE_CONTENU = {
    R + "importation.taux_sur_droits_et_taxes": "montant des droits et taxes liquidés",
    R + "exportation.taux_sur_valeur_en_douane": "sans texte qui l'écrive en 1994",
    M + "taux_general": "Série incomplète",
    M + "biens_equipement": "plafond",
}


def parametre(chemin):
    noeud = RACINE
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
for chemin, (_, serie) in SERIES.items():
    for rang, (date, valeur, _) in enumerate(serie):
        LECTURES.append((chemin, date, valeur))
        if rang > 0:
            LECTURES.append((chemin, veille(date), serie[rang - 1][1]))


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
    serie = SERIES[chemin][1]
    dates = {date for date, _, _ in serie}
    references = {str(d): liste for d, liste in p.metadata["reference"].items()}
    assert {v.instant_str for v in p.values_list} == dates
    assert set(references) == dates
    for date, _, (_, fascicule, lien) in serie:
        liste = references[date]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert "rticle" in reference["title"], (
                f"{chemin} au {date} : article non cité"
            )
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"], (
                f"{chemin} au {date} : fascicule non cité"
            )
            assert re.search(r"\bpp?\. \d{2,4}", reference["note"]), (
                f"{chemin} au {date} : page non citée"
            )
            assert "Date d'effet" in reference["note"], (
                f"{chemin} au {date} : date d'effet non dite"
            )


@pytest.mark.parametrize("chemin", SERIES)
def test_notes_des_series(chemin):
    notes = {
        str(d): " ".join(n["note"] for n in liste)
        for d, liste in parametre(chemin).metadata.get("notes", {}).items()
    }
    premiere = SERIES[chemin][1][0][0]
    attendues = {INCOMPLETES.get(chemin), NOTES_DE_CONTENU.get(chemin)} - {None}
    if not attendues:
        assert notes == {}
        return
    assert set(notes) == {premiere}
    for attendue in attendues:
        assert attendue in notes[premiere]


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def feuilles(noeud):
    return {
        d.name.removeprefix(f"{RACINE.name}.")
        for d in noeud.get_descendants()
        if not hasattr(d, "children")
    }


def test_le_sous_arbre_ne_porte_que_les_feuilles_attendues():
    assert feuilles(RACINE) == set(SERIES)


def test_ordre_declare():
    noeuds = [RACINE]
    for chemin in SERIES:
        noms = chemin.split(".")
        for rang in range(1, len(noms)):
            noeuds.append(parametre(".".join(noms[:rang])))
    for noeud in noeuds:
        assert set(noeud.children) == set(noeud.metadata["order"]), noeud.name


# État du droit à des dates repères : taux à l'importation, minimum à l'importation, minimum
# de perception en tarif minimum, redevance de transit, taxe scanner (conteneur).
ETATS = [
    ("1987-06-01", None, None, 0.10, None, None),
    ("1988-01-02", 0.015, 1, 0.15, None, None),
    ("1994-01-01", 0.02, 5, 0.15, None, None),
    ("1999-01-01", 0.03, 5, 0.15, None, None),
    ("2013-01-01", 0.03, 10, 0.15, None, None),
    ("2014-01-01", 0.03, 10, 0.15, 100, None),
    ("2018-01-01", 0.03, 10, 0.15, 100, 100),
    ("2024-01-01", 0.03, 20, 0.15, 100, 100),
]


@pytest.mark.parametrize(
    ("date", "taux", "minimum", "minimum_perception", "transit", "scanner"), ETATS
)
def test_etat_du_droit_aux_dates_reperes(
    date, taux, minimum, minimum_perception, transit, scanner
):
    lus = [
        parametre(R + "importation.taux_sur_droits_et_taxes")(date),
        parametre(R + "importation.minimum_par_article")(date),
        parametre(M + "taux_general")(date),
        parametre(R + "transit_terrestre.par_declaration")(date),
        parametre(S + "conteneur_20_pieds_au_plus")(date),
    ]
    for lu, attendu in zip(lus, [taux, minimum, minimum_perception, transit, scanner]):
        assert egal(lu, attendu)


def test_le_systeme_des_pensions_ne_charge_pas_la_fiscalite_indirecte():
    assert "fiscalite_indirecte" not in SOUS_ARBRES_PENSION
