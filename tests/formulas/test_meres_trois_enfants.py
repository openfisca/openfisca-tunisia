"""Mères de trois enfants : la jouissance est immédiate depuis le 1er janvier 1989.

`cnrps.depart_anticipe.meres_3_enfants.age_minimum` valait 50 ans pour toute période, sans
qu'aucun texte lu ne fixe cet âge — la version 5.4.0 en a d'ailleurs retiré la référence à
l'article 5, qui ne le contient pas.

Or l'**article 41 nouveau**, issu de la loi n° 88-71 du 27 juin 1988 (effet au 1er janvier
1989), range « la mise à la retraite sur la demande des mères » parmi les cas de
**jouissance immédiate**. À partir de cette date, aucune condition d'âge ne leur est
opposable.

Ces tests vérifient les **deux périodes** : la mère de trois enfants qui remplit la
condition de durée mais n'a pas 50 ans n'ouvre pas droit en 1988, et ouvre droit en 1990.
Ils vérifient aussi que les cas déjà couverts par les tests existants — une mère de 52 ans
— restent éligibles de part et d'autre de la bascule, afin que la correction n'emporte
rien d'autre.
"""

# Third Party
import numpy as np
import pytest
from openfisca_core import periods
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


SYSTEME = TunisiaPensionTaxBenefitSystem()

# Quinze ans de services : la durée requise des mères (article 22, condition générale).
DUREE_SUFFISANTE_TRIMESTRES = 65


def _simulation(periode, age, duree_assurance=DUREE_SUFFISANTE_TRIMESTRES):
    period = periods.period(periode)
    simulation = SimulationBuilder().build_default_simulation(SYSTEME, 1)
    simulation.set_input("age", period, np.array([age]))
    simulation.set_input("mere_3_enfants", period, np.array([True]))
    simulation.set_input(
        "cnrps_duree_assurance", period, np.array([duree_assurance], dtype=float)
    )
    simulation.set_input("cnrps_salaire_de_base", period, np.array([12000.0]))
    return simulation, period


@pytest.mark.parametrize(
    ("periode", "age_requis_attendu"),
    [
        # Avant la loi n° 88-71 : la valeur de 50 ans, que nul texte lu n'appuie.
        ("year:1985-09-12", 50),
        ("1986", 50),
        ("1988", 50),
        # Article 41 nouveau : jouissance immédiate, donc aucune condition d'âge.
        ("1989", 0),
        ("1990", 0),
        ("2024", 0),
    ],
)
def test_age_requis_des_meres_de_trois_enfants(periode, age_requis_attendu):
    simulation, period = _simulation(periode, age=45)
    age_requis = simulation.calculate("cnrps_age_requis", period)
    assert age_requis[0] == age_requis_attendu


@pytest.mark.parametrize(
    ("periode", "eligible_attendu"),
    [
        ("1988", False),
        ("1990", True),
    ],
)
def test_la_mere_de_45_ans_ouvre_droit_a_partir_de_1989(periode, eligible_attendu):
    """Le cas que la correction déplace, de part et d'autre du 1er janvier 1989.

    Quarante-cinq ans, seize ans de services : la condition de durée est remplie dans les
    deux cas. Seule la condition d'âge sépare 1988 de 1990, et elle disparaît en 1989.
    """
    simulation, period = _simulation(periode, age=45)
    assert bool(simulation.calculate("cnrps_eligible", period)[0]) is eligible_attendu


@pytest.mark.parametrize("periode", ["1988", "1990", "2024"])
def test_la_mere_de_52_ans_reste_eligible_de_part_et_d_autre(periode):
    """La correction n'ôte rien à qui était déjà éligible.

    C'est le cas que vérifient `test_anticipe.py` et `test_depart_anticipe.yaml`, à 52 ans :
    il passait avec la condition de 50 ans, et il passe sans elle.
    """
    simulation, period = _simulation(periode, age=52)
    assert bool(simulation.calculate("cnrps_eligible", period)[0]) is True


def test_la_duree_requise_des_meres_est_inchangee():
    """Seule la condition d'âge change : les quinze ans de services demeurent."""
    for periode in ("1988", "1990"):
        simulation, period = _simulation(periode, age=45)
        assert simulation.calculate("cnrps_duree_requise_annees", period)[0] == 15
