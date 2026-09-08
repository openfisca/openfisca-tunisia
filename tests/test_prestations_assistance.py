"""Assistance sociale : contrôle des séries sur le texte publié au JORT.

Plusieurs valeurs portaient des dates sans support et deux références étaient apocryphes.
"""

import pytest
from openfisca_core.errors import ParameterNotFoundError

from openfisca_tunisia import TunisiaTaxBenefitSystem

tax_benefit_system = TunisiaTaxBenefitSystem()


def nc(date):
    return tax_benefit_system.get_parameters_at_instant(date).prestations.non_contributives


def test_pnafn_seul_le_palier_atteste_borne_la_serie():
    """L'arrêté du 10 juillet 2024 constate 180 D ; aucun montant n'est publié après."""
    assert nc("2018-04-01").pnafn.allocation == 180
    assert nc("2026-01-01").pnafn.allocation == 180


def test_pnafn_les_plafonds_de_2024_et_2025_ne_sont_pas_des_montants():
    """L'arrêté autorise un relèvement plafonné à 240 puis 260 D, sans fixer de montant.

    Encoder ces plafonds comme des valeurs serait une sur-interprétation : c'est le piège le
    plus probable pour qui reprendrait la série.
    """
    assert nc("2025-01-01").pnafn.allocation not in (240, 260)


def test_amg2_date_de_1998_et_non_de_2015():
    """Article 10 du décret n° 98-409 du 18 février 1998."""
    with pytest.raises(ParameterNotFoundError):
        nc("1998-02-26").amg2
    assert nc("1998-02-27").amg2 == 10
    assert nc("2015-01-01").amg2 == 10


def test_allocation_familiale_non_contributive_nexiste_pas_avant_2022():
    """Décret-loi n° 2022-8 et arrêté du 1er avril 2022 ; ce qui existait en 2020 est autre."""
    with pytest.raises(ParameterNotFoundError):
        nc("2020-06-01").allocation_familiale
    assert nc("2022-04-08").allocation_familiale == 30


def test_amen_social_supplements():
    """Limite d'âge de l'étudiant à 25 ans, et non 21 ; effet au 20 mai 2020."""
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-19").amen_social.supplements.enfant_a_charge

    s = nc("2020-05-20").amen_social.supplements
    assert s.enfant_a_charge == 10
    assert s.limite_age_etudiant == 25
    assert s.limite_age_enfant == 18


def test_amen_social_allocation_de_base():
    def base(date):
        return nc(date).amen_social.allocation_base

    assert base("2020-06-01") == 180
    assert base("2022-06-01") == 200
    assert base("2023-06-01") == 220
    assert base("2024-06-01") == 240
    # Palier ajouté : arrêté du 29 août 2025, rétroactif au 1er janvier.
    assert base("2025-06-01") == 260
