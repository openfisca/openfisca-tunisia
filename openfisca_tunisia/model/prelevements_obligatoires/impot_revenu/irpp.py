# -*- coding: utf-8 -*-


from __future__ import division

from numpy import logical_or as or_

from openfisca_tunisia.model.base import *  # noqa analysis:ignore


class nb_enf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Nombre d'enfants"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        TODO: fixme
        '''
        age = foyer_fiscal.members('age', period = period)
        P = parameters(period.start).impot_revenu.deductions.fam
        # res =+ (
        #    (ag < 20) +
        #    (ag < 25)*not_(boursier)*()
        #    )
        condition = (age >= 0) * (age <= P.age)
        return foyer_fiscal.sum(condition, role = FoyerFiscal.PERSONNE_A_CHARGE)


class nb_enf_sup(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Nombre d'enfants étudiants du supérieur non boursiers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants étudiants du supérieur non boursiers
        '''
        age = foyer_fiscal.members('age', period = period)
        boursier = foyer_fiscal.members('boursier', period = period)

        return 0 * age * not_(boursier)


class nb_infirme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Nombre d'enfants infirmes"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants infirmes
        '''
        age = foyer_fiscal.members('age', period = period)
        invalide = foyer_fiscal.members('invalide', period = period)

        return 0 * age * invalide


class nb_parents(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Nombre de parents"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre de parents
        '''
        return (
            (foyer_fiscal.declarant_principal('age', period) > 20) +
            (foyer_fiscal.declarant_principal('age', period) > 20)
            )


class chef_de_famille(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"Indicatrice de chef de famille"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

    # Du point de vue fiscal, est considéré chef de famille :
    # - L’époux ;
    # - Le divorcé ou la divorcée qui a la garde des enfants (divorce & enfnats);
    # - Le veuf ou la veuve même sans enfants à charge;
    # - L’adoptant ou l’adoptante (adoptant). TODO
    # Cependant, l’épouse a la qualité de chef de famille dans les deux cas suivants :
    # - Lorsqu’elle justifie que le mari ne dispose d’aucune source de revenu durant l’année de réalisation du
    #   revenu. Tel est le cas d’une femme qui dispose d’un revenu et dont le mari, poursuivant des études, ne dispose
    #   d’aucun revenu propre. (marie & sexe & revenu_epoux == 0 & revenu_individu > 0) TODO
    # - Lorsque remariée, elle a la garde d’enfants issus d’un précédent mariage. TODO
    # Compte tenu de ce qui précède, n’est pas considéré comme chef de famille et ne bénéficie d’aucune déduction :
    # - Le célibataire ou la célibataire ;
    # - Le divorcé ou la divorcée qui n’a pas la garde des enfants ;
    # - La femme durant le mariage (sauf si elle dispose d’un revenu alors que son mari ne dispose d’aucun revenu) ;
    # - L’époux qui ne dispose pas d’une source de revenu. Dans ce cas, l’épouse acquiert la qualité de chef de famille
    #   au cas où elle réalise des revenus.

    def formula(foyer_fiscal, period):
        male = foyer_fiscal.declarant_principal('male', period = period)
        marie = foyer_fiscal.declarant_principal('marie', period = period)
        divorce = foyer_fiscal.declarant_principal('divorce', period = period)
        veuf = foyer_fiscal.declarant_principal('veuf', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        chef_de_famille = (
            veuf |
            (marie & male) |
            (divorce & (nb_enf > 0))  # | 
            # (marie & (not male)) |
            )

        return chef_de_famille


###############################################################################
# Revenus catégoriels
###############################################################################


# 1. Bénéfices industriels et commerciaux
class bic(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Bénéfices industriels et commerciaux (BIC)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_reel_res = foyer_fiscal('bic_reel_res', period = period)
        # TODO:
        #    return bic_reel + bic_simpl + bic_forf
        return bic_reel_res


# régime réel
# régime réel simplifié
# régime forfaitaire


class bic_ca_global(Variable):
    value_type = float
    entity = Individu
    label = u"Chiffre d’affaires global (BIC, cession de fond de commerce"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        """
        Chiffre d’affaires global
        des personnes soumises au régime forfaitaire ayant cédé le fond de commerce
        """
        bic_ca_revente = foyer_fiscal('bic_ca_revente', period = period)
        bic_ca_autre = foyer_fiscal('bic_ca_autre', period = period)

        return bic_ca_revente + bic_ca_autre


class bic_res_cession(Variable):
    value_type = float
    entity = Individu
    label = u"Résultat (BIC, cession de fond de commerce)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_ca_global = foyer_fiscal('bic_ca_global', period = period)
        bic_depenses = foyer_fiscal('bic_depenses', period = period)

        return max_(bic_ca_global - bic_depenses, 0)


class bic_benef_fiscal_cession(Variable):
    value_type = float
    entity = Individu
    label = u"Bénéfice fiscal (BIC, cession de fond de commerce)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_res_cession = foyer_fiscal('bic_res_cession', period = period)
        bic_pv_cession = foyer_fiscal('bic_pv_cession', period = period)

        return bic_res_cession + bic_pv_cession


def _bic_res_net(bic_benef_fiscal_cession, bic_part_benef_sp):
    """
    Résultat net BIC TODO: il manque le régime réel
    """
    return bic_benef_fiscal_cession + bic_part_benef_sp


# 2. Bénéfices des professions non commerciales
class bnc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Bénéfices des professions non commerciales (BNC)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bnc_reel_res_fiscal = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_reel_res_fiscal', period = period)
            )
        bnc_forf_benef_fiscal = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_forf_benef_fiscal', period = period)
            )
        bnc_part_benef_sp = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_part_benef_sp', period = period)
            )
        return bnc_reel_res_fiscal + bnc_forf_benef_fiscal + bnc_part_benef_sp


