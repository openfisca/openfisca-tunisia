# -*- coding: utf-8 -*-


from __future__ import division

from numpy import logical_or as or_, maximum as max_, minimum as min_

from openfisca_tunisia.model.base import *  # noqa analysis:ignore


class nb_enf(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Nombre d'enfants"

    def function(foyer_fiscal, period, legislation):
        '''
        TODO: fixme
        '''
        period = period.this_year
        age = foyer_fiscal.members('age', period = period)
        P = legislation(period.start).impot_revenu.deduc.fam
        # res =+ (
        #    (ag < 20) +
        #    (ag < 25)*not_(boursier)*()
        #    )
        condition = (age >= 0) * (age <= P.age)
        return period, foyer_fiscal.sum(condition, role = FoyerFiscal.PERSONNE_A_CHARGE)


class nb_enf_sup(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Nombre d'enfants étudiants du supérieur non boursiers"

    def function(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants étudiants du supérieur non boursiers
        '''
        period = period.this_year
        age = foyer_fiscal.members('age', period = period)
        boursier = foyer_fiscal.members('boursier', period = period)

        return period, 0 * age * not_(boursier)


class nb_infirme(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Nombre d'enfants infirmes"

    def function(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants infirmes
        '''
        period = period.this_year
        age = foyer_fiscal.members('age', period = period)
        invalide = foyer_fiscal.members('invalide', period = period)

        return period, 0 * age * invalide


class nb_parents(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Nombre de parents"

    def function(foyer_fiscal, period):
        '''
        TODO: Nombre de parents
        '''
        period = period.this_year
        return period, (
            (foyer_fiscal.declarant_principal('age', period) > 20) +
            (foyer_fiscal.declarant_principal('age', period) > 20)
            )


class chef_de_famille(Variable):
    column = BoolCol()
    entity = FoyerFiscal
    label = u"Indicatrice de chef de famille"
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

    def function(foyer_fiscal, period):
        period = period.this_year
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

        return period, chef_de_famille


###############################################################################
# Revenus catégoriels
###############################################################################


# 1. Bénéfices industriels et commerciaux
class bic(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Bénéfices industriels et commerciaux (BIC)"

    def function(foyer_fiscal, period):
        period = period.this_year
        bic_reel_res = foyer_fiscal('bic_reel_res', period = period)
        # TODO:
        #    return period, bic_reel + bic_simpl + bic_forf
        return period, bic_reel_res


# régime réel
# régime réel simplifié
# régime forfaitaire


class bic_ca_global(Variable):
    column = FloatCol
    entity = Individu
    label = u"Chiffre d’affaires global (BIC, cession de fond de commerce"

    def function(foyer_fiscal, period):
        """
        Chiffre d’affaires global
        des personnes soumises au régime forfaitaire ayant cédé le fond de commerce
        """
        period = period.this_year
        bic_ca_revente = foyer_fiscal('bic_ca_revente', period = period)
        bic_ca_autre = foyer_fiscal('bic_ca_autre', period = period)

        return period, bic_ca_revente + bic_ca_autre


class bic_res_cession(Variable):
    column = FloatCol
    entity = Individu
    label = u"Résultat (BIC, cession de fond de commerce)"

    def function(foyer_fiscal, period):
        period = period.this_year
        bic_ca_global = foyer_fiscal('bic_ca_global', period = period)
        bic_depenses = foyer_fiscal('bic_depenses', period = period)

        return period, max_(bic_ca_global - bic_depenses, 0)


class bic_benef_fiscal_cession(Variable):
    column = FloatCol
    entity = Individu
    label = u"Bénéfice fiscal (BIC, cession de fond de commerce)"

    def function(foyer_fiscal, period):
        period = period.this_year
        bic_res_cession = foyer_fiscal('bic_res_cession', period = period)
        bic_pv_cession = foyer_fiscal('bic_pv_cession', period = period)

        return period, bic_res_cession + bic_pv_cession


def _bic_res_net(bic_benef_fiscal_cession, bic_part_benef_sp):
    """
    Résultat net BIC TODO: il manque le régime réel
    """
    return period, bic_benef_fiscal_cession + bic_part_benef_sp


# 2. Bénéfices des professions non commerciales
class bnc(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Bénéfices des professions non commerciales (BNC)"

    def function(foyer_fiscal, period):
        period = period.this_year
        bnc_reel_res_fiscal = foyer_fiscal('bnc_reel_res_fiscal', period = period)
        bnc_forf_benef_fiscal = foyer_fiscal('bnc_forf_benef_fiscal', period = period)
        bnc_part_benef_sp = foyer_fiscal('bnc_part_benef_sp', period = period)

        return period, bnc_reel_res_fiscal + bnc_forf_benef_fiscal + bnc_part_benef_sp


class bnc_forf_benef_fiscal(Variable):
    column = FloatCol
    entity = Individu
    label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)"

    def function(foyer_fiscal, period, legislation):
        """
        Bénéfice fiscal (régime forfaitaire, 70% des recettes brutes TTC)
        """
        period = period.this_year
        bnc_forf_rec_brut = foyer_fiscal('bnc_forf_rec_brut', period = period)
        part = legislation(period.start).impot_revenu.bnc.forf.part_forf
        return period, bnc_forf_rec_brut * part


# 3. Bénéfices de l'exploitation agricole et de pêche
class beap(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Bénéfices de l'exploitation agricole et de pêche (BEAP)"

    def function(foyer_fiscal, period):
        period = period.this_year
        beap_reel_res_fiscal = foyer_fiscal('beap_reel_res_fiscal', period = period)
        beap_reliq_benef_fiscal = foyer_fiscal('beap_reliq_benef_fiscal', period = period)
        beap_monogr = foyer_fiscal('beap_monogr', period = period)
        beap_part_benef_sp = foyer_fiscal('beap_part_benef_sp', period = period)

        return period, beap_reel_res_fiscal + beap_reliq_benef_fiscal + beap_monogr + beap_part_benef_sp


# 4. Revenus fonciers

class revenus_fonciers(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenus fonciers"

    def function(foyer_fiscal, period):
        period = period.this_year
        fon_reel_fisc = foyer_fiscal.declarant_principal('fon_reel_fisc', period = period)
        fon_forf_bati = foyer_fiscal('fon_forf_bati', period = period)
        fon_forf_nbat = foyer_fiscal('fon_forf_nbat', period = period)
        fon_sp = foyer_fiscal.declarant_principal('fon_sp', period = period)

        return period, fon_reel_fisc + fon_forf_bati + fon_forf_nbat + fon_sp


class fon_forf_bati(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenus fonciers net des immeubles bâtis"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        fon_forf_bati_rec = foyer_fiscal.declarant_principal('fon_forf_bati_rec', period = period)
        fon_forf_bati_rel = foyer_fiscal.declarant_principal('fon_forf_bati_rel', period = period)
        fon_forf_bati_fra = foyer_fiscal.declarant_principal('fon_forf_bati_fra', period = period)
        fon_forf_bati_tax = foyer_fiscal.declarant_principal('fon_forf_bati_tax', period = period)
        P = legislation(period.start).impot_revenu.fon.bati.deduc_frais
        return period, max_(
            0,
            fon_forf_bati_rec * (1 - P) + fon_forf_bati_rel - fon_forf_bati_fra - fon_forf_bati_tax
            )


class fon_forf_nbat(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenus fonciers net des terrains non bâtis"

    def function(foyer_fiscal, period):
        period = period.this_year
        fon_forf_nbat_rec = foyer_fiscal.declarant_principal('fon_forf_nbat_rec', period = period)
        fon_forf_nbat_dep = foyer_fiscal.declarant_principal('fon_forf_nbat_dep', period = period)
        fon_forf_nbat_tax = foyer_fiscal.declarant_principal('fon_forf_nbat_tax', period = period)
        return period, max_(0, fon_forf_nbat_rec - fon_forf_nbat_dep - fon_forf_nbat_tax)


# 5. Traitements, salaires, indemnités, pensions et rentes viagères

class tspr(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Traitements, salaires, indemnités, pensions et rentes viagères"

    def function(foyer_fiscal, period):
        period = period.this_year
        revenu_assimile_salaire_apres_abattements = foyer_fiscal(
            'revenu_assimile_salaire_apres_abattements', period = period)
        revenu_assimile_pension_apres_abattements = foyer_fiscal(
            'revenu_assimile_pension_apres_abattements', period = period)

        return period, revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements


class revenu_assimile_salaire(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenu assimilé à des salaires"

    def function(foyer_fiscal, period):
        period = period.this_year
        salaire_imposable = foyer_fiscal.declarant_principal('salaire_imposable', period = period)
        salaire_en_nature = foyer_fiscal.declarant_principal('salaire_en_nature', period = period)
        return period, (salaire_imposable + salaire_en_nature)


class smig(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig_dec = foyer_fiscal.declarant_principal('smig_dec', period = period)
        smig_40h_mensuel = legislation(period.start).cotisations_sociales.gen.smig_40h_mensuel
        smig = or_(smig_dec, revenu_assimile_salaire <= 12 * smig_40h_mensuel)
        return period, smig


class revenu_assimile_salaire_apres_abattements(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenu imposé comme des salaires net des abatements"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = legislation(period.start).impot_revenu.tspr

        if period.start.year >= 2011:
            res = max_(
                revenu_assimile_salaire * (1 - tspr.abat_sal) - max_(smig * tspr.smig,
                 (revenu_assimile_salaire <= tspr.smig_ext) * tspr.smig), 0)
        else:
            res = max_(revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.smig, 0)
        return period, res


class revenu_assimile_pension_apres_abattements(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenu assimilé à des pensions après abattements"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        revenu_assimile_pension = foyer_fiscal.declarant_principal('revenu_assimile_pension', period = period)
        avantages_nature_assimile_pension = foyer_fiscal.declarant_principal(
            'avantages_nature_assimile_pension', period = period)
        tspr = legislation(period.start).impot_revenu.tspr
        return period, (revenu_assimile_pension + avantages_nature_assimile_pension) * (1 - tspr.abat_pen)


# 6. Revenus de valeurs mobilières et de capitaux mobiliers

class rvcm(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenus de valeurs mobilières et de capitaux mobiliers"

    def function(foyer_fiscal, period):
        period = period.this_year
        capm_banq = foyer_fiscal.declarant_principal('capm_banq', period = period)
        capm_cent = foyer_fiscal.declarant_principal('capm_cent', period = period)
        capm_caut = foyer_fiscal.declarant_principal('capm_caut', period = period)
        capm_part = foyer_fiscal.declarant_principal('capm_part', period = period)
        capm_oblig = foyer_fiscal.declarant_principal('capm_oblig', period = period)
        capm_caisse = foyer_fiscal.declarant_principal('capm_caisse', period = period)
        capm_plfcc = foyer_fiscal.declarant_principal('capm_plfcc', period = period)
        capm_epinv = foyer_fiscal.declarant_principal('capm_epinv', period = period)
        capm_aut = foyer_fiscal.declarant_principal('capm_aut', period = period)

        return period, (
            capm_banq + capm_cent + capm_caut + capm_part + capm_oblig + capm_caisse +
            capm_plfcc + capm_epinv + capm_aut
            )


# 7. revenus de source étrangère

class retr(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Autres revenus (revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine)"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        salaire_etranger = foyer_fiscal.declarant_principal('salaire_etranger', period = period)
        pension_etranger_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_transferee', period = period)
        pension_etranger_non_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_non_transferee', period = period)
        autres_revenus_etranger = foyer_fiscal.declarant_principal(
            'autres_revenus_etranger', period = period)
        tspr = legislation(period.start).impot_revenu.tspr

        return period, (
            salaire_etranger * (1 - tspr.abat_sal) +
            pension_etranger_non_transferee * (1 - tspr.abat_pen) +
            pension_etranger_transferee * (1 - tspr.abat_pen_etr) +
            autres_revenus_etranger
            )


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


class rng(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenu net global"

    def function(foyer_fiscal, period):
        period = period.this_year
        tspr = foyer_fiscal('tspr', period = period)
        revenus_fonciers = foyer_fiscal('revenus_fonciers', period = period)
        retr = foyer_fiscal('retr', period = period)
        rvcm = foyer_fiscal('rvcm', period = period)

        return period, tspr + revenus_fonciers + +rvcm + retr


#############################
#    Déductions
#############################

# # 1/ Au titre des revenus et bénéfices provenant de l’activité

# # 2/ Autres déductions


class deduction_interets(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Déductions intérêts issus de comptes spéciaux ou d'obligations"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        compte_special_epargne_banque = foyer_fiscal('compte_special_epargne_banque')
        compte_special_epargne_cent = foyer_fiscal('compte_special_epargne_cent')
        emprunt_obligataire = foyer_fiscal('emprunt_obligataire')
        deductions = legislation(period).deduc
        return period, max_(
            max_(
                max_(compte_special_epargne_banque, deductions.banq.plaf) +
                max_(compte_special_epargne_cent, deductions.cent.plaf),
                deductions.banq.plaf
                ) +
            max_(emprunt_obligataire, deductions.oblig.plaf), deductions.oblig.plaf
            )


class deduction_famille(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Déductions pour situation et charges de famille"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        # rng = foyer_fiscal('rng', period = period)
        chef_de_famille = foyer_fiscal('chef_de_famille', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        # nb_parents = foyer_fiscal('nb_parents', period = period)
        P = legislation(period.start).impot_revenu.deduc.fam
        #  chef de famille
        chef_de_famille = P.chef_de_famille * chef_de_famille

        enf = (nb_enf >= 1) * P.enf1 + (nb_enf >= 2) * P.enf2 + (nb_enf >= 3) * P.enf3 + (nb_enf >= 4) * P.enf4

        #    sup = P.enf_sup * nb_enf_sup
        #    infirme = P.infirme * nb_infirme
        #    parent = min_(P.parent_taux * rng, P.parent_max)

        #    return period, chef_de_famille + enf + sup + infirme + parent
        res = chef_de_famille + enf
        return period, res


class deduction_rente(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Arrérages et rentes payées à titre obligatoire et gratuit"

    def function(foyer_fiscal, period):
        period = period.this_year
        rente = foyer_fiscal('rente', period = period)

        return period, rente  # TODO:


class deduction_assurance_vie(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Primes afférentes aux contrats d'assurance-vie"

    def function(foyer_fiscal, period, legislation):
        '''
        Primes afférentes aux contrats d'assurance-vie collectifs ou individuels
        '''
        period = period.this_year
        primes_assurance_vie = foyer_fiscal.members('prime_assurance_vie', period = period)
        somme_primes_assurance_vie = foyer_fiscal.sum(primes_assurance_vie)
        marie = foyer_fiscal.declarant_principal('statut_marital', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        P = legislation(period.start).impot_revenu.deduc.assurance_vie
        deduction = min_(somme_primes_assurance_vie, P.plaf + marie * P.conj_plaf + nb_enf * P.enf_plaf)
        return period, deduction


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


class deduc_smig(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG"

    def function(foyer_fiscal, period):
        period = period.this_year
        chef = foyer_fiscal('chef_de_famille', period = period)

        return period, 0 * chef  # TODO: voir avec tspr


class rni(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Revenu net imposable"

    def function(foyer_fiscal, period):
        '''
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses
        et charges professionnelles
        et des revenus non soumis à l'impôt
        '''
        period = period.this_year
        rng = foyer_fiscal('rng', period = period)
        deduction_famille = foyer_fiscal('deduction_famille', period = period)
        deduction_rente = foyer_fiscal.declarant_principal('rente', period = period)
        deduction_assurance_vie = foyer_fiscal('deduction_assurance_vie', period = period)
        return period, rng - (deduction_famille + deduction_rente + deduction_assurance_vie)


class ir_brut(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Impôt avant non-imposabilité"

    def function(foyer_fiscal, period, legislation):
        period = period.this_year
        rni = foyer_fiscal('rni', period = period)
        bareme = legislation(period.start).impot_revenu.bareme
        # exemption = legislation(period.start).impot_revenu.reforme.exemption
        # rni_apres_exemption = rni * (exemption.active == 0) + rni * (exemption.active == 1) * (rni > exemption.max)
        rni_apres_exemption = rni
        ir_brut = - bareme.calc(rni_apres_exemption)
        return period, ir_brut


class irpp(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Impôt sur le revenu des personnes physiques"

    def function(foyer_fiscal, period):
        period = period.this_year
        ir_brut = foyer_fiscal('ir_brut', period = period)
        irpp = ir_brut
        return period, irpp
