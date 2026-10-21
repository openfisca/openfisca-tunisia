"""Temps de travail et congés : durée du travail, heures supplémentaires, congé annuel, jours
fériés, congé de paternité, jours fériés de la convention collective cadre.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : code du
travail de 1966 (en vigueur le 1er mai 1966, article premier de la loi n° 66-27), rectificatif de
l'article 113, loi n° 88-55 (5 juin 1988), loi n° 91-15 (date d'effet indéterminée entre le 3 et
le 7 mars 1991), loi n° 96-62 (31 juillet 1996), décrets-lois n° 2011-51 (16 juin 2011) et
n° 2021-11 (15 décembre 2021), loi n° 2024-44 (13 août 2024), convention collective cadre de 1973
et ses avenants n° 1 et n° 2. Sont éprouvés, feuille par feuille :

- la valeur la veille et le jour de chaque date d'effet, clôtures comprises ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du sous-arbre, et l'état du droit à des dates repères.

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

TEMPS_TRAVAIL = TunisiaTaxBenefitSystem().parameters.marche_travail.temps_travail

CODE_1966 = ("JORT n° 21 des 10-13 mai 1966", "/1966/1966F/Jo02166.pdf")
ART_445_1966 = ("JORT n° 22 des 17-20-24 mai 1966", "/1966/1966F/Jo02266.pdf")
RECTIFICATIF_1966 = ("JORT n° 37 des 30 août-2 septembre 1966", "/1966/1966F/Jo03766.pdf")
LOI_1988 = ("JORT n° 37 du 3 juin 1988", "/1988/1988F/Jo03788.pdf")
LOI_1991 = ("JORT n° 17 des 1er et 5 mars 1991", "/1991/1991F/Jo01791.pdf")
LOI_1996 = ("JORT n° 59 du 23 juillet 1996", "/1996/1996F/Jo05996.pdf")
DL_2011 = ("JORT n° 42 du 10 juin 2011", "/2011/2011F/Jo0422011.pdf")
DL_2021 = ("JORT n° 115 du 14 décembre 2021", "/2021/2021F/Jo1152021.pdf")
LOI_2024 = ("JORT n° 99 du 12 août 2024", "/2024/2024F/Jo0992024.pdf")
CC_1973 = ("JORT n° 21 des 25-29 mai-1er juin 1973", "/1973/1973F/Jo02173.pdf")
CC_1984 = ("JORT n° 13 du 15 février 1985", "/1985/1985F/Jo01385.pdf")
CC_1992 = ("JORT n° 12 du 12 février 1993", "/1993/1993F/Jo01293.pdf")

HS = "heures_supplementaires"
CA = "conge_annuel"

LISTE_1966 = ["1er mai", "1er juin", "25 juillet", "15 octobre"]
LISTE_1988 = ["20 mars", "1er mai", "25 juillet", "Aïd El Fitr", "Aïd El Idha"]
LISTE_1991 = ["20 mars", "1er mai", "25 juillet", "7 novembre", "Aïd El Fitr", "Aïd El Idha"]
LISTE_2011 = ["14 janvier", "20 mars", "1er mai", "25 juillet", "Aïd El Fitr", "Aïd El Idha"]
LISTE_2021 = ["17 décembre", "20 mars", "1er mai", "25 juillet", "Aïd El Fitr", "Aïd El Idha"]

# Chemin sous temps_travail : unité, et suite des (date, valeur, [textes]). None : clôture.
SERIES = {
    "duree.hebdomadaire_maximale": ("heure", [
        ("1966-05-01", 48, [CODE_1966]),
        ("1996-07-31", 48, [LOI_1996]),
    ]),
    "duree.hebdomadaire_plancher_reduction": ("heure", [
        ("1966-05-01", 40, [CODE_1966]),
        ("1996-07-31", 40, [LOI_1996]),
    ]),
    "duree.journaliere_maximale": ("heure", [
        ("1966-05-01", 9, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    "duree.hebdomadaire_plafond_heures_supplementaires": ("heure", [
        ("1966-05-01", 60, [CODE_1966]),
    ]),
    "duree.presence_hebdomadaire_maximale": ("heure", [
        ("1996-07-31", 64, [LOI_1996]),
    ]),
    "duree.agriculture_annuelle_maximale": ("heure", [
        ("1966-05-01", 2700, [CODE_1966]),
    ]),
    "duree.agriculture_jours_travail_effectif": ("day", [
        ("1966-05-01", 300, [CODE_1966]),
    ]),
    "duree.temps_partiel_part_maximale": ("/1", [
        ("1996-07-31", 0.70, [LOI_1996]),
    ]),
    f"{HS}.regime_48h": ("/1", [
        ("1966-05-01", 0.75, [CODE_1966]),
        ("1996-07-31", 0.75, [LOI_1996]),
    ]),
    f"{HS}.regime_40h.taux_premieres_heures": ("/1", [
        ("1966-05-01", 0.25, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    f"{HS}.regime_40h.taux_heures_suivantes": ("/1", [
        ("1966-05-01", 0.50, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    f"{HS}.regime_40h.nombre_premieres_heures": ("heure", [
        ("1966-05-01", 8, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    f"{HS}.regimes_inferieurs_48h.taux_jusqu_au_seuil": ("/1", [
        ("1996-07-31", 0.25, [LOI_1996]),
    ]),
    f"{HS}.regimes_inferieurs_48h.taux_au_dela_du_seuil": ("/1", [
        ("1996-07-31", 0.50, [LOI_1996]),
    ]),
    f"{HS}.regimes_inferieurs_48h.seuil": ("heure", [
        ("1996-07-31", 48, [LOI_1996]),
    ]),
    f"{HS}.temps_partiel": ("/1", [
        ("1996-07-31", 0.50, [LOI_1996]),
    ]),
    f"{HS}.agriculture": ("/1", [
        ("1966-05-01", 0.25, [CODE_1966]),
    ]),
    f"{CA}.jours_par_mois.adultes": ("day", [
        ("1966-05-01", 1, [CODE_1966]),
        ("1996-07-31", 1, [LOI_1996]),
    ]),
    f"{CA}.jours_par_mois.moins_18_ans": ("day", [
        ("1966-05-01", 2, [CODE_1966]),
        ("1996-07-31", 2, [LOI_1996]),
    ]),
    f"{CA}.jours_par_mois.de_18_a_20_ans": ("day", [
        ("1966-05-01", 1.5, [CODE_1966, RECTIFICATIF_1966]),
        ("1996-07-31", 1.5, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours_ouvrables.adultes": ("day", [
        ("1966-05-01", 12, [CODE_1966]),
        ("1996-07-31", 12, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours_ouvrables.moins_18_ans": ("day", [
        ("1966-05-01", 24, [CODE_1966]),
        ("1996-07-31", 24, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours_ouvrables.de_18_a_20_ans": ("day", [
        ("1966-05-01", 18, [CODE_1966, RECTIFICATIF_1966]),
        ("1996-07-31", 18, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours.adultes": ("day", [
        ("1966-05-01", 15, [CODE_1966]),
        ("1996-07-31", 15, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours.moins_18_ans": ("day", [
        ("1966-05-01", 30, [CODE_1966]),
        ("1996-07-31", 30, [LOI_1996]),
    ]),
    f"{CA}.plafond_jours.de_18_a_20_ans": ("day", [
        ("1966-05-01", 22, [CODE_1966, RECTIFICATIF_1966]),
        ("1996-07-31", 22, [LOI_1996]),
    ]),
    f"{CA}.anciennete.jours_ouvrables_par_periode": ("day", [
        ("1966-05-01", 1, [CODE_1966]),
    ]),
    f"{CA}.anciennete.duree_periode": ("year", [
        ("1966-05-01", 5, [CODE_1966]),
    ]),
    f"{CA}.anciennete.plafond_total_jours_ouvrables": ("day", [
        ("1966-05-01", 18, [CODE_1966]),
    ]),
    f"{CA}.mois_travail_effectif": ("day", [
        ("1966-05-01", 24, [CODE_1966]),
        ("1996-07-31", 26, [LOI_1996]),
    ]),
    f"{CA}.indemnite_diviseur.adultes": ("diviseur", [
        ("1966-05-01", 24, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    f"{CA}.indemnite_diviseur.moins_18_ans": ("diviseur", [
        ("1966-05-01", 12, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    f"{CA}.indemnite_diviseur.de_18_a_20_ans": ("diviseur", [
        ("1966-05-01", 16, [CODE_1966]),
        ("1996-07-31", None, [LOI_1996]),
    ]),
    "jours_feries.nombre": ("day", [
        ("1966-05-01", 4, [ART_445_1966]),
        ("1988-06-05", 5, [LOI_1988]),
        ("1991-03-03", None, [LOI_1991]),
        ("1991-03-07", 6, [LOI_1991]),
        ("2011-06-16", 6, [DL_2011]),
        ("2021-12-15", 6, [DL_2021]),
    ]),
    "jours_feries.liste": ("jour_ferie", [
        ("1966-05-01", LISTE_1966, [ART_445_1966]),
        ("1988-06-05", LISTE_1988, [LOI_1988]),
        ("1991-03-03", None, [LOI_1991]),
        ("1991-03-07", LISTE_1991, [LOI_1991]),
        ("2011-06-16", LISTE_2011, [DL_2011]),
        ("2021-12-15", LISTE_2021, [DL_2021]),
    ]),
    "jours_feries.indemnite_jour_ferie_travaille": ("/1", [
        ("1966-05-01", 1, [CODE_1966]),
    ]),
    "conge_paternite.duree": ("day", [
        ("1966-05-01", 1, [CODE_1966]),
        ("2024-08-13", 7, [LOI_2024]),
    ]),
    "conge_paternite.duree_majoree": ("day", [
        ("2024-08-13", 10, [LOI_2024]),
    ]),
    "conge_paternite.duree_enfant_mort_ne": ("day", [
        ("2024-08-13", 3, [LOI_2024]),
    ]),
    "conge_paternite.delai_prise": ("day", [
        ("1966-05-01", 7, [CODE_1966]),
        ("2024-08-13", 30, [LOI_2024]),
    ]),
    "convention_cadre.jours_feries": ("day", [
        ("1973-06-01", 7, [CC_1973]),
        ("1984-11-17", 9, [CC_1984]),
        ("1992-10-15", 9, [CC_1992]),
    ]),
    "convention_cadre.majoration_jour_ferie_travaille": ("/1", [
        ("1973-06-01", 1, [CC_1973]),
        ("1984-11-17", 1, [CC_1984]),
        ("1992-10-15", 1, [CC_1992]),
    ]),
}


def parametre(chemin):
    noeud = TEMPS_TRAVAIL
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


def egal(lu, attendu):
    if attendu is None:
        return lu is None
    if isinstance(attendu, list):
        return list(lu) == attendu
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
    for date, _, textes in suite:
        liste = references[date]
        assert len(liste) == len(textes), f"{chemin} au {date} : nombre de références"
        for reference, (fascicule, lien) in zip(liste, textes):
            assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"], f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]
            assert "Date d'effet" in reference["note"] or "rectificatif" in reference["title"]


@pytest.mark.parametrize("chemin", SERIES)
def test_aucune_note_d_incompletude(chemin):
    """Les séries commencent à l'entrée en vigueur du code ou au texte qui les crée."""
    assert not parametre(chemin).metadata.get("notes")


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def test_le_sous_arbre_ne_porte_que_les_feuilles_attendues():
    prefixe = f"{TEMPS_TRAVAIL.name}."
    feuilles = {
        d.name.removeprefix(prefixe)
        for d in TEMPS_TRAVAIL.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [TEMPS_TRAVAIL] + [d for d in TEMPS_TRAVAIL.get_descendants() if hasattr(d, "children")]
    for noeud in noeuds:
        assert list(noeud.metadata["order"]) and set(noeud.children) == set(noeud.metadata["order"]), noeud.name


def test_le_nombre_de_jours_feries_est_la_longueur_de_la_liste():
    for date, nombre, _ in SERIES["jours_feries.nombre"][1]:
        liste = parametre("jours_feries.liste")(date)
        assert (liste is None) if nombre is None else (len(liste) == nombre), date


# État du droit à des dates repères :
# (durée hebdomadaire maximale, journalière maximale, majoration du régime de 48 heures,
#  majoration du régime de 40 heures sur les premières heures (1966), premier taux des régimes
#  de moins de 48 heures (1996), majoration du temps partiel, mois de travail effectif en jours,
#  diviseur de l'indemnité de congé des adultes, jours fériés de la loi, de la convention cadre,
#  congé de paternité).
ETATS = [
    ("1966-05-01", 48, 9, 0.75, 0.25, None, None, 24, 24, 4, None, 1),
    ("1973-06-01", 48, 9, 0.75, 0.25, None, None, 24, 24, 4, 7, 1),
    ("1984-11-17", 48, 9, 0.75, 0.25, None, None, 24, 24, 4, 9, 1),
    ("1988-06-05", 48, 9, 0.75, 0.25, None, None, 24, 24, 5, 9, 1),
    ("1991-03-05", 48, 9, 0.75, 0.25, None, None, 24, 24, None, 9, 1),
    ("1991-03-07", 48, 9, 0.75, 0.25, None, None, 24, 24, 6, 9, 1),
    ("1996-07-30", 48, 9, 0.75, 0.25, None, None, 24, 24, 6, 9, 1),
    ("1996-07-31", 48, None, 0.75, None, 0.25, 0.50, 26, None, 6, 9, 1),
    ("2024-08-12", 48, None, 0.75, None, 0.25, 0.50, 26, None, 6, 9, 1),
    ("2024-08-13", 48, None, 0.75, None, 0.25, 0.50, 26, None, 6, 9, 7),
    ("2026-01-01", 48, None, 0.75, None, 0.25, 0.50, 26, None, 6, 9, 7),
]

LUS = [
    "duree.hebdomadaire_maximale",
    "duree.journaliere_maximale",
    f"{HS}.regime_48h",
    f"{HS}.regime_40h.taux_premieres_heures",
    f"{HS}.regimes_inferieurs_48h.taux_jusqu_au_seuil",
    f"{HS}.temps_partiel",
    f"{CA}.mois_travail_effectif",
    f"{CA}.indemnite_diviseur.adultes",
    "jours_feries.nombre",
    "convention_cadre.jours_feries",
    "conge_paternite.duree",
]


@pytest.mark.parametrize("etat", ETATS, ids=[e[0] for e in ETATS])
def test_etats_aux_dates_reperes(etat):
    instant, *attendus = etat
    lus = [parametre(chemin)(instant) for chemin in LUS]
    for chemin, lu, attendu in zip(LUS, lus, attendus):
        assert egal(lu, attendu), (instant, chemin, lu, attendu)
