"""Fiscalité locale : taxe sur les immeubles bâtis, taxe sur les terrains non bâtis,
contribution au fonds de l'habitat, taxe sur les établissements à caractère industriel, commercial
ou professionnel, taxe hôtelière, taxe sur les spectacles, contribution des propriétaires
riverains, droit de licence et contribution aux parkings collectifs.

Les valeurs attendues sont écrites en clair, tirées du code de la fiscalité locale (loi n° 97-11
du 3 février 1997), des décrets des barèmes et des lois de finances. Pour les deux taxes sur les
immeubles, cinq choses sont éprouvées :

- les valeurs, la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu avant le 1er janvier 1997 pour ce que fixe le code,
  ni avant le 13 mars 1997 pour ce que fixe un décret ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- les unités, toutes enregistrées dans `units.yaml` ;
- le système des pensions ne charge pas ce sous-arbre.

Pour tout le reste — taxe sur les établissements, taxe hôtelière, pénalité de retard et
dégrèvement partiel de la taxe sur les immeubles bâtis, contribution au fonds de l'habitat,
chapitres V à VII du code, parkings —, la table `SERIES` donne, feuille par feuille, chaque date, sa valeur (ou la clôture, `None`) et le fascicule de sa référence ; sont
éprouvés la forme de l'arbre, les comptes, les valeurs la veille et le jour de chaque date, les
clôtures, les références, les unités, et la croissance des barèmes d'un décret au suivant.

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


# --- Taxe sur les établissements et taxe hôtelière -----------------------------------------------

TCL = "taxe_etablissements"
TH = "taxe_hoteliere"

# Fascicule de chaque source : mention attendue dans la note, et fin du lien.
CODE_1997 = ("JORT n° 11 du 7 février 1997", "/1997/1997F/Jo01197.pdf")
LF_1997 = ("JORT n° 105 du 31 décembre 1996", "/1996/1996F/Jo10596.pdf")
DECRETS_1997 = ("JORT n° 19 du 7 mars 1997", "/1997/1997F/Jo01997.pdf")
DECRET_2003 = ("JORT n° 49 du 20 juin 2003", "/2003/2003F/Jo0492003.pdf")
DECRET_2006 = ("JORT n° 2 du 5 janvier 2007", "/2007/2007F/Jo0022007.pdf")
DECRET_2007 = ("JORT n° 40 du 18 mai 2007", "/2007/2007F/Jo0402007.pdf")
LFC_2012 = ("JORT n° 39 du 18 mai 2012", "/2012/2012F/Jo0392012.pdf")
LF_2013 = ("JORT n° 1 du 1er janvier 2013", "/2013/2013F/Jo0012013.pdf")
LF_2014 = ("JORT n° 105 du 31 décembre 2013", "/2013/2013F/Jo1052013.pdf")
DECRET_2017 = ("JORT n° 26 du 31 mars 2017", "/2017/2017F/Jo0262017.pdf")
DECRET_SPECTACLES = ("JORT n° 26 du 1er avril 1997", "/1997/1997F/Jo02697.pdf")
LF_2002 = ("JORT n° 104 du 28 décembre 2001", "/2001/2001F/Jo1042001.pdf")
LOI_2002_76 = ("JORT n° 61 du 26 juillet 2002", "/2002/2002F/Jo0612002.pdf")
LF_2003 = ("JORT n° 102 du 17 décembre 2002", "/2002/2002F/Jo1022002.pdf")
LF_2005 = ("JORT n° 105 du 31 décembre 2004", "/2004/2004F/Jo1052004.pdf")
LF_2007 = ("JORT n° 103 du 26 décembre 2006", "/2006/2006F/Jo1032006.pdf")
LF_2021 = ("JORT n° 128 du 25 décembre 2020", "/2020/2020F/Jo1282020.pdf")
LF_2022 = ("JORT n° 119 du 28 décembre 2021", "/2021/2021F/Jo1192021.pdf")
# Édition arabe : l'édition française de ce fascicule n'est pas en ligne.
LF_2023 = ("JORT n° 141 du 23 décembre 2022", "/2022/2022A/Ja1412022.pdf")

# Minimum de la taxe sur les établissements, en dinars par mètre carré : pour chaque catégorie
# d'usage, les colonnes « Taux 8 % », « 10 % », « 12 % » et « 14 % » des trois décrets.
TAUX_TIB = (8, 10, 12, 14)
MINIMUM = {
    1: ((0.760, 0.950, 1.140, 1.330), (0.815, 1.020, 1.220, 1.425), (0.900, 1.125, 1.345, 1.570)),
    2: ((0.520, 0.650, 0.780, 0.910), (0.560, 0.700, 0.835, 0.975), (0.620, 0.770, 0.920, 1.075)),
    3: ((0.640, 0.800, 0.960, 1.120), (0.685, 0.860, 1.030, 1.200), (0.755, 0.950, 1.135, 1.320)),
    4: ((0.840, 1.050, 1.260, 1.470), (0.900, 1.125, 1.350, 1.575), (0.990, 1.240, 1.485, 1.735)),
}

# Feuille -> suite de (date d'effet, valeur ou None pour une clôture, fascicule).
SERIES = {
    f"{TCL}.taux.chiffre_affaires_brut_local": (
        ("1997-01-01", 0.002, CODE_1997), ("2014-01-01", None, LF_2014)),
    f"{TCL}.taux.chiffre_affaires_brut": (("2014-01-01", 0.002, LF_2014),),
    f"{TCL}.taux.exportation_et_non_residents": (("2014-01-01", 0.001, LF_2014),),
    f"{TCL}.taux.produits_prix_homologues": (("2013-01-01", 0.001, LF_2013),),
    f"{TCL}.taux.impot_regime_1997": (
        ("1997-01-01", 0.25, CODE_1997), ("2013-01-01", None, LF_2013)),
    f"{TCL}.taux.impot_regime_2013": (("2013-01-01", 0.25, LF_2013),),
    f"{TCL}.maximum": (
        ("1997-03-13", 50000, DECRETS_1997), ("2003-06-26", 60000, DECRET_2003),
        ("2007-01-01", 100000, DECRET_2006), ("2012-01-01", None, LFC_2012)),
    f"{TCL}.seuil_affectation_excedent": (
        ("2013-01-01", 100000, LF_2013), ("2021-01-01", 100000, LF_2021)),
    f"{TCL}.part_impot_auto_entrepreneur": (("2023-01-01", 0.2, LF_2023),),
    f"{TH}.taux": (("1997-01-01", 0.02, CODE_1997),),
    f"{TH}.part_affectee_fonds": (("1997-01-01", 0.5, LF_1997),),
}
SERIES.update({
    f"{TCL}.minimum.categorie_{n}.taux_{t}": (
        ("1997-03-13", bareme[0][i], DECRETS_1997),
        ("2008-01-01", bareme[1][i], DECRET_2007),
        ("2017-01-01", bareme[2][i], DECRET_2017),
    )
    for n, bareme in MINIMUM.items()
    for i, t in enumerate(TAUX_TIB)
})

# --- Compléments : pénalité, dégrèvement, fonds de l'habitat, chapitres V à VII, parkings ---------

FNAH = "contribution_fonds_amelioration_habitat"
SPECTACLES = "taxe_spectacles"
RIVERAINS = "contribution_riverains"
LICENCE = "droit_licence"
PARKINGS = "contribution_parkings"

# Droit de licence, en dinars par an, par catégorie d'établissement (décret n° 97-434).
TARIF_LICENCE = {1: 25, 2: 150, 3: 300}
# Parkings, en dinars par place. 1997 : selon la population. 2003 : pour chaque part de places
# manquantes, selon la population (au plus 50 000 ; 50 000 à 100 000 ; plus de 100 000).
PARKINGS_1997 = {
    "population_20000_a_50000": 100,
    "population_50000_a_100000": 250,
    "population_plus_de_100000": 500,
}
POPULATIONS_2003 = (
    "population_jusqu_a_50000", "population_50000_a_100000", "population_plus_de_100000")
PARKINGS_2003 = {
    "manque_jusqu_a_25": (250, 500, 1000),
    "manque_25_a_75": (375, 750, 1500),
    "manque_plus_de_75": (565, 1125, 2250),
}

COMPLEMENTS = {
    f"{TIB}.penalite_retard.taux_mensuel": (
        ("1997-01-01", 0.0125, CODE_1997), ("2002-01-01", 0.01, LF_2002),
        ("2007-01-01", 0.0075, LF_2007), ("2023-01-01", 0.0125, LF_2023)),
    f"{TIB}.penalite_retard.plafond_part_principal": (("2022-01-01", 1, LF_2022),),
    f"{TIB}.degrevement_partiel": (
        ("1997-01-01", 0.25, CODE_1997), ("2003-01-01", None, LF_2003)),
    f"{FNAH}.taux": (("2005-01-01", 0.04, LF_2005),),
    f"{SPECTACLES}.part_recettes_previsionnelles": (("1997-01-01", 0.5, CODE_1997),),
    f"{SPECTACLES}.taux": (("1997-01-01", 0.06, CODE_1997),),
    f"{SPECTACLES}.prix_entree_exonere_maximum": (("1997-04-07", 5, DECRET_SPECTACLES),),
    f"{RIVERAINS}.reduction_maximale": (
        ("1997-01-01", 0.5, CODE_1997), ("2002-08-01", None, LOI_2002_76)),
    f"{RIVERAINS}.avance.minimum": (("1997-01-01", 0.1, CODE_1997),),
    f"{RIVERAINS}.avance.maximum": (("1997-01-01", 0.3, CODE_1997),),
    f"{LICENCE}.retenue_budget_etat": (("1997-01-01", 0.1, CODE_1997),),
}
COMPLEMENTS.update({
    f"{LICENCE}.tarif_annuel.categorie_{n}": (("1997-03-13", tarif, DECRETS_1997),)
    for n, tarif in TARIF_LICENCE.items()
})
COMPLEMENTS.update({
    f"{PARKINGS}.bareme_1997.{tranche}": (
        ("1997-01-01", montant, CODE_1997), ("2003-01-01", None, LF_2003))
    for tranche, montant in PARKINGS_1997.items()
})
COMPLEMENTS.update({
    f"{PARKINGS}.bareme_2003.{manque}.{tranche}": (("2003-01-01", montant, LF_2003),)
    for manque, montants in PARKINGS_2003.items()
    for tranche, montant in zip(POPULATIONS_2003, montants)
})
SERIES.update(COMPLEMENTS)

# Feuilles exprimées en dinars ; les autres séries sont des taux ou des parts.
EN_DINARS = (
    ".maximum", ".seuil_affectation_excedent", ".prix_entree_exonere_maximum")
NOEUDS_EN_DINARS = (".tarif_annuel.", f"{PARKINGS}.")


def veille(date):
    return str(datetime.date.fromisoformat(date) - datetime.timedelta(days = 1))


# (feuille, instant, valeur attendue) : le jour de chaque date, la veille de la suivante, et la
# veille de la première date, où rien ne se lit.
LECTURES = []
for _chemin, _serie in SERIES.items():
    LECTURES.append((_chemin, veille(_serie[0][0]), None))
    for _rang, (_date, _valeur, _) in enumerate(_serie):
        LECTURES.append((_chemin, _date, _valeur))
        _fin = veille(_serie[_rang + 1][0]) if _rang + 1 < len(_serie) else "2026-12-31"
        LECTURES.append((_chemin, _fin, _valeur))


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
    assert feuilles == set(CODE) | set(DECRETS) | set(SERIES)


def ordre(noeud):
    """L'ordre déclaré des enfants ; il doit les nommer tous, et eux seuls."""
    assert set(noeud.children) == set(noeud.metadata["order"])
    return noeud.metadata["order"]


