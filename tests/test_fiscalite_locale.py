"""Fiscalité locale : taxe sur les immeubles bâtis et taxe sur les terrains non bâtis.

Les valeurs attendues sont écrites en clair, tirées du code de la fiscalité locale (loi n° 97-11
du 3 février 1997) et des six décrets des barèmes. Cinq choses sont éprouvées :

- les valeurs, la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu avant le 1er janvier 1997 pour ce que fixe le code,
  ni avant le 13 mars 1997 pour ce que fixe un décret ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- les unités, toutes enregistrées dans `units.yaml` ;
- le système des pensions ne charge pas ce sous-arbre.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import (
    RACINE_PARAMETRES,
    SOUS_ARBRES_FISCAL,
    SOUS_ARBRES_PENSION,
)

FISCALITE_LOCALE = TunisiaTaxBenefitSystem().parameters.fiscalite_locale

TIB = "taxe_immeubles_batis"
TNB = "taxe_terrains_non_batis"

# Fixé par le code : en vigueur le 1er janvier 1997 (loi n° 97-11, article 3), jamais modifié.
CODE = {
    f"{TIB}.taux_assiette": 0.02,
    f"{TIB}.taux.un_ou_deux_services": 0.08,
    f"{TIB}.taux.trois_ou_quatre_services": 0.10,
    f"{TIB}.taux.plus_de_quatre_services": 0.12,
    f"{TIB}.taux.plus_de_quatre_services_et_autres_services": 0.14,
    f"{TIB}.seuils_superficie.categorie_1": 100,
    f"{TIB}.seuils_superficie.categorie_2": 200,
    f"{TIB}.seuils_superficie.categorie_3": 400,
    f"{TNB}.taux_valeur_venale": 0.003,
}

# Fixé par décret : valeurs au 13 mars 1997, au 1er janvier 2008 et au 1er janvier 2017.
DECRETS = {
    f"{TIB}.prix_reference.categorie_1.minimum": (100, 100, 100),
    f"{TIB}.prix_reference.categorie_1.maximum": (150, 162, 178),
    f"{TIB}.prix_reference.categorie_2.minimum": (151, 163, 163),
    f"{TIB}.prix_reference.categorie_2.maximum": (200, 216, 238),
    f"{TIB}.prix_reference.categorie_3.minimum": (201, 217, 217),
    f"{TIB}.prix_reference.categorie_3.maximum": (250, 270, 297),
    f"{TIB}.prix_reference.categorie_4.minimum": (251, 271, 271),
    f"{TIB}.prix_reference.categorie_4.maximum": (300, 324, 356),
    f"{TNB}.tarif_m2.haute_densite": (0.300, 0.318, 0.385),
    f"{TNB}.tarif_m2.moyenne_densite": (0.090, 0.095, 0.115),
    f"{TNB}.tarif_m2.basse_densite": (0.030, 0.032, 0.040),
}

# Pour chaque décret : le jour de l'effet, puis la veille de l'effet du décret suivant.
PERIODES = (
    ("1997-03-13", "2007-12-31"),
    ("2008-01-01", "2016-12-31"),
    ("2017-01-01", "2026-12-31"),
)

VALEURS_CODE = [
    (chemin, instant, valeur)
    for chemin, valeur in CODE.items()
    for instant in ("1997-01-01", "2008-01-01", "2017-01-01", "2026-12-31")
]
VALEURS_DECRETS = [
    (chemin, instant, valeur)
    for chemin, valeurs in DECRETS.items()
    for valeur, periode in zip(valeurs, PERIODES)
    for instant in periode
]
AVANT_LA_SERIE = [(chemin, "1996-12-31") for chemin in CODE] + [
    (chemin, instant) for chemin in DECRETS for instant in ("1997-01-01", "1997-03-12")
]
DATES = [(chemin, {"1997-01-01"}) for chemin in CODE] + [
    (chemin, {"1997-03-13", "2008-01-01", "2017-01-01"}) for chemin in DECRETS
]
FASCICULES = {
    "1997-01-01": ("JORT n° 11 du 7 février 1997", "/1997/1997F/Jo01197.pdf"),
    "1997-03-13": ("JORT n° 19 du 7 mars 1997", "/1997/1997F/Jo01997.pdf"),
    "2008-01-01": ("JORT n° 40 du 18 mai 2007", "/2007/2007F/Jo0402007.pdf"),
    "2017-01-01": ("JORT n° 26 du 31 mars 2017", "/2017/2017F/Jo0262017.pdf"),
}


def parametre(chemin):
    noeud = FISCALITE_LOCALE
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def unite_attendue(chemin):
    if ".prix_reference." in chemin or ".tarif_m2." in chemin:
        return "currency/m2"
    if ".seuils_superficie." in chemin:
        return "m2"
    return "/1"


@pytest.mark.parametrize(("chemin", "instant", "attendu"), VALEURS_CODE + VALEURS_DECRETS)
def test_valeur(chemin, instant, attendu):
    assert parametre(chemin)(instant) == pytest.approx(attendu)


@pytest.mark.parametrize(("chemin", "instant"), AVANT_LA_SERIE)
def test_rien_avant_la_date_d_effet(chemin, instant):
    """Ni le code avant le 1er janvier 1997, ni un barème avant le 13 mars 1997."""
    assert parametre(chemin)(instant) is None


@pytest.mark.parametrize(("chemin", "dates"), DATES)
def test_chaque_date_porte_sa_reference(chemin, dates):
    p = parametre(chemin)
    references = p.metadata["reference"]
    assert {v.instant_str for v in p.values_list} == dates
    assert {str(d) for d in references} == dates
    for date, liste in references.items():
        fascicule, lien = FASCICULES[str(date)]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"], f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]


@pytest.mark.parametrize(("chemin", "dates"), DATES)
def test_unites(chemin, dates):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == unite_attendue(chemin)
    assert unite in enregistrees


def test_l_arbre_ne_porte_que_les_feuilles_attendues():
    feuilles = {
        d.name.removeprefix("fiscalite_locale.")
        for d in FISCALITE_LOCALE.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(CODE) | set(DECRETS)


def test_seul_le_systeme_fiscal_lit_la_fiscalite_locale():
    assert "fiscalite_locale" in SOUS_ARBRES_FISCAL
    assert "fiscalite_locale" not in SOUS_ARBRES_PENSION
