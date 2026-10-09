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
    """Limite d'âge de l'étudiant à 25 ans, et non 21.

    Arrêté conjoint du 19 mai 2020, article 2 ; JORT n° 45 du 20 mai 2020, p. 1097. Sans
    clause d'effet : exécutoire le 25 mai 2020, cinq jours après le dépôt du fascicule
    (20 mai), jour du dépôt non compté — loi n° 93-64, article 2.
    """
    for feuille in (
        "enfant_a_charge",
        "handicap",
        "age_min_enfant",
        "limite_age_enfant",
        "limite_age_etudiant",
    ):
        with pytest.raises(ParameterNotFoundError):
            getattr(nc("2020-05-24").amen_social.supplements, feuille)

    s = nc("2020-05-25").amen_social.supplements
    assert s.enfant_a_charge == 10
    assert s.handicap == 2
    assert s.age_min_enfant == 0
    assert s.limite_age_etudiant == 25
    assert s.limite_age_enfant == 18


def test_amen_social_allocation_de_base():
    def base(date):
        return nc(date).amen_social.allocation_base

    assert base("2020-06-01") == 180
    assert base("2022-06-01") == 200
    assert base("2023-06-01") == 220
    assert base("2024-06-01") == 240
    # Arrêté conjoint du 29 janvier 2025, article 2 : effet au 1er janvier 2025.
    assert base("2025-06-01") == 260


def test_amen_allocation_de_base_dates_d_effet_enoncees():
    """Chaque arrêté modificatif énonce sa date d'effet, au 1er janvier de son année.

    Arrêtés des 1er avril 2022 (alinéa 1 nouveau), 3 avril 2023, 28 février 2024,
    29 janvier 2025 et 21 avril 2026 (article 2 de chacun).
    """

    def base(date):
        return nc(date).amen_social.allocation_base

    for veille, jour, avant, apres in (
        ("2021-12-31", "2022-01-01", 180, 200),
        ("2022-12-31", "2023-01-01", 200, 220),
        ("2023-12-31", "2024-01-01", 220, 240),
        ("2024-12-31", "2025-01-01", 240, 260),
        ("2025-12-31", "2026-01-01", 260, 280),
    ):
        assert base(veille) == avant
        assert base(jour) == apres


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


def test_amen_allocation_de_base_executoire_le_25_mai_2020():
    """L'arrêté conjoint du 19 mai 2020 est publié au JORT n° 45 du 20 mai 2020, p. 1097.

    Sans clause d'effet : exécutoire cinq jours après le dépôt du fascicule au gouvernorat
    de Tunis (20 mai 2020), jour du dépôt non compté — loi n° 93-64, article 2. La série
    portait le 20 mai 2020, jour de la publication.
    """
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-24").amen_social.allocation_base
    assert nc("2020-05-25").amen_social.allocation_base == 180


def test_aides_ponctuelles_datees_de_2020_et_non_de_2019():
    """L'appui financier occasionnel est fixé par l'arrêté conjoint du 19 mai 2020,
    publié au JORT n° 45 du 20 mai 2020. L'année 2019 n'est la date d'aucun texte.

    Sans clause d'effet : exécutoire le 25 mai 2020 (dépôt du 20 mai, plus cinq jours).
    """
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-24").amen_social.aides_ponctuelles.fetes_religieuses.ramadan
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-24").amen_social.aides_ponctuelles.scolarite.rentree_scolaire

    aides = nc("2020-05-25").amen_social.aides_ponctuelles
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
    # Arrêté sans clause d'effet, fascicule déposé le 9 décembre 2022 : exécutoire le 14.
    for feuille in ("montant_min", "montant_max", "nombre_max_par_an"):
        with pytest.raises(ParameterNotFoundError):
            getattr(nc("2022-12-13").amen_social.aides_ponctuelles.urgence, feuille)
    assert nc("2022-12-14").amen_social.aides_ponctuelles.urgence.montant_min == 60


def test_allocation_familiale_6_18_montant_fixe_par_l_arrete_du_3_novembre_2025():
    """Arrêté conjoint du 3 novembre 2025, article 2 ; JORT n° 132 du 4 novembre 2025, p. 2963.

    Trente dinars par mois et par enfant à charge. L'arrêté n'a pas de clause d'effet :
    exécutoire cinq jours après le dépôt du fascicule (4 novembre 2025), jour du dépôt non
    compté — loi n° 93-64, article 2. Le décret n° 2025-426 institue l'allocation au
    1er janvier 2025 sans en fixer le montant ; aucun texte publié ne fonde l'aide versée de
    2022 à 2024.
    """
    for date in ("2022-07-01", "2023-02-01", "2025-01-01", "2025-11-08"):
        with pytest.raises(ParameterNotFoundError):
            nc(date).allocation_familiale_6_18
    assert nc("2025-11-09").allocation_familiale_6_18 == 30
    assert nc("2026-06-01").allocation_familiale_6_18 == 30
    # La feuille des moins de six ans n'est ni déplacée ni modifiée.
    assert nc("2022-04-08").allocation_familiale == 30


def test_amen_seuils_d_eligibilite_executoires_le_25_mai_2020():
    """Décret gouvernemental n° 2020-317 du 19 mai 2020, article 5 ; JORT n° 45 du 20 mai 2020.

    Sans clause d'effet : exécutoire cinq jours après le dépôt du fascicule au gouvernorat de
    Tunis (20 mai 2020), jour du dépôt non compté — loi n° 93-64, article 2. La série portait
    le 1er janvier 2020, antérieur au décret.
    """
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-24").amen_social.eligibilite.un_membre
    with pytest.raises(ParameterNotFoundError):
        nc("2020-05-24").amen_social.eligibilite.handicap_lourd.un_membre

    seuils = nc("2020-05-25").amen_social.eligibilite
    assert seuils.un_membre == pytest.approx(2 / 3, abs=1e-12)
    assert seuils.deux_membres == 1
    assert seuils.trois_quatre_membres == 1.5
    assert seuils.plus_de_cinq_membres == 2
    assert seuils.handicap_lourd.un_membre == pytest.approx(7 / 6, abs=1e-12)
