"""Prévoyance sociale des titulaires de pension de la CNRPS : décret n° 73-91, article 15.

Le décret n° 73-91 du 12 mars 1973 (JORT n° 10, p. 356, lu à l'image) fixe à 2 % de la pension en
principal la cotisation du retraité et de la veuve de retraité, à compter du 1er avril 1973
(article 18). Le décret n° 2007-1406 (articles 12 et 13, JORT n° 49 du 19 juin 2007, p. 2162)
échelonne ensuite le taux du régime de base d'assurance maladie des titulaires de pension affiliés
à la CNRPS de 1 % à 4 % entre 2007 et 2010.

Aucune variable ne lit ce paramètre ; comme un test YAML n'asserte que des variables, ce test lit
le barème aux bornes, selon la convention de ``test_atmp_95_538.py``.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

PREVOYANCE = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux.cotisations_sociales.secteur_public.pensionne_cnrps.prevoyance_sociale
TAUX = PREVOYANCE.brackets[0].rate


def test_aucun_prelevement_avant_le_decret_73_91():
    assert TAUX("1972-06-01") is None
    assert TAUX("1973-03-01") is None


def test_deux_pour_cent_du_1er_avril_1973_a_2007():
    # Décret n° 73-91, article 15 : 2 % de la pension en principal.
    assert TAUX("1973-04-01") == pytest.approx(0.02)
    assert TAUX("1990-06-01") == pytest.approx(0.02)
    assert TAUX("2007-06-01") == pytest.approx(0.02)


def test_rampe_du_regime_de_base_d_assurance_maladie_2007_2010():
    # Décret n° 2007-1406, articles 12 et 13.
    assert TAUX("2007-07-01") == pytest.approx(0.01)
    assert TAUX("2008-07-01") == pytest.approx(0.02)
    assert TAUX("2009-07-01") == pytest.approx(0.03)
    assert TAUX("2010-07-01") == pytest.approx(0.04)