def test_la_fiscalite_locale_a_neuf_enfants_dans_l_ordre_du_code():
    """Les chapitres du code dans leur ordre ; la contribution au fonds de l'habitat, hors
    code, suit les deux taxes sur les immeubles dont elle reprend l'assiette."""
    assert ordre(FISCALITE_LOCALE) == [
        TIB, TNB, FNAH, TCL, TH, SPECTACLES, RIVERAINS, LICENCE, PARKINGS]


def test_forme_de_la_taxe_sur_les_etablissements_et_de_la_taxe_hoteliere():
    tcl = FISCALITE_LOCALE.children[TCL]
    assert ordre(tcl) == [
        "taux", "minimum", "maximum", "seuil_affectation_excedent",
        "part_impot_auto_entrepreneur",
    ]
    assert ordre(tcl.children["taux"]) == [
        "chiffre_affaires_brut_local", "chiffre_affaires_brut", "exportation_et_non_residents",
        "produits_prix_homologues", "impot_regime_1997", "impot_regime_2013",
    ]
    minimum = tcl.children["minimum"]
    assert ordre(minimum) == [f"categorie_{n}" for n in (1, 2, 3, 4)]
    for categorie in minimum.children.values():
        assert ordre(categorie) == [f"taux_{t}" for t in TAUX_TIB]
    assert ordre(FISCALITE_LOCALE.children[TH]) == ["taux", "part_affectee_fonds"]


