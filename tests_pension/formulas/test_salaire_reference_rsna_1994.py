"""Salaire de référence du RSNA, rédaction du décret n° 94-1429 : les deux erreurs explicites.

Un test YAML ne sait pas attendre une exception, d'où ce test Python.

- L'exercice 1994 relève de la rédaction de 1990, qui ne rend pas de valeur, sauf pour les
  droits ouverts à compter du 1er juillet 1994, date d'effet des articles 18 et 19
  nouveaux : la date de liquidation départage les deux semestres. Le cas du 15 septembre
  1994 est aussi testé en YAML (`rsna/salaire_de_reference.yaml`).
- Aucun barème d'actualisation n'est identifié pour les droits ouverts après 2024 : le
  calcul s'arrête sur une erreur plutôt que de réemployer le barème de 2024.
"""

# Third Party
import pytest
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.simulations import SimulationBuilder

# First Party
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

SYSTEME = TunisiaPensionTaxBenefitSystem()


def salaire_de_reference(annee, date_de_liquidation=None):
    individu = {
        "rsna_salaire_de_base": {str(a): 12000.0 for a in range(annee - 12, annee + 1)}
    }
    if date_de_liquidation is not None:
        individu["rsna_liquidation_date"] = {"ETERNITY": date_de_liquidation}
    simulation = SimulationBuilder().build_from_dict(
        SYSTEME, {"individus": {"assure": individu}}
    )
    return simulation.calculate("rsna_salaire_de_reference", str(annee))[0]


def test_droit_ouvert_le_30_juin_1994_redaction_de_1990():
    with pytest.raises(NotImplementedError, match="90-1455"):
        salaire_de_reference(1994, "1994-06-30")


def test_droit_ouvert_le_1er_juillet_1994_redaction_de_1994():
    # Cinq années, 1989 à 1993, barème de l'arrêté du 17 novembre 1994.
    attendu = 12000.0 * (1.26342 + 1.18541 + 1.10005 + 1.04197 + 1) / 5
    assert salaire_de_reference(1994, "1994-07-01") == pytest.approx(attendu)


@pytest.mark.parametrize("date_de_liquidation", [None, "2025-03-01"])
def test_pas_de_bareme_pour_les_droits_ouverts_en_2025(date_de_liquidation):
    with pytest.raises(ParameterNotFoundError, match="annee_2024"):
        salaire_de_reference(2025, date_de_liquidation)


def test_le_bareme_de_2024_vaut_pour_les_droits_ouverts_en_2024():
    # Dix années, 2014 à 2023, barème de l'arrêté du 16 juillet 2024.
    coefficients = [
        1.73582,
        1.65758,
        1.59801,
        1.51728,
        1.41202,
        1.32216,
        1.25163,
        1.18406,
        1.09323,
        1,
    ]
    assert salaire_de_reference(2024) == pytest.approx(12000.0 * sum(coefficients) / 10)