class bnc_forf_benef_fiscal(Variable):
    value_type = float
    entity = Individu
    label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Bénéfice fiscal (régime forfaitaire, en % des recettes brutes TTC)
        """
        bnc_forfaitaire_recettes_brutes = foyer_fiscal('bnc_forfaitaire_recettes_brutes', period = period)
        part = parameters(period.start).impot_revenu.bnc.forf.part_forf
        return bnc_forfaitaire_recettes_brutes * part


# 3. Bénéfices de l'exploitation agricole et de pêche
class beap(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Bénéfices de l'exploitation agricole et de pêche (BEAP)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        beap_reel_res_fiscal = foyer_fiscal('beap_reel_res_fiscal', period = period)
        beap_reliq_benef_fiscal = foyer_fiscal('beap_reliq_benef_fiscal', period = period)
        beap_monogr = foyer_fiscal('beap_monogr', period = period)
        beap_part_benef_sp = foyer_fiscal('beap_part_benef_sp', period = period)

        return beap_reel_res_fiscal + beap_reliq_benef_fiscal + beap_monogr + beap_part_benef_sp


# 4. Revenus fonciers

class revenus_fonciers(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus fonciers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        foncier_reel_resultat_fiscal = foyer_fiscal.declarant_principal('foncier_reel_resultat_fiscal', period = period)
        fon_forf_bati = foyer_fiscal('fon_forf_bati', period = period)
        fon_forf_nbat = foyer_fiscal('fon_forf_nbat', period = period)
        foncier_societes_personnes = foyer_fiscal.declarant_principal('foncier_societes_personnes', period = period)

        return foncier_reel_resultat_fiscal + fon_forf_bati + fon_forf_nbat + foncier_societes_personnes


class fon_forf_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus fonciers net des immeubles bâtis"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        foncier_forfaitaire_batis_recettes = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_recettes', period = period)
        foncier_forfaitaire_batis_reliquat = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_reliquat', period = period)
        foncier_forfaitaire_batis_frais = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_frais', period = period)
        foncier_forfaitaire_batis_taxe = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_taxe', period = period)
        P = parameters(period.start).impot_revenu.foncier.bati.deduction_frais
        return max_(
            0,
            foncier_forfaitaire_batis_recettes * (1 - P) - foncier_forfaitaire_batis_frais - foncier_forfaitaire_batis_taxe
            )


class fon_forf_nbat(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus fonciers net des terrains non bâtis"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        foncier_forfaitaire_non_batis_recettes = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_recettes', period = period)
        foncier_forfaitaire_non_batis_depenses = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_depenses', period = period)
        foncier_forfaitaire_non_batis_taxe = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_taxe', period = period)
        return max_(
            foncier_forfaitaire_non_batis_recettes - foncier_forfaitaire_non_batis_depenses - foncier_forfaitaire_non_batis_taxe,
            0
            )


# 5. Traitements, salaires, indemnités, pensions et rentes viagères

class tspr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Traitements, salaires, indemnités, pensions et rentes viagères"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        revenu_assimile_salaire_apres_abattements = foyer_fiscal(
            'revenu_assimile_salaire_apres_abattements', period = period)
        revenu_assimile_pension_apres_abattements = foyer_fiscal(
            'revenu_assimile_pension_apres_abattements', period = period)

        return revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements


class revenu_assimile_salaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu assimilé à des salaires"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        salaire_imposable = foyer_fiscal.declarant_principal('salaire_imposable', period = period, options = [ADD])
        salaire_en_nature = foyer_fiscal.declarant_principal('salaire_en_nature', period = period, options = [ADD])
        return (salaire_imposable + salaire_en_nature)


class smig(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig_dec = foyer_fiscal.declarant_principal('smig_dec', period = period.first_month)
        smig_40h_mensuel = parameters(period.start).cotisations_sociales.gen.smig_40h_mensuel
        smig = or_(smig_dec, revenu_assimile_salaire <= 12 * smig_40h_mensuel)
        return smig


class revenu_assimile_salaire_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu imposé comme des salaires net des abatements"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        if period.start.year >= 2011:
            res = max_(
                revenu_assimile_salaire * (1 - tspr.abat_sal) - max_(smig * tspr.smig,
                 (revenu_assimile_salaire <= tspr.smig_ext) * tspr.smig), 0)
        else:
            res = max_(revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.smig, 0)
        return res


class revenu_assimile_pension_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu assimilé à des pensions après abattements"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_pension = foyer_fiscal.declarant_principal('revenu_assimile_pension', period = period)
        avantages_nature_assimile_pension = foyer_fiscal.declarant_principal(
            'avantages_nature_assimile_pension', period = period)
        tspr = parameters(period.start).impot_revenu.tspr
        return (revenu_assimile_pension + avantages_nature_assimile_pension) * (1 - tspr.abat_pen)


# 6. Revenus de valeurs mobilières et de capitaux mobiliers

class rvcm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus de valeurs mobilières et de capitaux mobiliers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        capm_banq = foyer_fiscal.declarant_principal('capm_banq', period = period)
        capm_cent = foyer_fiscal.declarant_principal('capm_cent', period = period)
        capm_caut = foyer_fiscal.declarant_principal('capm_caut', period = period)
        capm_part = foyer_fiscal.declarant_principal('capm_part', period = period)
        capm_oblig = foyer_fiscal.declarant_principal('capm_oblig', period = period)
        capm_caisse = foyer_fiscal.declarant_principal('capm_caisse', period = period)
        capm_plfcc = foyer_fiscal.declarant_principal('capm_plfcc', period = period)
        capm_epinv = foyer_fiscal.declarant_principal('capm_epinv', period = period)
        capm_aut = foyer_fiscal.declarant_principal('capm_aut', period = period)

        return (
            capm_banq + capm_cent + capm_caut + capm_part + capm_oblig + capm_caisse +
            capm_plfcc + capm_epinv + capm_aut
            )


# 7. revenus de source étrangère

class retr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Autres revenus (revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        salaire_etranger = foyer_fiscal.declarant_principal('salaire_etranger', period = period)
        pension_etranger_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_transferee', period = period)
        pension_etranger_non_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_non_transferee', period = period)
        autres_revenus_etranger = foyer_fiscal.declarant_principal(
            'autres_revenus_etranger', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        return (
            salaire_etranger * (1 - tspr.abat_sal) +
            pension_etranger_non_transferee * (1 - tspr.abat_pen) +
            pension_etranger_transferee * (1 - tspr.abat_pen_etr) +
            autres_revenus_etranger
            )


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


class rng(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu net global"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bnc = foyer_fiscal('bnc', period = period)
        tspr = foyer_fiscal('tspr', period = period)
        revenus_fonciers = foyer_fiscal('revenus_fonciers', period = period)
        retr = foyer_fiscal('retr', period = period)
        rvcm = foyer_fiscal('rvcm', period = period)

        return bnc + tspr + revenus_fonciers + +rvcm + retr


#############################
#    Déductions
#############################

# # 1/ Au titre des revenus et bénéfices provenant de l’activité

# # 2/ Autres déductions


class deduction_interets(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Déductions intérêts issus de comptes spéciaux ou d'obligations"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        compte_special_epargne_banque = foyer_fiscal('compte_special_epargne_banque')
        compte_special_epargne_cent = foyer_fiscal('compte_special_epargne_cent')
        emprunt_obligataire = foyer_fiscal('emprunt_obligataire')
        deductions = parameters(period).deduc
        return max_(
            max_(
                max_(compte_special_epargne_banque, deductions.banq.plaf) +
                max_(compte_special_epargne_cent, deductions.cent.plaf),
                deductions.banq.plaf
                ) +
            max_(emprunt_obligataire, deductions.oblig.plaf), deductions.oblig.plaf
            )


class deduction_famille(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Déductions pour situation et charges de famille"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        # rng = foyer_fiscal('rng', period = period)
        chef_de_famille = foyer_fiscal('chef_de_famille', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        # nb_parents = foyer_fiscal('nb_parents', period = period)
        P = parameters(period.start).impot_revenu.deductions.fam
        #  chef de famille
        chef_de_famille = P.chef_de_famille * chef_de_famille

        enf = (nb_enf >= 1) * P.enf1 + (nb_enf >= 2) * P.enf2 + (nb_enf >= 3) * P.enf3 + (nb_enf >= 4) * P.enf4

        #    sup = P.enf_sup * nb_enf_sup
        #    infirme = P.infirme * nb_infirme
        #    parent = min_(P.parent_taux * rng, P.parent_max)

        #    return chef_de_famille + enf + sup + infirme + parent
        res = chef_de_famille + enf
        return res


class deduction_rente(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Arrérages et rentes payées à titre obligatoire et gratuit"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        rente = foyer_fiscal('rente', period = period)

        return rente  # TODO:


class deduction_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Primes afférentes aux contrats d'assurance-vie collectifs ou individuels"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        primes_assurance_vie = foyer_fiscal.members('prime_assurance_vie', period = period)
        somme_primes_assurance_vie = foyer_fiscal.sum(primes_assurance_vie)
        marie = foyer_fiscal.declarant_principal('statut_marital', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        P = parameters(period.start).impot_revenu.deductions.assurance_vie
        deduction = min_(somme_primes_assurance_vie, P.plaf + marie * P.conj_plaf + nb_enf * P.enf_plaf)
        return deduction


#     - Les remboursements des prêts universitaires en principal et en intérêts
#    - Revenus et bénéfices réinvestis dans les conditions et limites
#    prévues par la législation en vigueur dont notamment :
#     les revenus provenant de l'exportation, totalement pendant 10
#    ans à partir de la première opération d'exportation;
#     les revenus provenant de l’hébergement et de la restauration
#    des étudiants pendant dix ans ;
#     les revenus provenant du courtage international dans la limite
#    de 50% pendant 10 ans à partir de la première opération de courtage
#    international;
#     les montants déposés dans les comptes-épargne pour
#    l’investissement et dans les comptes-épargne en actions dans la
#    limite de 20.000D par an et sous réserve du minimum d’IR ;
#     la plus-value provenant des opérations de transmission des
#    entreprises en difficultés économiques ou des entreprises sous
#    forme de participations ou d’actifs pour départ du propriétaire à la
#    retraite ou pour incapacité de poursuivre la gestion et ce, sous
#    certaines conditions,
#     la plus-value provenant de l’apport d’une entreprise individuelle
#    au capital d’une société ;
#     les revenus réinvestis dans la souscription au capital des
#    entreprises dans les conditions prévues par la législation relative aux
#    incitations fiscales;
#     les revenus réinvestis dans la réalisation de projets
#    d’hébergement et de restauration universitaires sous réserve du
#    minimum d’IR.
#     Les revenus provenant de la location des terres agricoles
#    réservées aux grandes cultures objet de contrat de location conclus
#    pour une période minimale de trois ans.


class deduction_smig(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        chef = foyer_fiscal('chef_de_famille', period = period)

        return 0 * chef  # TODO: voir avec tspr


class revenu_net_imposable(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu net imposable"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses
        et charges professionnelles et des revenus non soumis à l'impôt
        '''
        rng = foyer_fiscal('rng', period = period)
        deduction_famille = foyer_fiscal('deduction_famille', period = period)
        deduction_rente = foyer_fiscal.declarant_principal('rente', period = period)
        deduction_assurance_vie = foyer_fiscal('deduction_assurance_vie', period = period)
        return rng - (deduction_famille + deduction_rente + deduction_assurance_vie)


class impot_revenu_brut(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Impôt brut avant non-imposabilité"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_net_imposable = foyer_fiscal('revenu_net_imposable', period = period)
        bareme = parameters(period.start).impot_revenu.bareme
        impot_revenu_brut = - bareme.calc(revenu_net_imposable)
        return impot_revenu_brut


class exoneration(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"Exoneration de l'impôt sur le revenu des personnes physiques"
    definition_period = YEAR
    end = '2016-12-31'

    def formula_2014(foyer_fiscal, period, parameters):
        # Les éligibles ne doivent percevoir que des salaires et des pensions
        rng = foyer_fiscal('rng', period = period)
        tspr = foyer_fiscal('tspr', period = period)
        eligble = (rng == tspr)
        # Condition de revenu
        deduction_famille = foyer_fiscal('deduction_famille', period = period)
        condition_de_revenu = (
            rng - deduction_famille
            ) <= parameters(period.start).impot_revenu.exoneration.seuil
        return eligble * condition_de_revenu


class irpp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Impôt sur le revenu des personnes physiques"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        impot_revenu_brut = foyer_fiscal('impot_revenu_brut', period = period)
        exoneration = foyer_fiscal('exoneration', period = period)
        return impot_revenu_brut * not_(exoneration)


class irpp_mensuel_salarie(Variable):
    value_type = float
    entity = Individu
    label = u"Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés"
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_imposable = individu('salaire_imposable', period = period)
        deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)

        return calcule_impot_revenu_brut(
            salaire_imposable, deduction_famille_annuelle, period, parameters,
            )


# Utils

def calcule_impot_revenu_brut(salaire_mensuel, deduction_famille_annuelle, period, parameters):
    revenu_assimile_salaire = salaire_mensuel
    smig_40h_mensuel = parameters(period.start).cotisations_sociales.gen.smig_40h_mensuel
    smig = revenu_assimile_salaire <= smig_40h_mensuel
    tspr = parameters(period.start).impot_revenu.tspr

    if period.start.year >= 2011:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal) - max_(smig * tspr.smig,
                (revenu_assimile_salaire <= tspr.smig_ext) * tspr.smig), 0)
    else:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.smig, 0)
    bareme = parameters(period.start).impot_revenu.bareme

    non_exonere = revenu_assimile_salaire_apres_abattement >= 0
    if 2014 <= period.start.year <= 2016:
        non_exonere = (
            (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
            ) > parameters(period.start).impot_revenu.exoneration.seuil

    return - 1.0 * non_exonere * bareme.calc(
        (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
        ) / 12
