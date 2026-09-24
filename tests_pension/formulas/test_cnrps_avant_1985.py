"""CNRPS avant 1985 : réversion, orphelins, maximum d'annuités et plancher de l'indice 100.

Ces paramètres décrivent l'état du droit de la loi n° 59-18 du 5 février 1959 et de ses
modificatifs, du 1er avril 1959 (article 52, rédaction de la loi n° 59-100) au 12 septembre
1985 (loi n° 85-12, article 75). Un test YAML n'atteint que des valeurs de variables, et les
variables du système des pensions lisent leurs paramètres au premier jour de leur période :
ce test lit donc les paramètres à l'instant même, la veille et le jour de chaque borne.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

CNRPS = TunisiaPensionTaxBenefitSystem().parameters.retraite.cnrps
SURVIVANTS = CNRPS.survivants
INDICE_100 = CNRPS.pension_minimale.indice_100


@pytest.mark.parametrize(
    ("instant", "conjoint", "orphelin"),
    [
        ("1959-03-31", None, None),
        ("1959-04-01", 0.5, 0.1),  # loi n° 59-18, art. 31, § I et § III
        ("1981-04-30", 0.5, 0.1),
        ("1981-05-01", 0.75, 0.1),  # loi n° 81-70, art. 4 et 5
        ("1985-09-11", 0.75, 0.1),
        ("1985-09-12", 0.75, 0.1),  # loi n° 85-12, art. 43 et 45
    ],
)
def test_survivants(instant, conjoint, orphelin):
    assert SURVIVANTS.taux_conjoint(instant) == conjoint
    assert SURVIVANTS.taux_orphelin(instant) == orphelin


@pytest.mark.parametrize(
    ("instant", "maximum"),
    [
        ("1959-03-31", None),
        ("1959-04-01", 40),  # loi n° 59-18, art. 20, § III
        ("1985-09-11", 40),
        ("1985-09-12", None),  # loi n° 85-12 : aucun maximum
    ],
)
def test_maximum_annuites_liquidables(instant, maximum):
    assert CNRPS.maximum_annuites_liquidables(instant) == maximum


@pytest.mark.parametrize(
    ("instant", "part", "annuites", "taux"),
    [
        ("1959-03-31", None, None, None),
        ("1959-04-01", 1, 30, 0.04),  # loi n° 59-18, art. 22, § II a) et b)
        ("1970-06-30", 1, 30, 0.04),
        ("1970-07-01", 0.6, None, None),  # décret-loi n° 70-1, art. 1er et 2
        ("1981-04-30", 0.6, None, None),
        ("1981-05-01", None, None, None),  # loi n° 81-70 : deux tiers du SMIG
    ],
)
def test_plancher_indice_100(instant, part, annuites, taux):
    assert INDICE_100.part_indice_100(instant) == part
    assert INDICE_100.annuites_pension_pleine(instant) == annuites
    assert INDICE_100.taux_par_annuite_proportionnelle(instant) == taux


@pytest.mark.parametrize(
    ("instant", "minimum"),
    [("1981-04-30", None), ("1981-05-01", 0.66666)],
)
def test_le_plancher_en_smig_prend_le_relais(instant, minimum):
    assert CNRPS.pension_minimale.minimum_garanti(instant) == minimum
