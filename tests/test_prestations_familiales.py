"""Prestations familiales : contrôle des séries sur le texte publié au JORT.

Les quatre états successifs de l'article 61 de la loi n° 60-30 sont relevés sur fac-similé.
Aucune valeur du dispositif ne date de 1960, contrairement à ce qui était encodé.
"""

from openfisca_tunisia import TunisiaTaxBenefitSystem

tax_benefit_system = TunisiaTaxBenefitSystem()


def pf(date):
    parametres = tax_benefit_system.get_parameters_at_instant(date)
    return parametres.prestations.contributives.prestations_familiales


def test_les_quatre_ages_du_bareme():
    """Article 61 : taux unique en 1960, barème dégressif en 1976, 4e rang supprimé en 1989."""
    # 1960 : taux UNIQUE de 15 %, bande d'assiette 52-500 D, quatre rangs.
    a = pf("1960-01-01").af
    assert (a.taux.enf1, a.taux.enf2, a.taux.enf3, a.taux.enf4) == (0.15, 0.15, 0.15, 0.15)
    assert a.plancher_trim == 52
    assert a.plaf_trim == 500
    assert a.nb_enfants_max == 4

    # 1976 (loi n° 75-82) : barème dégressif, plafond unique de 72 D, plus de bande.
    a = pf("1976-01-01").af
    assert (a.taux.enf1, a.taux.enf2, a.taux.enf3, a.taux.enf4) == (0.18, 0.16, 0.14, 0.12)
    assert a.plaf_trim == 72
    assert a.nb_enfants_max == 4

    # 1986 (loi n° 86-75) : plafond porté à 122 D, taux inchangés.
    a = pf("1986-05-01").af
    assert a.plaf_trim == 122
    assert (a.taux.enf1, a.taux.enf2, a.taux.enf3, a.taux.enf4) == (0.18, 0.16, 0.14, 0.12)

    # 1989 (loi n° 88-38) : le quatrième rang est supprimé, le plafond ne bouge pas.
    a = pf("1989-01-01").af
    assert a.plaf_trim == 122
    assert a.nb_enfants_max == 3


def test_le_plafond_de_122_dinars_ne_date_pas_de_1960():
    """Non-régression : la valeur était encodée au 1er janvier 1960 en citant un texte de 1988."""
    assert pf("1960-01-01").af.plaf_trim == 500
    assert pf("1985-12-31").af.plaf_trim == 72
    assert pf("1986-05-01").af.plaf_trim == 122


def test_le_quatrieme_rang_et_le_plancher_sont_cloture_aux_bonnes_dates():
    """Deux paramètres n'existent que sur une période bornée ; hors d'elle, ils sont absents."""
    import pytest
    from openfisca_core.errors import ParameterNotFoundError

    # Le plancher d'assiette disparaît avec la bande, en 1976.
    assert pf("1975-12-31").af.plancher_trim == 52
    with pytest.raises(ParameterNotFoundError):
        pf("1976-01-01").af.plancher_trim

    # Le quatrième rang disparaît en 1989.
    assert pf("1988-12-31").af.taux.enf4 == 0.12
    with pytest.raises(ParameterNotFoundError):
        pf("1989-01-01").af.taux.enf4


def test_majoration_pour_salaire_unique_nexiste_pas_avant_1980():
    """Le dispositif est créé par la loi n° 80-36, effet au 1er mai 1980."""
    import pytest
    from openfisca_core.errors import ParameterNotFoundError

    with pytest.raises(ParameterNotFoundError):
        pf("1980-04-30").salaire_unique.enf1

    su = pf("1980-05-01").salaire_unique
    assert (su.enf1, su.enf2, su.enf3) == (9.375, 18.750, 23.475)


def test_contribution_creche_ne_date_pas_de_1960():
    """Loi n° 94-88 et décret n° 95-114, effet au 1er octobre 1994."""
    import pytest
    from openfisca_core.errors import ParameterNotFoundError

    with pytest.raises(ParameterNotFoundError):
        pf("1994-09-30").creche.montant

    c = pf("1994-10-01").creche
    assert c.montant == 15
    assert (c.age_min, c.age_max, c.duree) == (2, 36, 11)
    assert c.plaf == 2.5
