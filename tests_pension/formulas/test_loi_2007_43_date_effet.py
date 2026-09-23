"""Date d'effet de la loi n° 2007-43 : le 2 juillet 2007.

La loi n'a pas de clause d'entrée en vigueur. Le fascicule n° 51 du 26 juin 2007 a été déposé
au siège du gouvernorat de Tunis le 27 juin 2007 : la loi est exécutoire cinq jours plus tard,
le jour du dépôt n'étant pas compté (loi n° 93-64, article 2).

Les variables du système des pensions sont annuelles et lisent les paramètres au 1er janvier :
aucun test YAML ne peut atteindre le 1er ou le 2 juillet, et une période annuelle qui commence
en cours d'année ignore ses entrées. Ce test lit donc les paramètres à l'instant même.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

PARAMETRES = TunisiaPensionTaxBenefitSystem().parameters
CADRE_COMMUN = PARAMETRES.retraite.cnrps.depart_anticipe.sur_demande.cadre_commun


@pytest.mark.parametrize(
    ("instant", "age", "duree"),
    [("2007-07-01", 55, 35), ("2007-07-02", 57, 37)],
)
def test_depart_anticipe_sur_demande_cadre_commun(instant, age, duree):
    assert CADRE_COMMUN.age_minimum(instant) == age
    assert CADRE_COMMUN.duree_minimum(instant) == duree


@pytest.mark.parametrize("regime", ["raci", "rtfr"])
@pytest.mark.parametrize(
    "feuille",
    ["age_limite_orphelin", "age_limite_orphelin_etudes", "age_limite_orphelin_etudes_superieures"],
)
def test_reference_de_la_loi_datee_du_2_juillet(regime, feuille):
    parametre = getattr(PARAMETRES.retraite, regime).survivants.children[feuille]
    references = parametre.metadata["reference"]
    assert "2007-07-02" in {str(date) for date in references}
    assert not {"2007-06-28", "2007-07-01"} & {str(date) for date in references}
