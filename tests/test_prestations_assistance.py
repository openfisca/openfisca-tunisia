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


def test_amen_supplement_borne_basse_dage_et_non_cumul():
    """La borne basse passe de 0 à 6 ans le 1er février 2022, jour où l'allocation
    familiale non contributive prend en charge les enfants de moins de six ans.

    Sans cette borne, un enfant de moins de six ans ouvrirait droit aux deux prestations.
    """
    supplements = nc("2020-06-01").amen_social.supplements
    assert supplements.age_min_enfant == 0
    assert supplements.limite_age_enfant == 18

    apres = nc("2022-02-01").amen_social.supplements
    assert apres.age_min_enfant == 6
    assert nc("2022-01-31").amen_social.supplements.age_min_enfant == 0


def test_amen_allocation_de_base_prend_effet_a_la_publication():
    """L'arrêté conjoint du 19 mai 2020 est publié au JORT n° 45 du 20 mai 2020.

    La série portait le 1er mai 2020, date qu'aucun texte n'énonce.
    """
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-19").amen_social.allocation_base
    assert nc("2020-05-20").amen_social.allocation_base == 180


def test_aides_ponctuelles_datees_de_2020_et_non_de_2019():
    """L'appui financier occasionnel est fixé par l'arrêté conjoint du 19 mai 2020,
    publié au JORT n° 45 du 20 mai 2020. L'année 2019 n'est la date d'aucun texte.
    """
    aides = nc("2020-05-20").amen_social.aides_ponctuelles
    assert aides.fetes_religieuses.ramadan == 60
    assert aides.fetes_religieuses.aid_al_fitr == 60
    assert aides.fetes_religieuses.aid_al_adha == 60
    assert aides.scolarite.rentree_scolaire == 50
    assert aides.scolarite.rentree_universitaire == 120

    with pytest.raises(ParameterNotFoundError):
        nc("2019-06-01").amen_social.aides_ponctuelles.fetes_religieuses.ramadan


def test_appui_urgence_est_un_intervalle_et_non_un_montant():
    """L'arrêté du 8 décembre 2022 module l'appui entre 60 et 200 dinars selon la
    situation de la famille : c'est le seul du dispositif à ne pas avoir de montant fixe.
    """
    urgence = nc("2023-01-01").amen_social.aides_ponctuelles.urgence
    assert urgence.montant_min == 60
    assert urgence.montant_max == 200
    assert urgence.nombre_max_par_an == 4

    # Un NŒUD de paramètres existe à toute date ; seule une feuille sans valeur lève.
    with pytest.raises(ParameterNotFoundError):
        nc("2022-12-08").amen_social.aides_ponctuelles.urgence.montant_min