def test_forme_des_complements():
    tib = FISCALITE_LOCALE.children[TIB]
    assert ordre(tib) == [
        "taux_assiette", "taux", "seuils_superficie", "prix_reference", "degrevement_partiel",
        "penalite_retard",
    ]
    assert ordre(tib.children["penalite_retard"]) == ["taux_mensuel", "plafond_part_principal"]
    assert ordre(FISCALITE_LOCALE.children[FNAH]) == ["taux"]
    assert ordre(FISCALITE_LOCALE.children[SPECTACLES]) == [
        "part_recettes_previsionnelles", "taux", "prix_entree_exonere_maximum"]
    riverains = FISCALITE_LOCALE.children[RIVERAINS]
    assert ordre(riverains) == ["reduction_maximale", "avance"]
    assert ordre(riverains.children["avance"]) == ["minimum", "maximum"]
    licence = FISCALITE_LOCALE.children[LICENCE]
    assert ordre(licence) == ["tarif_annuel", "retenue_budget_etat"]
    assert ordre(licence.children["tarif_annuel"]) == [f"categorie_{n}" for n in TARIF_LICENCE]
    parkings = FISCALITE_LOCALE.children[PARKINGS]
    assert ordre(parkings) == ["bareme_1997", "bareme_2003"]
    assert ordre(parkings.children["bareme_1997"]) == list(PARKINGS_1997)
    bareme_2003 = parkings.children["bareme_2003"]
    assert ordre(bareme_2003) == list(PARKINGS_2003)
    for manque in bareme_2003.children.values():
        assert ordre(manque) == list(POPULATIONS_2003)


