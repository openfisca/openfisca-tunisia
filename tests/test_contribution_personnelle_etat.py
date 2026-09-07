"""Contribution personnelle d'État : contrôle du tarif sur le texte publié au JORT.

Aucune variable du modèle ne consomme ces paramètres — openfisca-tunisia ne calcule pas
l'avant-1990. Ils servent de référence datée, notamment aux tableaux du précis socio-fiscal.
Ces tests sont donc leur seul garde-fou : ils vérifient d'une part la structure des trois
tarifs successifs, d'autre part que la colonne « taux d'imposition du revenu global à la
limite supérieure de la tranche », imprimée dans le texte de loi, se déduit bien du tarif
encodé. Une erreur de seuil ou de taux casse cette seconde vérification.
"""

import datetime

from openfisca_tunisia import TunisiaTaxBenefitSystem

tax_benefit_system = TunisiaTaxBenefitSystem()


def bareme(annee):
    parametres = tax_benefit_system.get_parameters_at_instant(f"{annee}-01-01")
    return parametres.impot_revenu.contribution_personnelle_etat.bareme


def taux_effectifs(bareme):
    """Taux d'imposition du revenu global à la limite supérieure de chaque tranche.

    Deux décimales TRONQUÉES et non arrondies : c'est la convention du JORT, qui imprime
    « 1,53 % » pour 1,538 % et « 20,12 % » pour 20,125 %.
    """
    seuils, taux = list(bareme.thresholds), list(bareme.rates)
    resultats, cumul = [], 0.0
    for indice in range(len(seuils) - 1):
        cumul += (seuils[indice + 1] - seuils[indice]) * taux[indice]
        resultats.append(int(cumul / seuils[indice + 1] * 100 * 100 + 1e-9) / 100)
    return resultats


def test_structure_des_trois_tarifs():
    # Revenus 1980 : art. 8 de la loi n° 79-66, JORT n° 76 des 28-31 décembre 1979, p. 3540.
    assert len(bareme(1980).thresholds) == 11
    assert bareme(1980).thresholds[-1] == 8500
    assert bareme(1980).rates[-1] == 0.80

    # Revenus 1983 : art. 9 de la loi n° 82-91, JORT n° 84 du 31 décembre 1982, p. 2877.
    assert len(bareme(1983).thresholds) == 20
    assert bareme(1983).thresholds[-1] == 100000
    assert bareme(1983).rates[-1] == 0.80

    # Revenus 1986 : art. 8 de la loi n° 85-109, JORT n° 91 du 31 décembre 1985, p. 1731.
    assert len(bareme(1986).thresholds) == 18
    assert bareme(1986).thresholds[-1] == 80000
    assert bareme(1986).rates[-1] == 0.68


def test_tarif_1986_reste_en_vigueur_jusqu_aux_revenus_de_1989():
    """La CPE est supprimée pour les revenus réalisés à compter du 1er janvier 1990."""
    assert list(bareme(1989).thresholds) == list(bareme(1986).thresholds)
    assert list(bareme(1989).rates) == list(bareme(1986).rates)


def test_taux_effectifs_conformes_au_jort_1986():
    """Colonne imprimée à l'article 8 de la loi n° 85-109 (JORT n° 91/1985, p. 1731)."""
    assert taux_effectifs(bareme(1986)) == [
        0.0, 1.53, 2.66, 5.75, 8.6, 11.33, 14.0, 16.75, 21.8, 26.16,
        33.12, 37.7, 43.5, 50.76, 54.97, 57.98, 59.98,
    ]


def test_taux_effectifs_conformes_au_jort_1983():
    """Colonne imprimée à l'article 9 de la loi n° 82-91 (JORT n° 84/1982, p. 2877).

    La valeur de la tranche 50 000-65 000 est illisible sur le fac-similé ; elle est
    déduite des deux valeurs voisines, lisibles, et des seuils du tarif.
    """
    assert taux_effectifs(bareme(1983)) == [
        0.0, 1.53, 2.66, 5.75, 8.6, 11.33, 14.0, 16.75, 21.8, 26.16,
        33.12, 37.7, 43.5, 50.76, 56.38, 58.13, 59.61, 60.76, 62.29,
    ]


def test_taux_effectifs_conformes_au_jort_1980():
    """Colonne imprimée à l'article 8 de la loi n° 79-66 (JORT n° 76/1979, p. 3540)."""
    assert taux_effectifs(bareme(1980)) == [
        0.0, 4.0, 7.66, 10.75, 13.6, 16.33, 22.25, 29.81, 36.28, 42.23,
    ]


def test_plafond_de_cotisation():
    def plafond(annee):
        parametres = tax_benefit_system.get_parameters_at_instant(f"{annee}-01-01")
        return parametres.impot_revenu.contribution_personnelle_etat.plafond_cotisation

    assert plafond(1980) == 0.55
    assert plafond(1983) == 0.60
    assert plafond(1989) == 0.60
