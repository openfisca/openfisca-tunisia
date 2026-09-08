"""Pensions de source étrangère et minimum d'impôt : contrôle sur le texte publié au JORT.

Les trois régimes successifs des pensions étrangères et la date du minimum d'impôt de
l'article 12 bis de la loi n° 89-114 sont établis sur fac-similé (JORT n° 1 des 2-5 janvier
1990 et JORT n° 104 des 30-31 décembre 1997, page 2441).
"""

from openfisca_tunisia import TunisiaTaxBenefitSystem

tax_benefit_system = TunisiaTaxBenefitSystem()


def impot_revenu(date):
    return tax_benefit_system.get_parameters_at_instant(date).impot_revenu


def test_pensions_etrangeres_trois_regimes():
    # Article 37 d'origine : les « sommes effectivement perçues de l'étranger », sans abattement.
    assert impot_revenu("1990-01-01").tspr.abat_pen_etr == 0
    assert impot_revenu("1996-01-01").tspr.abat_pen_etr == 0

    # Article 61 de la loi de finances 1998 : renvoi à l'article 26, soit 25 %.
    assert impot_revenu("1997-01-01").tspr.abat_pen_etr == 0.25
    assert impot_revenu("2005-01-01").tspr.abat_pen_etr == 0.25

    # Article 35 de la loi de finances 2007 : régime de faveur de 80 %.
    assert impot_revenu("2006-01-01").tspr.abat_pen_etr == 0.8
    assert impot_revenu("2026-01-01").tspr.abat_pen_etr == 0.8


def test_abattement_etranger_aligne_sur_le_droit_commun_entre_1997_et_2005():
    """Le renvoi de l'article 61 aligne les pensions étrangères sur l'article 26."""
    for annee in range(1997, 2006):
        etranger = impot_revenu(f"{annee}-01-01").tspr.abat_pen_etr
        droit_commun = impot_revenu(f"{annee}-01-01").tspr.abat_pen
        assert etranger == droit_commun, annee


def test_minimum_impot_avantages_fiscaux():
    """« … est relevé à partir du 1er janvier 1999 respectivement à 20% et 60% » (art. 62 LF 1998)."""
    assert impot_revenu("1998-12-31").minimum_impot.taux == 0
    assert impot_revenu("1999-01-01").minimum_impot.taux == 0.60
    assert impot_revenu("2017-03-31").minimum_impot.taux == 0.60
    # Article 2 § 6 de la loi n° 2017-8, applicable « à partir du 1er avril 2017 ».
    assert impot_revenu("2017-04-01").minimum_impot.taux == 0.45
    assert impot_revenu("2026-01-01").minimum_impot.taux == 0.45