def test_comptes():
    """53 feuilles ; 91 valeurs et 8 clôtures. Dont, de la version 0.133 : 26 feuilles, 60
    valeurs, 3 clôtures et les 48 montants du minimum ; s'y ajoutent une valeur du seuil
    d'affectation (2021) et 27 feuilles, 30 valeurs et 5 clôtures de compléments."""
    assert len(SERIES) == 10 + 16 + 27
    valeurs = [v for serie in SERIES.values() for _, v, _ in serie]
    assert sum(v is not None for v in valeurs) == 60 + 1 + 30
    assert sum(v is None for v in valeurs) == 3 + 5
    assert len(COMPLEMENTS) + 1 == 27
    assert sum(len(serie) for serie in COMPLEMENTS.values()) == 29 + 5
    parkings = [p for p in SERIES if p.startswith(f"{PARKINGS}.")]
    assert len(parkings) == 3 + 9
    minimum = [p for p in SERIES if ".minimum." in p]
    assert len(minimum) == 16
    assert sum(len(SERIES[p]) for p in minimum) == 48


@pytest.mark.parametrize(("chemin", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(chemin, instant, attendu):
    lu = parametre(chemin)(instant)
    if attendu is None:
        assert lu is None
    else:
        assert lu == pytest.approx(attendu)


@pytest.mark.parametrize("chemin", SERIES)
def test_chaque_date_des_series_porte_sa_reference(chemin):
    p = parametre(chemin)
    serie = SERIES[chemin]
    dates = {date for date, _, _ in serie}
    references = p.metadata["reference"]
    assert {v.instant_str for v in p.values_list} == dates
    assert {str(d) for d in references} == dates
    for date, valeur, (fascicule, lien) in serie:
        (reference,) = [liste for d, liste in references.items() if str(d) == date][0]
        assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
        assert reference["href"] == f"https://www.pist.tn/jort{lien}"
        assert fascicule in reference["note"], f"{chemin} au {date} : fascicule non cité"
        assert ", p. " in reference["note"] or ", pp. " in reference["note"]
        assert re.search(r"\blue?s?\b", reference["note"]), f"{chemin} au {date} : édition lue non dite"
        if valeur is None:
            assert "la valeur est vide" in reference["note"], f"{chemin} : clôture sans raison"


@pytest.mark.parametrize("chemin", SERIES)
def test_unites_des_series(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    if ".minimum." in chemin:
        attendue = "currency/m2"
    elif (chemin.endswith(EN_DINARS) and ".avance." not in chemin) or any(
            n in chemin for n in NOEUDS_EN_DINARS):
        attendue = "currency"
    else:
        attendue = "/1"
    unite = parametre(chemin).metadata["unit"]
    assert unite == attendue
    assert unite in enregistrees


def test_les_trois_clotures():
    """Le chiffre d'affaires « local » en 2014, l'assiette sur l'impôt de 1997 en 2013, le
    maximum en 2012 : chacune cesse à sa date, et la feuille qui prend la suite commence là."""
    assert parametre(f"{TCL}.taux.chiffre_affaires_brut_local")("2013-12-31") == 0.002
    assert parametre(f"{TCL}.taux.chiffre_affaires_brut_local")("2014-01-01") is None
    assert parametre(f"{TCL}.taux.chiffre_affaires_brut")("2013-12-31") is None
    assert parametre(f"{TCL}.taux.chiffre_affaires_brut")("2014-01-01") == 0.002
    assert parametre(f"{TCL}.taux.impot_regime_1997")("2012-12-31") == 0.25
    assert parametre(f"{TCL}.taux.impot_regime_1997")("2013-01-01") is None
    assert parametre(f"{TCL}.taux.impot_regime_2013")("2012-12-31") is None
    assert parametre(f"{TCL}.taux.impot_regime_2013")("2013-01-01") == 0.25
    assert parametre(f"{TCL}.maximum")("2011-12-31") == 100000
    assert parametre(f"{TCL}.maximum")("2012-01-01") is None
    # Aucun seuil en 2012 : le maximum est supprimé, l'affectation ne commence qu'en 2013.
    assert parametre(f"{TCL}.seuil_affectation_excedent")("2012-12-31") is None


def test_les_cinq_clotures_des_complements():
    """Le dégrèvement partiel en 2003, la réduction de moitié des riverains en 2002, et les trois
    tranches du barème des parkings de 1997, que le barème de 2003 remplace à la même date."""
    assert parametre(f"{TIB}.degrevement_partiel")("2002-12-31") == 0.25
    assert parametre(f"{TIB}.degrevement_partiel")("2003-01-01") is None
    assert parametre(f"{RIVERAINS}.reduction_maximale")("2002-07-31") == 0.5
    assert parametre(f"{RIVERAINS}.reduction_maximale")("2002-08-01") is None
    for tranche, montant in PARKINGS_1997.items():
        assert parametre(f"{PARKINGS}.bareme_1997.{tranche}")("2002-12-31") == montant
        assert parametre(f"{PARKINGS}.bareme_1997.{tranche}")("2003-01-01") is None
    for manque, montants in PARKINGS_2003.items():
        for tranche, montant in zip(POPULATIONS_2003, montants):
            assert parametre(f"{PARKINGS}.bareme_2003.{manque}.{tranche}")("2002-12-31") is None
            assert parametre(f"{PARKINGS}.bareme_2003.{manque}.{tranche}")("2003-01-01") == montant


def test_penalite_de_retard():
    """Quatre taux, 1,25 % puis 1 % puis 0,75 % puis de nouveau 1,25 % ; le texte de 2022 pose
    le plafond sans toucher au taux."""
    taux = parametre(f"{TIB}.penalite_retard.taux_mensuel")
    plafond = parametre(f"{TIB}.penalite_retard.plafond_part_principal")
    assert [taux(d) for d in ("1997-01-01", "2002-01-01", "2007-01-01", "2023-01-01")] == [
        0.0125, 0.01, 0.0075, 0.0125]
    assert taux("2021-12-31") == taux("2022-01-01") == 0.0075
    assert plafond("2021-12-31") is None
    assert plafond("2022-01-01") == 1
    assert "2022-01-01" not in {v.instant_str for v in taux.values_list}


def test_bareme_des_parkings():
    """Chaque barème croît avec la population ; celui de 2003 croît avec la part des places
    manquantes. D'un cas au suivant, le montant est multiplié par une fois et demie, sauf dans la
    première tranche du troisième cas, où le texte porte 565 dinars et non 562,500."""
    assert list(PARKINGS_1997.values()) == sorted(set(PARKINGS_1997.values()))
    for montants in PARKINGS_2003.values():
        assert list(montants) == sorted(set(montants))
    bas, milieu, haut = PARKINGS_2003.values()
    assert [m * 1.5 for m in bas] == list(milieu)
    assert [m * 1.5 for m in milieu[1:]] == list(haut[1:])
    assert haut[0] == 565 != milieu[0] * 1.5
    # La première tranche de 2003 n'a plus de plancher ; celle de 1997 commençait à 20 000.
    assert "population_jusqu_a_50000" in POPULATIONS_2003
    assert "population_20000_a_50000" in PARKINGS_1997


def test_baremes_croissants():
    """Le maximum et chacun des seize montants du minimum croissent d'un décret au suivant ;
    dans chaque décret, le minimum croît avec le taux de la taxe sur les immeubles bâtis."""
    maximum = [v for _, v, _ in SERIES[f"{TCL}.maximum"] if v is not None]
    assert maximum == sorted(set(maximum))
    for n in MINIMUM:
        for t in TAUX_TIB:
            montants = [v for _, v, _ in SERIES[f"{TCL}.minimum.categorie_{n}.taux_{t}"]]
            assert montants == sorted(set(montants)), f"catégorie {n}, taux {t}"
        for instant in ("1997-03-13", "2008-01-01", "2017-01-01"):
            ligne = [
                parametre(f"{TCL}.minimum.categorie_{n}.taux_{t}")(instant) for t in TAUX_TIB
            ]
            assert ligne == sorted(set(ligne)), f"catégorie {n} au {instant}"


def test_seul_le_systeme_fiscal_lit_la_fiscalite_locale():
    assert "fiscalite_locale" in SOUS_ARBRES_FISCAL
    assert "fiscalite_locale" not in SOUS_ARBRES_PENSION
