"""Droit d'enregistrement sur les successions : tarif par degré de parenté, abattements,
superficie de l'habitation principale exonérée, forfait des frais funéraires.

Les valeurs attendues sont écrites en clair, tirées de la loi de finances pour 1969 (article
14), de celle pour 1975 (articles 29 et 30), de celle pour 1984 (article 12), du code des droits d'enregistrement et de timbre de 1993
(articles 20, 49, 51 et 53) et de la loi n° 98-73 du 4 août 1998 (articles 8 à 10). Sont
éprouvés :

- les valeurs, la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu avant sa première date ;
- les tranches du tarif : six de 1969 au 16 mai 1993 (bornes et taux de 1969, 1975 et 1984), une seule depuis le 17 mai 1993 ;
- chaque date porte sa référence : texte, article, fascicule, page et lien ;
- les unités, toutes enregistrées dans `units.yaml` ;
- l'ordre déclaré de chaque nœud nomme tous ses enfants ;
- le système des pensions ne charge pas ce sous-arbre.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

SUCCESSIONS = TunisiaTaxBenefitSystem().parameters.fiscalite_indirecte.droits_enregistrement.successions

SEUILS_1984 = [0, 5000, 10000, 15000, 45000, 90000]
SEUILS_1975 = [0, 1000, 2000, 3000, 9000, 18000]
SEUILS_1969 = [0, 500, 1000, 2000, 6000, 12000]
SEUILS_1969_LIGNE_DIRECTE = [0, 500, 1000, 2000, 8000, 12000]

# Taux par tranche de la loi de finances pour 1969, article 14 (JORT n° 55/1968, pp. 1371-1372),
# et de celle pour 1975, article 29 (JORT n° 80/1974, p. 2916 ; éd. ar. p. 3221).
TARIF_1969 = {
    "ligne_directe_epoux": [0.07, 0.10, 0.115, 0.145, 0.18, 0.23],
    "freres_soeurs": [0.23, 0.31, 0.36, 0.43, 0.50, 0.65],
    "oncles_neveux_cousins": [0.47, 0.53, 0.58, 0.65, 0.72, 0.94],
    "au_dela_quatrieme_degre": [0.62, 0.65, 0.72, 0.79, 0.87, 1.00],
}
TARIF_1975 = {
    "ligne_directe_epoux": [0.06, 0.08, 0.09, 0.12, 0.15, 0.18],
    "freres_soeurs": [0.23, 0.31, 0.36, 0.43, 0.50, 0.65],
    "oncles_neveux_cousins": [0.47, 0.53, 0.58, 0.65, 0.72, 0.94],
    "au_dela_quatrieme_degre": [0.62, 0.65, 0.72, 0.79, 0.87, 1.00],
}

# Taux par tranche de la loi de finances pour 1984, article 12 (JORT n° 86/1983, p. 3372),
# puis taux unique du code (1993) et de la loi n° 98-73 (1998).
TARIF = {
    "ligne_directe_epoux": ([0.06, 0.08, 0.10, 0.13, 0.18, 0.25], 0.05, 0.025),
    "freres_soeurs": ([0.20, 0.25, 0.30, 0.36, 0.42, 0.50], 0.05, 0.05),
    "oncles_neveux_cousins": ([0.25, 0.35, 0.45, 0.55, 0.65, 0.75], 0.25, 0.25),
    "au_dela_quatrieme_degre": ([0.35, 0.45, 0.55, 0.65, 0.75, 0.85], 0.35, 0.35),
}

# Feuilles : (première date, [(veille, jour, valeur avant, valeur après), ...]).
FEUILLES = {
    "abattement.par_enfant_ascendant_conjoint": (
        "1975-01-02",
        [("1975-01-01", "1975-01-02", None, 2000), ("1998-08-16", "1998-08-17", 2000, 5000)],
    ),
    "abattement.plafond": (
        "1975-01-02",
        [("1975-01-01", "1975-01-02", None, 12000), ("1998-08-16", "1998-08-17", 12000, 30000)],
    ),
    "abattement.supplement_heritier_handicape": (
        "1993-05-17",
        [("1993-05-16", "1993-05-17", None, 4000), ("1998-08-16", "1998-08-17", 4000, 10000)],
    ),
    "habitation_principale_superficie_maximum": (
        "1993-05-17",
        [("1993-05-16", "1993-05-17", None, 1000)],
    ),
    "frais_funeraires_forfait": (
        "1993-05-17",
        [("1993-05-16", "1993-05-17", None, 500)],
    ),
}

# Dates portant une référence, et le fascicule et le lien attendus.
FASCICULES = {
    "1969-01-02": ("JORT n° 55 du 31 décembre 1968", "/1968/1968F/Jo05568.pdf"),
    "1975-01-02": ("JORT n° 80 du 31 décembre 1974", "/1974/1974F/Jo08074.pdf"),
    "1984-01-01": ("JORT n° 86 du 30 décembre 1983", "/1983/1983F/Jo08683.pdf"),
    "1993-05-17": ("JORT n° 39 du 25 mai 1993", "/1993/1993F/Jo03993.pdf"),
    "1998-08-17": ("JORT n° 64 du 11 août 1998", "/1998/1998F/Jo06498.pdf"),
}

DATES = {
    **{
        f"tarif.{nom}": {"1969-01-02", "1975-01-02", "1984-01-01", "1993-05-17"} | ({"1998-08-17"} if nom in ("ligne_directe_epoux", "freres_soeurs") else set())
        for nom in TARIF
    },
    "abattement.par_enfant_ascendant_conjoint": {"1975-01-02", "1993-05-17", "1998-08-17"},
    "abattement.plafond": {"1975-01-02", "1993-05-17", "1998-08-17"},
    "abattement.supplement_heritier_handicape": {"1993-05-17", "1998-08-17"},
    "habitation_principale_superficie_maximum": {"1993-05-17"},
    "frais_funeraires_forfait": {"1993-05-17"},
}

UNITES = {
    "abattement.par_enfant_ascendant_conjoint": "currency",
    "abattement.plafond": "currency",
    "abattement.supplement_heritier_handicape": "currency",
    "habitation_principale_superficie_maximum": "m2",
    "frais_funeraires_forfait": "currency",
}


def parametre(chemin):
    noeud = SUCCESSIONS
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


@pytest.mark.parametrize("nom", TARIF)
def test_rien_avant_1969(nom):
    bareme = parametre(f"tarif.{nom}")("1969-01-01")
    assert bareme.thresholds == []
    assert bareme.rates == []


@pytest.mark.parametrize("nom", TARIF)
@pytest.mark.parametrize(
    ("instant", "seuils", "taux"),
    [
        ("1969-01-02", None, TARIF_1969),
        ("1974-12-31", None, TARIF_1969),
        ("1975-01-01", None, TARIF_1969),
        ("1975-01-02", SEUILS_1975, TARIF_1975),
        ("1983-12-31", SEUILS_1975, TARIF_1975),
    ],
)
def test_six_tranches_de_1969_et_de_1975(nom, instant, seuils, taux):
    if seuils is None:
        seuils = SEUILS_1969_LIGNE_DIRECTE if nom == "ligne_directe_epoux" else SEUILS_1969
    bareme = parametre(f"tarif.{nom}")(instant)
    assert bareme.thresholds == seuils
    assert bareme.rates == pytest.approx(taux[nom])


@pytest.mark.parametrize("nom", TARIF)
@pytest.mark.parametrize("instant", ["1984-01-01", "1993-05-16"])
def test_six_tranches_de_1984_au_code(nom, instant):
    bareme = parametre(f"tarif.{nom}")(instant)
    assert bareme.thresholds == SEUILS_1984
    assert bareme.rates == pytest.approx(TARIF[nom][0])


@pytest.mark.parametrize("nom", TARIF)
@pytest.mark.parametrize(
    ("instant", "rang"),
    [("1993-05-17", 1), ("1998-08-16", 1), ("1998-08-17", 2), ("2026-01-01", 2)],
)
def test_taux_unique_depuis_le_code(nom, instant, rang):
    bareme = parametre(f"tarif.{nom}")(instant)
    assert bareme.thresholds == [0]
    assert bareme.rates == pytest.approx([TARIF[nom][rang]])


@pytest.mark.parametrize("chemin", FEUILLES)
def test_rien_avant_la_premiere_date(chemin):
    premiere, _ = FEUILLES[chemin]
    assert parametre(chemin)(premiere) is not None
    veille = FEUILLES[chemin][1][0][0]
    assert parametre(chemin)(veille) is None


@pytest.mark.parametrize(
    ("chemin", "veille", "jour", "avant", "apres"),
    [(chemin, *bornes) for chemin, (_, liste) in FEUILLES.items() for bornes in liste],
)
def test_la_veille_et_le_jour(chemin, veille, jour, avant, apres):
    p = parametre(chemin)
    assert p(veille) == avant
    assert p(jour) == apres


@pytest.mark.parametrize("chemin", DATES)
def test_chaque_date_porte_sa_reference(chemin):
    p = parametre(chemin)
    references = p.metadata["reference"]
    assert {str(d) for d in references} == DATES[chemin]
    for date, liste in references.items():
        fascicule, lien = FASCICULES[str(date)]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"], f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]


@pytest.mark.parametrize("chemin", DATES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    metadata = parametre(chemin).metadata
    if chemin.startswith("tarif."):
        unites = [metadata["threshold_unit"], metadata["rate_unit"]]
        assert unites == ["currency", "/1"]
    else:
        unites = [metadata["unit"]]
        assert unites == [UNITES[chemin]]
    assert set(unites) <= enregistrees


def test_ordre_des_noeuds():
    for noeud in (SUCCESSIONS, SUCCESSIONS.tarif, SUCCESSIONS.abattement):
        assert set(noeud.children) == set(noeud.metadata["order"])


def test_le_systeme_des_pensions_ne_charge_pas_ce_sous_arbre():
    assert "fiscalite_indirecte" not in SOUS_ARBRES_PENSION
