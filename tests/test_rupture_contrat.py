"""Rupture du contrat de travail : préavis, gratification de fin de service, dommages-intérêts
du licenciement abusif, contrat à durée déterminée, période d'essai, garantie des prestataires.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : code du
travail de 1966 (articles 14 et 22, en vigueur le 1er mai 1966), loi n° 94-29 (articles 14 bis,
22 et 23 bis, exécutoire le 1er mars 1994), loi n° 96-62 (article 6-4, exécutoire le
31 juillet 1996), loi n° 2025-9 (articles 6-3 et 6-4 nouveaux, exécutoire le 24 mai 2025),
arrêté du 23 septembre 2025 (article 2, exécutoire le 24 septembre 2025). Sont éprouvés, feuille
par feuille :

- la valeur la veille et le jour de chaque date d'effet, clôtures comprises ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- aucune série ne porte de note d'incomplétude : toutes commencent à l'institution de la règle
  dans le code du travail ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du nœud, et sa déclaration pour le système des pensions, qui lit aussi
  `marche_travail/`.

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

RUPTURE = TunisiaTaxBenefitSystem().parameters.marche_travail.rupture_contrat

CODE_1966 = ("JORT n° 20 des 3-6 mai 1966", "/1966/1966F/Jo02066.pdf")
LOI_1994 = ("JORT n° 15 du 22 février 1994", "/1994/1994F/Jo01594.pdf")
LOI_1996 = ("JORT n° 59 du 23 juillet 1996", "/1996/1996F/Jo05996.pdf")
LOI_2025 = ("JORT n° 61 du 23 mai 2025, édition arabe", "/2025/2025A/Ja0612025.pdf")
ARRETE_2025 = (
    "JORT n° 117 du 23 septembre 2025, édition arabe",
    "/2025/2025A/Ja1172025.pdf",
)

# Chemin sous rupture_contrat : unité, et suite des (date, valeur, texte). None : clôture.
SERIES = {
    "preavis.duree": (
        "month",
        [("1966-05-01", 1, CODE_1966), ("1994-03-01", 1, LOI_1994)],
    ),
    "preavis.duree_salaries_non_mensuels": (
        "day",
        [("1966-05-01", 8, CODE_1966), ("1994-03-01", None, LOI_1994)],
    ),
    "gratification_fin_service.jours_par_mois_service": (
        "day/month",
        [("1966-05-01", 1, CODE_1966), ("1994-03-01", 1, LOI_1994)],
    ),
    "gratification_fin_service.plafond": (
        "month",
        [("1966-05-01", 3, CODE_1966), ("1994-03-01", 3, LOI_1994)],
    ),
    "gratification_fin_service.anciennete_minimale": (
        "month",
        [("1966-05-01", 6, CODE_1966), ("1994-03-01", None, LOI_1994)],
    ),
    "dommages_interets.minimum_par_annee_anciennete": (
        "month/year",
        [("1994-03-01", 1, LOI_1994)],
    ),
    "dommages_interets.maximum_par_annee_anciennete": (
        "month/year",
        [("1994-03-01", 2, LOI_1994)],
    ),
    "dommages_interets.plafond": (
        "month",
        [("1994-03-01", 36, LOI_1994)],
    ),
    "dommages_interets.vice_procedure_minimum": (
        "month",
        [("1994-03-01", 1, LOI_1994)],
    ),
    "dommages_interets.vice_procedure_maximum": (
        "month",
        [("1994-03-01", 4, LOI_1994)],
    ),
    "contrat_duree_determinee.duree_maximale_hors_cas_recours": (
        "month",
        [("1996-07-31", 48, LOI_1996), ("2025-05-24", None, LOI_2025)],
    ),
    "periode_essai.duree_maximale": (
        "month",
        [("2025-05-24", 6, LOI_2025)],
    ),
    "periode_essai.renouvellements_maximum": (
        None,
        [("2025-05-24", 1, LOI_2025)],
    ),
    "entreprises_prestataires.garantie_financiere": (
        "/1",
        [("2025-09-24", 0.20, ARRETE_2025)],
    ),
}


def parametre(chemin):
    noeud = RUPTURE
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
            assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert reference["note"].startswith(fascicule), f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]
            assert "Date d'effet" in reference["note"], f"{chemin} au {date} : date d'effet non justifiée"


@pytest.mark.parametrize("chemin", SERIES)
def test_aucune_note_d_incompletude(chemin):
    assert dict(parametre(chemin).metadata.get("notes", {})) == {}


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata.get("unit")
    assert unite == SERIES[chemin][0]
    assert unite is None or unite in enregistrees


def test_le_noeud_ne_porte_que_les_feuilles_attendues():
    feuilles = {
        d.name.removeprefix(f"{RUPTURE.name}.")
        for d in RUPTURE.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [RUPTURE] + [RUPTURE.children[nom] for nom in RUPTURE.metadata["order"]]
    for noeud in noeuds:
        assert set(noeud.metadata["order"]) == set(noeud.children)


# État du droit à des dates repères :
# (préavis en mois, préavis des non-mensuels en jours, gratification en jours par mois,
#  plafond de la gratification, ancienneté minimale, dommages-intérêts maximaux par année,
#  plafond des dommages-intérêts, durée maximale hors cas de recours, période d'essai,
#  garantie financière).
ETATS = [
    ("1966-05-01", 1, 8, 1, 3, 6, None, None, None, None, None),
    ("1994-03-01", 1, None, 1, 3, None, 2, 36, None, None, None),
    ("1996-07-31", 1, None, 1, 3, None, 2, 36, 48, None, None),
    ("2025-05-23", 1, None, 1, 3, None, 2, 36, 48, None, None),
    ("2025-05-24", 1, None, 1, 3, None, 2, 36, None, 6, None),
    ("2025-09-24", 1, None, 1, 3, None, 2, 36, None, 6, 0.20),
    ("2026-01-01", 1, None, 1, 3, None, 2, 36, None, 6, 0.20),
]

CHEMINS_ETATS = [
    "preavis.duree",
    "preavis.duree_salaries_non_mensuels",
    "gratification_fin_service.jours_par_mois_service",
    "gratification_fin_service.plafond",
    "gratification_fin_service.anciennete_minimale",
    "dommages_interets.maximum_par_annee_anciennete",
    "dommages_interets.plafond",
    "contrat_duree_determinee.duree_maximale_hors_cas_recours",
    "periode_essai.duree_maximale",
    "entreprises_prestataires.garantie_financiere",
]


@pytest.mark.parametrize("etat", ETATS, ids=[etat[0] for etat in ETATS])
def test_etats_aux_dates_reperes(etat):
    instant, *attendus = etat
    lus = [parametre(chemin)(instant) for chemin in CHEMINS_ETATS]
    for lu, attendu in zip(lus, attendus):
        assert egal(lu, attendu), (instant, lus, attendus)


def test_le_systeme_des_pensions_lit_aussi_le_noeud():
    """`marche_travail/` est déclaré pour les deux systèmes : le nœud entre avec lui dans
    celui des pensions, que ce test n'instancie pas (il exige l'extra [pension])."""
    assert "marche_travail" in SOUS_ARBRES_PENSION
