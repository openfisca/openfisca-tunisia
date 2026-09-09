"""La série des taux de retraite CNRPS, telle que les textes la fixent.

Le point vérifié ici est celui qu'un fichier de paramètres ne peut pas défendre seul :
l'article 4 de la loi n° 2019-37 du 30 avril 2019 (JORT n° 35, p. 1314) majore la part
de l'agent de « 1 % à partir du premier janvier 2020 », en une seule fois. Le fichier
portait un palier intermédiaire au 1er juin 2019 — cette date est celle de la part
patronale, et le test l'interdit désormais de revenir.
"""

import datetime

from openfisca_tunisia import TunisiaTaxBenefitSystem


tax_benefit_system = TunisiaTaxBenefitSystem()

RETRAITE_SALARIE = (
    "prelevements_sociaux.cotisations_sociales.secteur_public.salarie_cnrps"
    ".cotisations_salarie.retraite"
)
RETRAITE_EMPLOYEUR = (
    "prelevements_sociaux.cotisations_sociales.secteur_public.salarie_cnrps"
    ".cotisations_employeur.retraite"
)


def _taux(chemin, date):
    parametres = tax_benefit_system.get_parameters_at_instant(date)
    noeud = parametres
    for element in chemin.split("."):
        noeud = getattr(noeud, element)
    return noeud.rates[0]


def test_le_point_de_2019_tombe_en_une_fois_au_1er_janvier_2020():
    assert _taux(RETRAITE_SALARIE, "2019-05-31") == 0.082
    assert _taux(RETRAITE_SALARIE, "2019-12-31") == 0.082
    assert _taux(RETRAITE_SALARIE, "2020-01-01") == 0.092


def test_les_echeanciers_pluriannuels_de_2002_et_2007():
    # Loi de finances 2002, article 85 : 0,50 / 0,25 / 0,25 en juillet.
    assert _taux(RETRAITE_SALARIE, "2002-06-30") == 0.06
    assert _taux(RETRAITE_SALARIE, "2002-07-01") == 0.065
    assert _taux(RETRAITE_SALARIE, "2003-07-01") == 0.0675
    assert _taux(RETRAITE_SALARIE, "2004-07-01") == 0.07
    # Loi 2007-43, article premier : 0,40 trois fois, en juillet.
    assert _taux(RETRAITE_SALARIE, "2007-07-01") == 0.074
    assert _taux(RETRAITE_SALARIE, "2008-07-01") == 0.078
    assert _taux(RETRAITE_SALARIE, "2009-07-01") == 0.082


def test_les_marches_patronales_de_2007_tombent_en_janvier():
    # Loi 2007-43 : 0,60 point au 1er janvier 2007, 2008 et 2009 — la part patronale
    # suit un calendrier distinct de celui de la part salariale.
    assert _taux(RETRAITE_EMPLOYEUR, "2007-01-01") == 0.103
    assert _taux(RETRAITE_EMPLOYEUR, "2007-12-31") == 0.103
    assert _taux(RETRAITE_EMPLOYEUR, "2008-01-01") == 0.109
    assert _taux(RETRAITE_EMPLOYEUR, "2009-01-01") == 0.115


def test_la_serie_reste_definie_sur_toute_sa_longueur():
    for annee in range(1960, datetime.date.today().year + 1):
        assert _taux(RETRAITE_SALARIE, f"{annee}-06-30") > 0
