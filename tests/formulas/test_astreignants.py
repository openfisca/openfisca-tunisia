"""Fonctions astreignantes (article 28 de la loi n° 85-12) et calculs CNRPS de 1985.

Les paramètres `depart_anticipe.sur_demande.astreignants` commençaient au
24 septembre 1985, date de signature du décret n° 85-1178 ; ils sont désormais fondés
sur l'article 28 de la loi n° 85-12, dont l'effet est au 12 septembre 1985.

Aucun calcul CNRPS n'aboutit avant cette date. `cnrps_age_requis` et
`cnrps_duree_requise_annees` lisent, pour tous les individus, toutes les branches de
leur `select` — astreignants, cadre commun, mères de trois enfants — et, à défaut,
`duree_de_service_minimale` : tous ces paramètres commencent le 12 septembre 1985,
faute de texte lu pour la période de la loi n° 59-18. L'erreur est explicite, et c'est
ce qui est voulu : une valeur reconduite en arrière sans texte se présenterait comme du
droit.

Les périodes annuelles commençant en cours d'année (`year:1985-06-01`) lisent les
paramètres à leur premier jour : elles permettent de tester les deux côtés du
12 septembre 1985.
"""

# Third Party
import pytest
from openfisca_core import periods
from openfisca_core.errors.parameter_not_found_error import ParameterNotFoundError
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


SYSTEME = TunisiaPensionTaxBenefitSystem()


def _simulation(period, **entrees):
    simulation = SimulationBuilder().build_default_simulation(SYSTEME, 1)
    for variable, valeur in entrees.items():
        simulation.set_input(variable, period, [valeur])
    return simulation


@pytest.mark.parametrize(
    ("debut", "taux_attendu"),
    [
        # Barème de l'article 38 de la loi n° 85-12 : 2 % puis 3 % par année.
        ("1985-09-12", 40 * 0.005 + 40 * 0.0075),
        ("1985-09-24", 40 * 0.005 + 40 * 0.0075),
    ],
)
def test_taux_de_liquidation_calcule_a_partir_du_12_septembre_1985(debut, taux_attendu):
    period = periods.period(f"year:{debut}")
    simulation = _simulation(period, cnrps_duree_assurance=80)
    taux = simulation.calculate("cnrps_taux_de_liquidation", period)
    assert taux[0] == pytest.approx(taux_attendu)


@pytest.mark.parametrize(
    ("debut", "variable"),
    [
        ("1985-06-01", "cnrps_taux_de_liquidation"),
        ("1985-09-11", "cnrps_taux_de_liquidation"),
        ("1985-06-01", "cnrps_age_requis"),
        ("1985-09-11", "cnrps_duree_requise_annees"),
    ],
)
def test_aucun_calcul_cnrps_avant_le_12_septembre_1985(debut, variable):
    """Avant l'effet de la loi n° 85-12, le calcul échoue au lieu d'inventer une valeur.

    La loi n° 59-18 du 5 février 1959 n'a pas été lue article par article : l'état du
    droit antérieur n'est pas établi, aucune valeur n'est portée, et les conditions
    d'ouverture du droit ne sont donc pas définies. Le barème d'annuités du 1er février
    1959, lui, reste encodé et sourcé, mais aucun calcul ne peut l'atteindre.
    """
    period = periods.period(f"year:{debut}")
    simulation = _simulation(
        period,
        cnrps_duree_assurance=80,
        depart_anticipe_sur_demande=True,
        fonction_astreignante=True,
    )
    with pytest.raises(ParameterNotFoundError) as erreur:
        simulation.calculate(variable, period)
    message = str(erreur.value)
    assert "retraite.cnrps" in message
    assert debut in message


@pytest.mark.parametrize(
    ("periode", "age_attendu"),
    [
        ("year:1985-09-12", 55),
        ("2019", 55),
        # Loi n° 2019-37, article 5 : +1 an au 1er juillet 2019, +2 ans au 1er janvier 2020.
        ("year:2019-07-01", 56),
        ("2020", 57),
    ],
)
def test_conditions_du_depart_sur_demande_des_astreignants(periode, age_attendu):
    period = periods.period(periode)
    simulation = _simulation(
        period,
        depart_anticipe_sur_demande=True,
        fonction_astreignante=True,
    )
    assert simulation.calculate("cnrps_age_requis", period)[0] == age_attendu
    assert simulation.calculate("cnrps_duree_requise_annees", period)[0] == 35
