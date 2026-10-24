"""Droit de timbre, droits d'enregistrement hors mutations et taxe unique sur les assurances.

Les valeurs attendues sont écrites en clair, tirées des fascicules du Journal officiel : code des
droits d'enregistrement et de timbre (loi n° 93-53, JORT n° 39 de 1993), lois de finances pour
1994, 1997, 1999, 2002 à 2007, 2013, 2017, 2018, 2022, 2023 et 2026, lois de finances
complémentaires pour 2012 et 2014. Sont éprouvés, feuille par feuille :

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
import re

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

RACINE = TunisiaTaxBenefitSystem().parameters.fiscalite_indirecte

CODE = ("1993-05-17", "JORT n° 39 du 25 mai 1993", "/1993/1993F/Jo03993.pdf")
LF_1994 = ("1994-01-01", "JORT n° 100 du 31 décembre 1993", "/1993/1993F/Jo10093.pdf")
LF_1997 = ("1997-01-01", "JORT n° 105 du 31 décembre 1996", "/1996/1996F/Jo10596.pdf")
LF_1999 = (
    "1999-01-01",
    "JORT n° 104 des 29-31 décembre 1998",
    "/1998/1998F/Jo10498.pdf",
)
LF_2002 = ("2002-01-01", "JORT n° 104 du 28 décembre 2001", "/2001/2001F/Jo1042001.pdf")
LF_2003 = ("2003-01-01", "JORT n° 102 du 17 décembre 2002", "/2002/2002F/Jo1022002.pdf")
LF_2004 = ("2004-01-01", "JORT n° 104 du 30 décembre 2003", "/2003/2003F/Jo1042003.pdf")
LF_2005 = ("2005-01-01", "JORT n° 105 du 31 décembre 2004", "/2004/2004F/Jo1052004.pdf")
LF_2006 = ("2006-01-01", "JORT n° 101 du 20 décembre 2005", "/2005/2005F/Jo1012005.pdf")
LF_2007 = ("2007-01-01", "JORT n° 103 du 26 décembre 2006", "/2006/2006F/Jo1032006.pdf")
# Déposé le 19 mai 2012 ; date des notes communes n° 14/2012, 16/2012 et 25/2012.
LFC_2012 = ("2012-05-25", "JORT n° 39 du 18 mai 2012", "/2012/2012F/Jo0392012.pdf")
LF_2013 = ("2013-01-01", "JORT n° 1 du 1er janvier 2013", "/2013/2013F/Jo0012013.pdf")
# Déposé le 22 août 2014, exécutoire cinq jours après.
LFC_2014 = ("2014-08-27", "JORT n° 68 du 22 août 2014", "/2014/2014F/Jo0682014.pdf")
LF_2017 = ("2017-01-01", "JORT n° 105 du 27 décembre 2016", "/2016/2016F/Jo1052016.pdf")
LF_2018 = ("2018-01-01", "JORT n° 101 du 19 décembre 2017", "/2017/2017F/Jo1012017.pdf")
LF_2022 = ("2022-01-01", "JORT n° 119 du 28 décembre 2021", "/2021/2021F/Jo1192021.pdf")
# Éditions arabes : l'édition française n'est pas en ligne.
LF_2023 = ("2023-01-01", "JORT n° 141 du 23 décembre 2022", "/2022/2022A/Ja1412022.pdf")
LF_2026 = ("2026-01-01", "JORT n° 148 du 12 décembre 2025", "/2025/2025A/Ja1482025.pdf")


def suite(*couples):
    return [(texte[0], valeur, texte) for texte, valeur in couples]


def jugements(v1993, v2003, v2006, v2012):
    return suite(
        (CODE, v1993),
        (LF_2003, v2003),
        (LF_2006, v2006),
        (LFC_2012, v2012),
        (LF_2017, 40),
    )


def grandes_surfaces(valeur):
    return suite((LF_2026, valeur))


ENR = "droits_enregistrement."
TIM = "droit_timbre."

# Chemin sous fiscalite_indirecte : unité, et suite des (date, valeur, texte). None : clôture.
SERIES = {
    ENR + "droit_fixe.par_page": (
        "currency/page",
        suite((CODE, 10), (LF_2005, 15), (LFC_2012, 20), (LF_2018, 25), (LF_2022, 30)),
    ),
    ENR + "droit_fixe.actes_sans_tarif": (
        "currency/page",
        suite(
            (CODE, 5),
            (LF_2002, 10),
            (LF_2005, 15),
            (LFC_2012, 20),
            (LF_2018, 25),
            (LF_2022, 30),
        ),
    ),
    ENR + "minimum_perception.actes_mutations": (
        "currency",
        suite((CODE, 5), (LF_2003, 10), (LF_2006, 15), (LFC_2012, 20), (LF_2017, 40)),
    ),
    ENR + "minimum_perception.jugements.tribunaux_cantonaux": (
        "currency",
        jugements(5, 10, 15, 20),
    ),
    ENR + "minimum_perception.jugements.premiere_instance": (
        "currency",
        jugements(10, 20, 30, 40),
    ),
    ENR + "minimum_perception.jugements.appel_cassation": (
        "currency",
        jugements(20, 40, 60, 75),
    ),
    ENR + "fonds_commerce.cession": ("/1", suite((CODE, 0.025))),
    ENR + "fonds_commerce.location": ("/1", suite((CODE, 0.01))),
    ENR + "marches.taux": (
        "/1",
        suite((CODE, 0.027), (LF_1994, None), (LF_2013, 0.005)),
    ),
    ENR + "marches.droit_fixe_par_page": (
        "currency/page",
        suite((LF_1994, 10), (LF_2005, 15), (LFC_2012, 20), (LF_2013, None)),
    ),
    ENR + "marches.plafond": ("/1", suite((LF_2005, 0.02), (LF_2013, None))),
    TIM + "factures.par_facture": (
        "currency/unit",
        suite(
            (LF_2004, 0.2),
            (LF_2006, 0.3),
            (LFC_2012, 0.4),
            (LFC_2014, 0.5),
            (LF_2018, 0.6),
            (LF_2023, 1.0),
        ),
    ),
    TIM + "factures.grandes_surfaces.seuil_inferieur": (
        "currency",
        grandes_surfaces(50),
    ),
    TIM + "factures.grandes_surfaces.seuil_superieur": (
        "currency",
        grandes_surfaces(100),
    ),
    TIM + "factures.grandes_surfaces.de_50_a_100_dinars": (
        "currency/unit",
        grandes_surfaces(1.5),
    ),
    TIM + "factures.grandes_surfaces.plus_de_100_dinars": (
        "currency/unit",
        grandes_surfaces(2.0),
    ),
    TIM + "telephonie.par_carte_ou_recharge": (
        "currency/unit",
        suite((LF_2006, 0.3), (LF_2007, 0.3), (LFC_2012, None)),
    ),
    TIM + "telephonie.seuil_carte": ("currency", suite((LF_2007, 5), (LF_2018, None))),
    TIM + "telephonie.par_tranche_5_dinars": (
        "currency/tranche",
        suite((LF_2007, 0.3), (LFC_2012, 0.4), (LFC_2014, 0.5), (LF_2018, None)),
    ),
    TIM + "telephonie.par_dinar": (
        "/1",
        suite((LFC_2012, 0.08), (LFC_2014, 0.1), (LF_2018, 0.14)),
    ),
    TIM + "telephonie.supplement_recharge.montant": (
        "currency/unit",
        suite((LF_2026, 0.1)),
    ),
    TIM + "telephonie.supplement_recharge.seuil": ("currency", suite((LF_2026, 5))),
    TIM + "passeport.general": (
        "currency/unit",
        suite((CODE, 21), (LF_1999, 30), (LF_2004, 35), (LF_2006, 60), (LF_2013, 80)),
    ),
    TIM + "passeport.etudiants": (
        "currency/unit",
        suite((CODE, 7), (LF_1999, 10), (LF_2006, 20), (LF_2013, 25)),
    ),
    "taxe_unique_assurances.navigation_maritime_aerienne": (
        "/1",
        suite((LF_1997, 0.05), (LF_2018, 0.06)),
    ),
    "taxe_unique_assurances.autres_risques": (
        "/1",
        suite((LF_1997, 0.10), (LF_2018, 0.12)),
    ),
}

# Séries qui commencent à leur première date sourcée alors que des états antérieurs existent.
INCOMPLETES = {
    chemin: "Série incomplète : états antérieurs à 1993 non versés."
    for chemin, (_, serie) in SERIES.items()
    if serie[0][0] == CODE[0]
}
INCOMPLETES.update(
    {
        "taxe_unique_assurances.navigation_maritime_aerienne": "Série incomplète : états antérieurs à 1997 non versés.",
        "taxe_unique_assurances.autres_risques": "Série incomplète : états antérieurs à 1997 non versés.",
    }
)


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


@pytest.mark.parametrize(
    "chemin", [c for c, (_, s) in SERIES.items() if LFC_2012 in [t for _, _, t in s]]
)
def test_lfc_2012_dit_le_depot_et_la_date_retenue(chemin):
    note = parametre(chemin).metadata["reference"]["2012-05-25"][0]["note"]
    assert "19 mai 2012" in note
    assert "24 mai 2012" in note
    assert "n° 14/2012" in note


@pytest.mark.parametrize(
    "chemin", [c for c, (_, s) in SERIES.items() if LFC_2014 in [t for _, _, t in s]]
)
def test_lfc_2014_dit_le_depot(chemin):
    note = parametre(chemin).metadata["reference"]["2014-08-27"][0]["note"]
    assert "22 août 2014" in note
    assert "p. 2105" in note


@pytest.mark.parametrize("chemin", SERIES)
def test_note_des_series_incompletes(chemin):
    notes = {
        str(d): liste
        for d, liste in parametre(chemin).metadata.get("notes", {}).items()
    }
    if chemin in INCOMPLETES:
        premiere = SERIES[chemin][1][0][0]
        assert notes == {premiere: [{"note": INCOMPLETES[chemin]}]}
    else:
        assert notes == {}


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


def test_les_sous_arbres_ne_portent_que_les_feuilles_attendues():
    successions = {
        f for f in feuilles(parametre("droits_enregistrement")) if ".successions." in f
    }
    lues = (
        feuilles(parametre("droits_enregistrement")) - successions
        | feuilles(parametre("droit_timbre"))
        | feuilles(parametre("taxe_unique_assurances"))
    )
    assert lues == set(SERIES)


def test_ordre_declare():
    noeuds = [
        RACINE,
        parametre("droits_enregistrement"),
        parametre("droit_timbre"),
        parametre("taxe_unique_assurances"),
    ]
    for chemin in SERIES:
        noms = chemin.split(".")
        for rang in range(1, len(noms)):
            noeuds.append(parametre(".".join(noms[:rang])))
    for noeud in noeuds:
        assert set(noeud.children) == set(noeud.metadata["order"]), noeud.name


# État du droit à des dates repères : (droit fixe par page, minimum des actes, factures,
# téléphonie par dinar, passeport, TUA autres risques, marchés : taux, droit fixe).
ETATS = [
    ("1993-05-17", 10, 5, None, None, 21, None, 0.027, None),
    ("1994-01-01", 10, 5, None, None, 21, None, None, 10),
    ("2006-01-01", 15, 15, 0.3, None, 60, 0.10, None, 15),
    ("2012-05-25", 20, 20, 0.4, 0.08, 60, 0.10, None, 20),
    ("2013-01-01", 20, 20, 0.4, 0.08, 80, 0.10, 0.005, None),
    ("2014-08-27", 20, 20, 0.5, 0.1, 80, 0.10, 0.005, None),
    ("2018-01-01", 25, 40, 0.6, 0.14, 80, 0.12, 0.005, None),
    ("2026-01-01", 30, 40, 1.0, 0.14, 80, 0.12, 0.005, None),
]


@pytest.mark.parametrize(
    (
        "date",
        "droit_fixe",
        "minimum",
        "facture",
        "par_dinar",
        "passeport",
        "tua",
        "marches_taux",
        "marches_fixe",
    ),
    ETATS,
)
def test_etat_du_droit_aux_dates_reperes(
    date,
    droit_fixe,
    minimum,
    facture,
    par_dinar,
    passeport,
    tua,
    marches_taux,
    marches_fixe,
):
    lus = [
        parametre(ENR + "droit_fixe.par_page")(date),
        parametre(ENR + "minimum_perception.actes_mutations")(date),
        parametre(TIM + "factures.par_facture")(date),
        parametre(TIM + "telephonie.par_dinar")(date),
        parametre(TIM + "passeport.general")(date),
        parametre("taxe_unique_assurances.autres_risques")(date),
        parametre(ENR + "marches.taux")(date),
        parametre(ENR + "marches.droit_fixe_par_page")(date),
    ]
    attendus = [
        droit_fixe,
        minimum,
        facture,
        par_dinar,
        passeport,
        tua,
        marches_taux,
        marches_fixe,
    ]
    for lu, attendu in zip(lus, attendus):
        assert egal(lu, attendu)


def test_le_systeme_des_pensions_ne_charge_pas_la_fiscalite_indirecte():
    assert "fiscalite_indirecte" not in SOUS_ARBRES_PENSION
