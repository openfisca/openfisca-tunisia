"""Déductions d'épargne de l'article 39 du code : contrôle sur le texte publié au JORT.

Les valeurs de 1990 sont relevées sur le fac-similé du Journal officiel (n° 1 des 2-5 janvier
1990, page 8), celles de 1992 sur le n° 90 du 31 décembre 1991, page 2084.
"""

from openfisca_tunisia import TunisiaTaxBenefitSystem

tax_benefit_system = TunisiaTaxBenefitSystem()


def deductions(annee):
    return tax_benefit_system.get_parameters_at_instant(f"{annee}-01-01").impot_revenu.deductions


def test_interets_epargne_structure_a_deux_niveaux():
    """Avant 1992, un seul plafond ; ensuite, un plafond global et un sous-plafond."""
    # `interets_emprunts_obligataires` porte le plafond GLOBAL, malgré son nom.
    # 1990 : « sans que cette déduction n'excède 1000 dinars par an », comptes spéciaux seuls.
    assert deductions(1990).interets_emprunts_obligataires.plaf == 1000
    assert deductions(1990).interets_comptes_speciaux_epargne_bancaires.plaf == 1000

    # 1992 : « dans la limite d'un montant annuel de mille cinq cent dinars (1500 d) sans que ce
    # montant n'excède mille dinars pour les intérêts provenant des comptes spéciaux d'épargne ».
    assert deductions(1992).interets_emprunts_obligataires.plaf == 1500
    assert deductions(1992).interets_comptes_speciaux_epargne_bancaires.plaf == 1000

    assert deductions(2016).interets_emprunts_obligataires.plaf == 5000
    assert deductions(2016).interets_comptes_speciaux_epargne_bancaires.plaf == 3000
    assert deductions(2021).interets_emprunts_obligataires.plaf == 10000
    assert deductions(2021).interets_comptes_speciaux_epargne_bancaires.plaf == 6000


def test_sous_plafond_jamais_superieur_au_plafond_global():
    """Contrainte de cohérence interne du dispositif, à tout millésime."""
    for annee in range(1990, 2027):
        d = deductions(annee)
        assert (
            d.interets_comptes_speciaux_epargne_bancaires.plaf
            <= d.interets_emprunts_obligataires.plaf
        ), annee


def test_assurance_vie_valeurs_d_origine():
    """« dans la limite de 200 dinars par an, majorés de : 100 dinars au titre du conjoint ;
    50 dinars au titre de chacun des quatre premiers enfants à charge » (JORT n° 1/1990, p. 8)."""
    assurance = deductions(1990).assurance_vie
    assert assurance.plaf == 200
    assert assurance.conj_plaf == 100
    assert assurance.enf_plaf == 50


def test_assurance_vie_serie():
    # Article 52 de la loi de finances 1998 : « dans la limite de 800 dinars par an, majorés de :
    # 400 dinars au titre du conjoint ; et 200 dinars au titre de chacun des enfants à charge ».
    assert deductions(1997).assurance_vie.plaf == 800
    assert deductions(1997).assurance_vie.conj_plaf == 400
    assert deductions(1997).assurance_vie.enf_plaf == 200

    assert deductions(2007).assurance_vie.plaf == 1200
    assert deductions(2013).assurance_vie.plaf == 10000
    # Rattaché aux revenus 2020 par la note commune n° 1/2021, et non à 2021.
    assert deductions(2020).assurance_vie.plaf == 100000


def test_assurance_vie_majorations_cloturees_par_le_plafond_unique():
    """L'article 24 de la loi de finances 2014 remplace le plafond majoré par un plafond unique.

    La formule additionne plafond et majorations : laisser ces dernières à leur dernière valeur
    porterait le plafond effectif d'un couple avec enfants au-delà des 10 000 dinars du texte.
    """
    assert deductions(2012).assurance_vie.conj_plaf == 600
    assert deductions(2012).assurance_vie.enf_plaf == 300
    for annee in range(2013, 2027):
        assert deductions(annee).assurance_vie.conj_plaf == 0, annee
        assert deductions(annee).assurance_vie.enf_plaf == 0, annee
