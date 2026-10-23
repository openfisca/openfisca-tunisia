"""Travail domestique (loi n° 2021-37 du 16 juillet 2021) : durée, pause, congé annuel, congés pour
événements familiaux, régime du salaire minimum.

Les valeurs attendues sont écrites en clair, tirées de la loi lue au Journal officiel : articles 11, 13,
14 et 19 (JORT n° 68 du 30 juillet 2021, pp. 2007-2008), entrée en vigueur à l'article 29 : « dans un
délai de six mois à compter de sa publication », soit le 30 janvier 2022. Sont éprouvés, feuille par
feuille :

- la valeur la veille et le jour de la date d'effet ;
- le début de chaque série : rien n'est lu la veille de la première date ;
- la référence : texte, article, fascicule, page, lien, calcul de la date d'effet ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du nœud : feuilles attendues, ordre déclaré.

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

DOMESTIQUE = TunisiaTaxBenefitSystem().parameters.marche_travail.temps_travail.travail_domestique

EFFET = "2022-01-30"
FASCICULE = "JORT n° 68 du 30 juillet 2021"
LIEN = "https://www.pist.tn/jort/2021/2021F/Jo0682021.pdf"

# Chemin sous travail_domestique : unité, valeur au 30 janvier 2022, article cité, page.
SERIES = {
    "duree.hebdomadaire_maximale_employeur_unique": ("heure", 48, "13", "p. 2007"),
    "duree.journaliere_maximale_employeur_unique": ("heure", 10, "13", "p. 2007"),
    "duree.journaliere_maximale_employeurs_multiples": ("heure", 8, "19", "p. 2008"),
    "duree.journaliere_maximale_heures_supplementaires_comprises_employeurs_multiples": (
        "heure", 10, "19", "p. 2008"),
    "duree.pause_dejeuner": ("heure", 1, "13", "p. 2007"),
    "conge_annuel.jours_par_mois_adultes": ("day", 1, "14", "p. 2007"),
    "conge_annuel.jours_par_mois_de_18_a_20_ans": ("day", 1.5, "14", "p. 2007"),
    "conge_annuel.plafond_jours_adultes": ("day", 15, "14", "p. 2007"),
    "conge_annuel.plafond_jours_de_18_a_20_ans": ("day", 22, "14", "p. 2007"),
    "conge_annuel.plafond_jours_ouvres_adultes": ("day", 12, "14", "p. 2007"),
    "conge_annuel.plafond_jours_ouvres_de_18_a_20_ans": ("day", 18, "14", "p. 2007"),
    "conges_evenements_familiaux.deces_conjoint_pere_mere_enfant": ("day", 3, "14", "p. 2007"),
    "conges_evenements_familiaux.deces_frere_soeur_petit_enfant_grand_parent": (
        "day", 2, "14", "p. 2007"),
    "conges_evenements_familiaux.mariage_travailleur": ("day", 7, "14", "p. 2007"),
    "conges_evenements_familiaux.circoncision_enfant": ("day", 1, "14", "p. 2007"),
    "conges_evenements_familiaux.mariage_enfant": ("day", 2, "14", "p. 2007"),
    "regime_salaire_minimum.heures_hebdomadaires": ("heure", 48, "11", "p. 2007"),
}


def parametre(chemin):
    noeud = DOMESTIQUE
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


@pytest.mark.parametrize("chemin", SERIES)
def test_valeur_le_jour_de_l_entree_en_vigueur(chemin):
    assert parametre(chemin)(EFFET) == pytest.approx(SERIES[chemin][1])
    assert parametre(chemin)("2026-01-01") == pytest.approx(SERIES[chemin][1])


@pytest.mark.parametrize("chemin", SERIES)
def test_rien_la_veille(chemin):
    assert parametre(chemin)(veille(EFFET)) is None


@pytest.mark.parametrize("chemin", SERIES)
def test_la_reference_cite_l_article_la_page_et_le_calcul_de_la_date(chemin):
    _, _, article, page = SERIES[chemin]
    p = parametre(chemin)
    assert {v.instant_str for v in p.values_list} == {EFFET}
    references = p.metadata["reference"][EFFET]
    assert len(references) == 1
    reference = references[0]
    assert reference["title"].startswith("Loi n° 2021-37 du 16 juillet 2021")
    assert f"article {article}" in reference["title"]
    assert reference["href"] == LIEN
    assert reference["note"].startswith(f"{FASCICULE}, {page}.")
    assert "Date d'effet : article 29" in reference["note"]
    assert "30 janvier 2022" in reference["note"]


@pytest.mark.parametrize("chemin", SERIES)
def test_aucune_note_d_incompletude(chemin):
    assert not parametre(chemin).metadata.get("notes")


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def test_le_noeud_ne_porte_que_les_feuilles_attendues():
    prefixe = f"{DOMESTIQUE.name}."
    feuilles = {
        d.name.removeprefix(prefixe)
        for d in DOMESTIQUE.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [DOMESTIQUE] + [d for d in DOMESTIQUE.get_descendants() if hasattr(d, "children")]
    for noeud in noeuds:
        assert list(noeud.metadata["order"])
        assert set(noeud.children) == set(noeud.metadata["order"]), noeud.name


def test_le_plafond_ouvre_ne_depasse_pas_le_plafond_en_jours():
    """12 jours ouvrés dans 15 jours ; 18 dans 22 : la loi enferme les premiers dans les seconds."""
    for age in ("adultes", "de_18_a_20_ans"):
        ouvres = parametre(f"conge_annuel.plafond_jours_ouvres_{age}")(EFFET)
        jours = parametre(f"conge_annuel.plafond_jours_{age}")(EFFET)
        assert ouvres < jours
