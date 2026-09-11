"""Fonctions astreignantes (article 28 de la loi n° 85-12) et calculs CNRPS de 1985.

Les paramètres `depart_anticipe.sur_demande.astreignants` ne commençaient que le
24 septembre 1985 ; comme `cnrps_duree_requise_annees` et `cnrps_age_requis` les lisent
pour tous les individus, aucun calcul CNRPS n'aboutissait avant cette date.

Les périodes annuelles commençant en cours d'année (`year:1985-06-01`) lisent les
paramètres à leur premier jour : elles permettent de tester les deux côtés du
12 septembre 1985, date d'effet de la loi n° 85-12.
"""

# Third Party
import pytest
from openfisca_core import periods
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
        # Barème de la loi n° 59-18 : 0,5 % par trimestre.
        ("1985-06-01", 80 * 0.005),
        ("1985-09-11", 80 * 0.005),
        # Barème de l'article 38 de la loi n° 85-12 : 2 % puis 3 % par année.
        ("1985-09-12", 40 * 0.005 + 40 * 0.0075),
        ("1985-09-24", 40 * 0.005 + 40 * 0.0075),
    ],
)
def test_taux_de_liquidation_calcule_en_1985(debut, taux_attendu):
    period = periods.period(f"year:{debut}")
    simulation = _simulation(period, cnrps_duree_assurance=80)
    taux = simulation.calculate("cnrps_taux_de_liquidation", period)
    assert taux[0] == pytest.approx(taux_attendu)


@pytest.mark.parametrize(
    ("periode", "age_attendu"),
    [
        ("year:1985-06-01", 55),
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
