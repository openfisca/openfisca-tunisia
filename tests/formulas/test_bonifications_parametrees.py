"""Les bonifications CNRPS, branchées sur leurs paramètres, donnent les mêmes résultats.

`cnrps_bonifications` calculait le barème de l'article 32 de la loi n° 85-12 en dur,
sous un commentaire qui disait que la lecture des paramètres YAML échouait. Les
paramètres `retraite.cnrps.bonifications.**` existent, datés du 12 septembre 1985 et
sourcés sur cet article ; la formule les lit désormais.

Ce module démontre que le remaniement ne change aucun résultat. Il ne compare pas la
formule à une table de valeurs attendues — une table recopierait les mêmes constantes et
ne prouverait rien — mais **reconstruit le calcul en dur tel qu'il était écrit** et le
compare au calcul paramétré sur une grille qui encadre chacun des seuils des deux côtés.

La grille couvre les quatre durées de services du barème (35, 25, 20 et 15 ans) et leurs
voisines immédiates, croisées avec les durées de services militaires qui encadrent le
seuil de 20 ans, à plusieurs périodes.

Une réserve, que ce module ne masque pas : l'égalité démontrée porte sur les deux canaux
d'entrée que le modèle possède — `duree_service_cadre_actif` et
`duree_service_militaire`. L'article 32 vise **trois** catégories (ouvriers des travaux
pénibles, fonctions astreignantes, cadres actifs) et ne leur applique pas la même règle :
le barème est la bonification des premiers, mais seulement le **plafond** de « la période
restant à courir jusqu'à 60 ans » — 62 ans depuis la loi n° 2019-37 — pour les deux
autres. Le modèle les réunit dans une seule durée d'entrée, dont le libellé dit « cadre
actif ou travaux pénibles », et ne porte aucun paramètre de repère d'âge. Le calcul
conservé n'est donc pas celui du texte pour deux des trois catégories ; ce que ces tests
établissent, c'est qu'il n'a pas changé.
"""

# Standard Library
import itertools

# Third Party
import numpy as np
import pytest
from openfisca_core import periods
from openfisca_core.errors.parameter_not_found_error import ParameterNotFoundError
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


SYSTEME = TunisiaPensionTaxBenefitSystem()

# Les quatre seuils du barème de l'article 32, encadrés des deux côtés.
DUREES_CADRE_ACTIF = [0, 14, 15, 19, 20, 24, 25, 34, 35, 40]

# Le seuil de 20 ans de la bonification militaire, encadré des deux côtés.
DUREES_MILITAIRE = [0, 19, 20, 25, 30]

GRILLE = list(itertools.product(DUREES_CADRE_ACTIF, DUREES_MILITAIRE))

PERIODES = ["year:1985-09-12", "1986", "1990", "2019", "2024"]


def calcul_en_dur(duree_actif, duree_militaire):
    """Le calcul des bonifications tel qu'il était écrit avant le branchement.

    Reproduit à l'identique, constantes comprises : 5 ans pour 35 ans de services de
    cadre actif, 4 ans pour 25, 3 ans pour 20, 2 ans pour 15 ; 5 ans pour 20 ans de
    services militaires ; le tout converti en trimestres.
    """
    bonus_militaire = (duree_militaire >= 20) * 5
    bonus_actif = (
        (duree_actif >= 35) * 5
        + ((duree_actif >= 25) & (duree_actif < 35)) * 4
        + ((duree_actif >= 20) & (duree_actif < 25)) * 3
        + ((duree_actif >= 15) & (duree_actif < 20)) * 2
    )
    return (bonus_militaire + bonus_actif) * 4


def _simulation_sur_la_grille(period):
    """Un individu par couple de la grille, pour comparer en une fois."""
    simulation = SimulationBuilder().build_default_simulation(SYSTEME, len(GRILLE))
    durees_actif = np.array([actif for actif, _ in GRILLE])
    durees_militaire = np.array([militaire for _, militaire in GRILLE])
    simulation.set_input("duree_service_cadre_actif", period, durees_actif)
    simulation.set_input("duree_service_militaire", period, durees_militaire)
    simulation.set_input(
        "cnrps_duree_assurance_annuelle", period, 4 * durees_actif.astype(float)
    )
    return simulation, durees_actif, durees_militaire


@pytest.mark.parametrize("periode", PERIODES)
def test_les_bonifications_parametrees_egalent_le_calcul_en_dur(periode):
    """Cinquante couples, à chaque période : aucun écart."""
    period = periods.period(periode)
    simulation, durees_actif, durees_militaire = _simulation_sur_la_grille(period)

    obtenu = simulation.calculate("cnrps_bonifications", period)
    attendu = calcul_en_dur(durees_actif, durees_militaire)

    ecarts = [
        (int(actif), int(militaire), float(obtenu[rang]), int(attendu[rang]))
        for rang, (actif, militaire) in enumerate(GRILLE)
        if obtenu[rang] != attendu[rang]
    ]
    assert not ecarts, (
        "Le branchement sur les paramètres change le résultat pour "
        f"{len(ecarts)} couple(s) (durée cadre actif, durée militaire, obtenu, "
        f"attendu) : {ecarts}"
    )


@pytest.mark.parametrize("periode", PERIODES)
def test_la_duree_d_assurance_totale_est_elle_aussi_inchangee(periode):
    """La bonification s'ajoute à la durée d'assurance : on le vérifie en bout de chaîne."""
    period = periods.period(periode)
    simulation, durees_actif, durees_militaire = _simulation_sur_la_grille(period)

    obtenu = simulation.calculate("cnrps_duree_assurance", period)
    attendu = 4 * durees_actif + calcul_en_dur(durees_actif, durees_militaire)

    assert (obtenu == attendu).all()


def test_le_bareme_lu_est_bien_celui_de_l_article_32():
    """Les paramètres portent les valeurs que la formule écrivait en dur."""
    period = periods.period("2024")
    bonifications = SYSTEME.get_parameters_at_instant(
        period.start
    ).retraite.cnrps.bonifications
    assert bonifications.cadre_actif.service_35 == 5
    assert bonifications.cadre_actif.service_25 == 4
    assert bonifications.cadre_actif.service_20 == 3
    assert bonifications.cadre_actif.service_15 == 2
    assert bonifications.militaire.bonus == 5


@pytest.mark.parametrize("debut", ["1985-06-01", "1985-09-11"])
def test_les_bonifications_n_aboutissent_plus_avant_le_12_septembre_1985(debut):
    """Conséquence assumée du branchement : une erreur explicite, pas une valeur inventée.

    L'arithmétique en dur rendait un nombre pour n'importe quelle date, y compris avant
    l'effet de la loi qui institue le barème. Les paramètres commencent le 12 septembre
    1985, et la formule échoue désormais avant cette date — comme `cnrps_age_requis`,
    `cnrps_duree_requise_annees` et `cnrps_taux_de_liquidation` depuis les versions 5.4.0
    et 5.5.0. La période est réellement atteignable : `cnrps_bonifications` se calcule
    sans passer par les conditions d'ouverture du droit.
    """
    period = periods.period(f"year:{debut}")
    simulation = SimulationBuilder().build_default_simulation(SYSTEME, 1)
    simulation.set_input("duree_service_cadre_actif", period, np.array([35]))

    with pytest.raises(ParameterNotFoundError) as erreur:
        simulation.calculate("cnrps_bonifications", period)

    message = str(erreur.value)
    assert "retraite.cnrps.bonifications" in message
    assert debut in message
