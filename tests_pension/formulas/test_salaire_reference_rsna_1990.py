"""Salaire de référence du RSNA du 23 septembre 1990 au 30 juin 1994 : une erreur explicite.

Le décret n° 90-1455 récrit l'article 18 du décret n° 74-499 (dix dernières années) et
laisse l'article 19 intact (total divisé par 36 ou 60 mois). Les textes ne disent pas
lequel l'emporte : le calcul s'arrête sur une erreur plutôt que de rendre une valeur.

Un test YAML ne sait pas attendre une exception, d'où ce test Python. Les exercices 1991
à 1994 relèvent tous de cette rédaction, l'exercice annuel étant daté du 1er janvier ;
1990 relève encore de la rédaction de 1974, 1995 de celle de 1994.
"""

# Third Party
import pytest
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

SYSTEME = TunisiaPensionTaxBenefitSystem()


def salaire_de_reference(annee):
    salaires = {str(a): 12000.0 for a in range(annee - 12, annee + 1)}
    simulation = SimulationBuilder().build_from_dict(
        SYSTEME, {"individus": {"assure": {"rsna_salaire_de_base": salaires}}}
    )
    return simulation.calculate("rsna_salaire_de_reference", str(annee))[0]


@pytest.mark.parametrize("annee", [1991, 1992, 1993, 1994])
def test_la_redaction_de_1990_ne_rend_pas_de_valeur(annee):
    with pytest.raises(NotImplementedError, match="90-1455"):
        salaire_de_reference(annee)


@pytest.mark.parametrize(
    ("annee", "attendu"),
    [
        # 1990 : rédaction de 1974, salaires constants.
        (1990, 12000.0),
        # 1995 : rédaction de 1994, cinq années actualisées par l'arrêté du 16 mars 1995.
        (1995, 12000.0 * (1.23839 + 1.14921 + 1.08854 + 1.04469 + 1) / 5),
    ],
)
def test_les_exercices_voisins_rendent_une_valeur(annee, attendu):
    assert salaire_de_reference(annee) == pytest.approx(attendu)
