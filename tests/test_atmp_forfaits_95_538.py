"""Salaires forfaitaires et modulation AT/MP : décret n° 95-538, articles 4 à 27.

Les forfaits des articles 4 à 7 et la modulation des articles 10 à 27 sont versés en paramètres
sous ``prelevements_sociaux/atmp_forfaits`` et ``prelevements_sociaux/atmp_modulation``. Hormis le
forfait des employés de maison (article 6), calculé par
``cotisation_accident_travail_forfaitaire_employe_maison`` et testé en YAML, aucune variable ne lit
encore ces paramètres (l'arborescence des variables reste à arbitrer : issue #471). Comme un test
YAML n'asserte que des variables, ce test lit les paramètres aux bornes, selon la convention de
``test_atmp_95_538.py``.

Valeurs lues dans le JORT : décret n° 95-538 (JORT n° 30 du 14 avril 1995, éd. arabe pp. 691-692,
qui fait foi) ; décret n° 99-1010 (JORT n° 40 du 18 mai 1999, p. 734) ; décret n° 2000-1439
(JORT n° 52 du 30 juin 2000, p. 1541).
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

PARAMETERS = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux
FORFAITS = PARAMETERS.atmp_forfaits
MODULATION = PARAMETERS.atmp_modulation


# --- Article 4 : forfait agricole et pêche à la part ---
def test_agriculture_taux_1_pc_en_1995_puis_0_80_pc_en_1999():
    taux = FORFAITS.agriculture_peche.taux
    assert taux("1995-06-01") == pytest.approx(0.01)
    assert taux("1999-03-01") == pytest.approx(0.01)
    assert taux("1999-04-01") == pytest.approx(0.008)


def test_agriculture_coefficients_cotisation_et_prestations():
    ap = FORFAITS.agriculture_peche
    assert ap.coefficient_cotisation("1995-06-01") == pytest.approx(1.5)
    assert ap.plafond_salaire_smag("1995-06-01") == pytest.approx(2)
    assert ap.base_prestations_jours("1995-06-01") == 300
    assert ap.coefficient_prestations_ordinaire("1995-06-01") == pytest.approx(1)
    assert ap.coefficient_prestations_specialise("1995-06-01") == pytest.approx(1.5)
    assert ap.coefficient_prestations_qualifie("1995-06-01") == pytest.approx(2)


# Tableau des journées de l'article 4 : (chemin, valeur 1995, valeur 1999).
# ``None`` en 1995 marque une ligne ajoutée par le décret n° 99-1010.
JOURNEES = [
    ("cereales_sec", 7, 7),
    ("cereales_irrigue", 15, 15),
    ("legumineuses_grandes_cultures_sec", 15, 15),
    ("cultures_industrielles", 70, 70),
    ("maraicheres_solanacees", 150, 150),
    ("maraicheres_pommes_de_terre", 50, 50),
    ("horticulture_plein_champ", None, 70),  # ligne ajoutée en 1999
    ("oliviers_amandiers", 17, 17),
    ("vigne_cuve", 20, 20),
    ("vigne_table", 40, 40),
    ("agrumes", 90, 90),
    ("arboriculture_sec", 20, 20),
    ("arboriculture_irrigue", 60, 60),
    ("palmier_dattier", 120, 120),
    ("cultures_sous_serres", 300, 300),
    ("bananes_sous_serres", 700, 700),
    ("elevage_bovins", 30, 30),  # étendu aux équins et camélidés en 1999
    ("elevage_ovins", 5, 5),
    ("aviculture", 36, 36),
    ("cuniculture", None, 36),  # ligne ajoutée en 1999
    ("peche_cotiere", 500, 500),
    ("peche_chalut", 2000, 2000),
]


@pytest.mark.parametrize("nom, valeur_1995, valeur_1999", JOURNEES)
def test_tableau_des_journees_1995_et_1999(nom, valeur_1995, valeur_1999):
    parametre = getattr(FORFAITS.agriculture_peche.journees, nom)
    assert parametre("1995-06-01") == valeur_1995
    assert parametre("1999-06-01") == valeur_1999


# --- Article 5 : chauffeurs de louage et taxis ; masseurs des bains maures ---
def test_chauffeurs_2400_heures_et_coefficient_abaisse_en_2000():
    chauffeurs = FORFAITS.chauffeurs_taxi_louage
    assert chauffeurs.nombre_heures("1995-06-01") == 2400
    assert chauffeurs.coefficient("1995-06-01") == pytest.approx(1.5)
    assert chauffeurs.coefficient("2000-06-01") == pytest.approx(1.5)
    assert chauffeurs.coefficient("2000-07-01") == pytest.approx(
        1
    )  # décret n° 2000-1439


def test_masseurs_inchanges_par_le_decret_2000_1439():
    masseurs = FORFAITS.masseurs_bains_maures
    assert masseurs.nombre_heures("1995-06-01") == 2400
    assert masseurs.coefficient("1995-06-01") == pytest.approx(1.5)
    assert masseurs.coefficient("2000-07-01") == pytest.approx(1.5)


# --- Article 6 : employés de maison ---
def test_employes_maison_taux_et_base():
    maison = FORFAITS.employes_maison
    assert maison.base_jours("1995-06-01") == 300
    assert maison.taux_aides_menage("1995-06-01") == pytest.approx(0.0053)
    assert maison.taux_autres("1995-06-01") == pytest.approx(0.0075)
    assert maison.taux_conducteurs("1995-06-01") == pytest.approx(0.01)
    assert maison.coefficient_conducteurs("1995-06-01") == pytest.approx(1.5)


# --- Article 7 : travailleurs temporaires auprès des particuliers ---
def test_temporaires_200_heures_et_coefficients():
    temporaires = FORFAITS.temporaires_particuliers
    assert temporaires.nombre_heures_mensuel("1995-06-01") == 200
    assert temporaires.coefficient_ordinaire("1995-06-01") == pytest.approx(1)
    assert temporaires.coefficient_qualifie("1995-06-01") == pytest.approx(2)


# --- Articles 17, 18 et 24 : modulation ---
def test_modulation_cotisation_supplementaire_et_reduction():
    assert MODULATION.cotisation_supplementaire("1995-06-01") == pytest.approx(0.5)
    assert MODULATION.cotisation_supplementaire_maximum("1995-06-01") == pytest.approx(
        1.0
    )
    assert MODULATION.reduction_maximum("1995-06-01") == pytest.approx(0.25)
