# -*- coding: utf-8 -*-


from __future__ import division

from numpy import logical_or as or_, maximum as max_, minimum as min_

from openfisca_tunisia.model.base import *  # noqa analysis:ignore


ALL = [x[1] for x in QUIFOY]
PACS = [QUIFOY['pac' + str(i)] for i in range(1, 10)]


class nb_enf(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants"

    def function(self, simulation, period):
        '''
        TODO: fixme
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period = period)
        _P = simulation.legislation_at(period.start)

        age = self.split_by_roles(age_holder, roles = PACS)
        P = _P.impot_revenu.deduc.fam
    #    res = None
    #    i = 1
    #    if res is None: res = zeros(len(age))
    #    for key, ag in age.iteritems():
    #        i += 1
    #        res =+ ( (ag < 20) +
    #                 (ag < 25)*not_(boursier)*() )
        res = 0
        for ag in age.itervalues():
            res += 1 * (ag < P.age) * (ag >= 0)
        return period, res


class nb_enf_sup(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants étudiant du supérieur non boursiers"

    def function(self, simulation, period):
        '''
        TODO: Nombre d'enfants étudiant du supérieur non boursiers
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_en_mois = simulation.calculate('age_en_mois', period = period)
        boursier = simulation.calculate('boursier', period = period)

        return period, 0 * age_en_mois * not_(boursier)


class nb_infirme(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants infirmes"

    def function(self, simulation, period):
        '''
        TODO: Nombre d'enfants infirmes
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_en_mois = simulation.calculate('age_en_mois', period = period)
        inv = simulation.calculate('inv', period = period)

        return period, 0 * age_en_mois * inv


class nb_parents(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre de parents"

    def function(self, simulation, period):
        '''
        TODO: Nombre de parents
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_en_mois_holder = simulation.compute('age_en_mois', period = period)

        age_en_mois_vous = self.filter_role(age_en_mois_holder, role = VOUS)
        age_en_mois_conj = self.filter_role(age_en_mois_holder, role = CONJ)
        return period, (age_en_mois_vous > 10 * 12) + (age_en_mois_conj > 10 * 12)


class chef_de_famille(Variable):
    column = BoolCol()
    entity_class = FoyersFiscaux
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

    def function(self, simulation, period):
        period = period.this_year
        male = self.filter_role(
            simulation.calculate('male', period = period),
            role = VOUS,
            )
        marie = self.filter_role(
            simulation.calculate('marie', period = period),
            role = VOUS,
            )
        divorce = self.filter_role(
            simulation.calculate('divorce', period = period),
            role = VOUS,
            )
        veuf = self.filter_role(
            simulation.calculate('veuf', period = period),
            role = VOUS,
            )
        nb_enf = simulation.calculate('nb_enf', period = period)
        chef_de_famille = (
            veuf |
            (marie & male) |
            (divorce & (nb_enf > 0))  # | 
            # (marie & (not male)) |
            )

        return period, chef_de_famille


###############################################################################
# # Revenus catégoriels
###############################################################################


# 1. Bénéfices industriels et commerciaux
class bic(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Bénéfices industriels et commerciaux"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        bic_reel_res = simulation.calculate('bic_reel_res', period = period)
        # TODO:
        #    return period, bic_reel + bic_simpl + bic_forf
        return period, bic_reel_res


# régime réel
# régime réel simplifié
# régime forfaitaire


class bic_ca_global(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Chiffre d’affaires global (BIC, cession de fond de commerce"

    def function(self, simulation, period):
        """
        Chiffre d’affaires global
        des personnes soumises au régime forfaitaire ayant cédé le fond de commerce
        """
        period = period.start.offset('first-of', 'month').period('year')
        bic_ca_revente = simulation.calculate('bic_ca_revente', period = period)
        bic_ca_autre = simulation.calculate('bic_ca_autre', period = period)

        return period, bic_ca_revente + bic_ca_autre


class bic_res_cession(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Résultat (BIC, cession de fond de commerce)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        bic_ca_global = simulation.calculate('bic_ca_global', period = period)
        bic_depenses = simulation.calculate('bic_depenses', period = period)

        return period, max_(bic_ca_global - bic_depenses, 0)


class bic_benef_fiscal_cession(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bénéfice fiscal (BIC, cession de fond de commerce)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        bic_res_cession = simulation.calculate('bic_res_cession', period = period)
        bic_pv_cession = simulation.calculate('bic_pv_cession', period = period)

        return period, bic_res_cession + bic_pv_cession


def _bic_res_net(bic_benef_fiscal_cession, bic_part_benef_sp):
    """
    Résultat net BIC TODO: il manque le régime réel
    """
    return period, bic_benef_fiscal_cession + bic_part_benef_sp


# 2. Bénéfices des professions non commerciales
class bnc(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Bénéfices des professions non commerciales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        bnc_reel_res_fiscal = simulation.calculate('bnc_reel_res_fiscal', period = period)
        bnc_forf_benef_fiscal = simulation.calculate('bnc_forf_benef_fiscal', period = period)
        bnc_part_benef_sp = simulation.calculate('bnc_part_benef_sp', period = period)

        return period, bnc_reel_res_fiscal + bnc_forf_benef_fiscal + bnc_part_benef_sp


class bnc_forf_benef_fiscal(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)"

    def function(self, simulation, period):
        """
        Bénéfice fiscal (régime forfaitaire, 70% des recettes brutes TTC)
        """
        period = period.start.offset('first-of', 'month').period('year')
        bnc_forf_rec_brut = simulation.calculate('bnc_forf_rec_brut', period = period)
        _P = simulation.legislation_at(period.start)

        part = _P.impot_revenu.bnc.forf.part_forf
        return period, bnc_forf_rec_brut * part


# 3. Bénéfices de l'exploitation agricole et de pêche
class beap(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Bénéfices de l'exploitation agricole et de pêche"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        beap_reel_res_fiscal = simulation.calculate('beap_reel_res_fiscal', period = period)
        beap_reliq_benef_fiscal = simulation.calculate('beap_reliq_benef_fiscal', period = period)
        beap_monogr = simulation.calculate('beap_monogr', period = period)
        beap_part_benef_sp = simulation.calculate('beap_part_benef_sp', period = period)

        return period, beap_reel_res_fiscal + beap_reliq_benef_fiscal + beap_monogr + beap_part_benef_sp


# 4. Revenus fonciers

class revenus_fonciers(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus fonciers"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        fon_reel_fisc_holder = simulation.compute('fon_reel_fisc', period = period)
        fon_forf_bati = simulation.calculate('fon_forf_bati', period = period)
        fon_forf_nbat = simulation.calculate('fon_forf_nbat', period = period)
        fon_sp_holder = simulation.compute('fon_sp', period = period)

        fon_reel_fisc = self.filter_role(fon_reel_fisc_holder, role = VOUS)
        fon_sp = self.filter_role(fon_sp_holder, role = VOUS)
        return period, fon_reel_fisc + fon_forf_bati + fon_forf_nbat + fon_sp


class fon_forf_bati(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus fonciers net des immeubles bâtis"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        fon_forf_bati_rec_holder = simulation.compute('fon_forf_bati_rec', period = period)
        fon_forf_bati_rel_holder = simulation.compute('fon_forf_bati_rel', period = period)
        fon_forf_bati_fra_holder = simulation.compute('fon_forf_bati_fra', period = period)
        fon_forf_bati_tax_holder = simulation.compute('fon_forf_bati_tax', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.fon.bati.deduc_frais
        fon_forf_bati_rec = self.filter_role(fon_forf_bati_rec_holder, role = VOUS)
        fon_forf_bati_rel = self.filter_role(fon_forf_bati_rel_holder, role = VOUS)
        fon_forf_bati_fra = self.filter_role(fon_forf_bati_fra_holder, role = VOUS)
        fon_forf_bati_tax = self.filter_role(fon_forf_bati_tax_holder, role = VOUS)
        return period, max_(0, fon_forf_bati_rec * (1 - P) + fon_forf_bati_rel - fon_forf_bati_fra - fon_forf_bati_tax)


class fon_forf_nbat(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus fonciers net des terrains non bâtis"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        fon_forf_nbat_rec_holder = simulation.compute('fon_forf_nbat_rec', period = period)
        fon_forf_nbat_dep_holder = simulation.compute('fon_forf_nbat_dep', period = period)
        fon_forf_nbat_tax_holder = simulation.compute('fon_forf_nbat_tax', period = period)
        fon_forf_nbat_rec = self.filter_role(fon_forf_nbat_rec_holder, role = VOUS)
        fon_forf_nbat_dep = self.filter_role(fon_forf_nbat_dep_holder, role = VOUS)
        fon_forf_nbat_tax = self.filter_role(fon_forf_nbat_tax_holder, role = VOUS)
        return period, max_(0, fon_forf_nbat_rec - fon_forf_nbat_dep - fon_forf_nbat_tax)


# 5. Traitements, salaires, indemnités, pensions et rentes viagères

class tspr(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Traitements, salaires, indemnités, pensions et rentes viagères"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenu_assimile_salaire_apres_abattements = simulation.calculate(
            'revenu_assimile_salaire_apres_abattements', period = period)
        revenu_assimile_pension_apres_abattements = simulation.calculate(
            'revenu_assimile_pension_apres_abattements', period = period)

        return period, revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements


class revenu_assimile_salaire(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu assimilé à des salaires"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        salaire_imposable_holder = simulation.compute('salaire_imposable', period = period)
        salaire_en_nature_holder = simulation.compute('salaire_en_nature', period = period)

        salaire_imposable = self.sum_by_entity(salaire_imposable_holder, roles = [VOUS, CONJ])
        salaire_en_nature = self.sum_by_entity(salaire_en_nature_holder, roles = [VOUS, CONJ])
        return period, (salaire_imposable + salaire_en_nature)


class smig(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenu_assimile_salaire = simulation.calculate('revenu_assimile_salaire', period = period)
        smig_dec_holder = simulation.compute('smig_dec', period = period)
        _P = simulation.legislation_at(period.start)

        # TODO: should be better implemented
        smig_dec = self.filter_role(smig_dec_holder, role = VOUS)
        smig = or_(smig_dec, revenu_assimile_salaire <= 12 * _P.cotisations_sociales.gen.smig)
        return period, smig


class revenu_assimile_salaire_apres_abattements(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu imposé comme des salaires net des abatements"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenu_assimile_salaire = simulation.calculate('revenu_assimile_salaire', period = period)
        smig = simulation.calculate('smig', period = period)
        tspr = simulation.legislation_at(period.start).impot_revenu.tspr

        if period.start.year >= 2011:
            res = max_(
                revenu_assimile_salaire * (1 - tspr.abat_sal) - max_(smig * tspr.smig,
                 (revenu_assimile_salaire <= tspr.smig_ext) * tspr.smig), 0)
        else:
            res = max_(revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.smig, 0)
        return period, res


class revenu_assimile_pension_apres_abattements(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu assimilé à des pensions après abattements"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        revenu_assimile_pension_holder = simulation.compute('revenu_assimile_pension', period = period)
        avantages_nature_assimile_pension_holder = simulation.compute(
            'avantages_nature_assimile_pension', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.tspr
        revenu_assimile_pension = self.filter_role(revenu_assimile_pension_holder, role = VOUS)
        avantages_nature_assimile_pension = self.filter_role(avantages_nature_assimile_pension_holder, role = VOUS)
        return period, (revenu_assimile_pension + avantages_nature_assimile_pension) * (1 - P.abat_pen)


# 6. Revenus de valeurs mobilières et de capitaux mobiliers

class rvcm(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus de valeurs mobilières et de capitaux mobiliers"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        capm_banq_holder = simulation.compute('capm_banq', period = period)
        capm_cent_holder = simulation.compute('capm_cent', period = period)
        capm_caut_holder = simulation.compute('capm_caut', period = period)
        capm_part_holder = simulation.compute('capm_part', period = period)
        capm_oblig_holder = simulation.compute('capm_oblig', period = period)
        capm_caisse_holder = simulation.compute('capm_caisse', period = period)
        capm_plfcc_holder = simulation.compute('capm_plfcc', period = period)
        capm_epinv_holder = simulation.compute('capm_epinv', period = period)
        capm_aut_holder = simulation.compute('capm_aut', period = period)

        capm_banq = self.filter_role(capm_banq_holder, role = VOUS)
        capm_cent = self.filter_role(capm_cent_holder, role = VOUS)
        capm_caut = self.filter_role(capm_caut_holder, role = VOUS)
        capm_part = self.filter_role(capm_part_holder, role = VOUS)
        capm_oblig = self.filter_role(capm_oblig_holder, role = VOUS)
        capm_caisse = self.filter_role(capm_caisse_holder, role = VOUS)
        capm_plfcc = self.filter_role(capm_plfcc_holder, role = VOUS)
        capm_epinv = self.filter_role(capm_epinv_holder, role = VOUS)
        capm_aut = self.filter_role(capm_aut_holder, role = VOUS)

        return period, (
            capm_banq + capm_cent + capm_caut + capm_part + capm_oblig + capm_caisse +
            capm_plfcc + capm_epinv + capm_aut
            )


# 7. revenus de source étrangère

class retr(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Autres revenus (revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        salaire_etranger_holder = simulation.compute('salaire_etranger', period = period)
        pension_etranger_non_transferee_holder = simulation.compute('pension_etranger_non_transferee', period = period)
        pension_etranger_transferee_holder = simulation.compute('pension_etranger_transferee', period = period)
        autres_revenus_etranger_holder = simulation.compute('autres_revenus_etranger', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.tspr
        salaire_etranger = self.filter_role(salaire_etranger_holder, role = VOUS)
        pension_etranger_non_transferee = self.filter_role(pension_etranger_non_transferee_holder, role = VOUS)
        pension_etranger_transferee = self.filter_role(pension_etranger_transferee_holder, role = VOUS)
        autres_revenus_etranger = self.filter_role(autres_revenus_etranger_holder, role = VOUS)
        return period, (
            salaire_etranger * (1 - P.abat_sal) +
            pension_etranger_non_transferee * (1 - P.abat_pen) +
            pension_etranger_transferee * (1 - P.abat_pen_etr) +
            autres_revenus_etranger
            )


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


class rng(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net global"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        tspr = simulation.calculate('tspr', period = period)
        revenus_fonciers = simulation.calculate('revenus_fonciers', period = period)
        retr = simulation.calculate('retr', period = period)
        rvcm = simulation.calculate('rvcm', period = period)

        return period, tspr + revenus_fonciers + +rvcm + retr


#############################
#    Déductions
#############################

# # 1/ Au titre des revenus et bénéfices provenant de l’activité

# # 2/ Autres déductions


def _deduc_int(capm_banq, capm_cent, capm_oblig, _P):
    P = _P.deduc
    return period, max_(
        max_(
            max_(capm_banq, P.banq.plaf) + max_(capm_cent, P.cent.plaf),
            P.banq.plaf
            ) +
        max_(capm_oblig, P.oblig.plaf), P.oblig.plaf
        )


class deduction_famille(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déductions pour situation et charges de famille"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        # rng = simulation.calculate('rng', period = period)
        chef_de_famille = self.any_by_roles(
            simulation.calculate('chef_de_famille', period = period)
            )
        nb_enf = simulation.calculate('nb_enf', period = period)
        # nb_parents = simulation.calculate('nb_parents', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.deduc.fam
        #  chef de famille
        chef_de_famille = P.chef_de_famille * chef_de_famille

        enf = (nb_enf >= 1) * P.enf1 + (nb_enf >= 2) * P.enf2 + (nb_enf >= 3) * P.enf3 + (nb_enf >= 4) * P.enf4

        #    sup = P.enf_sup * nb_enf_sup
        #    infirme = P.infirme * nb_infirme
        #    parent = min_(P.parent_taux * rng, P.parent_max)

        #    return period, chef_de_famille + enf + sup + infirme + parent
        res = chef_de_famille + enf
        return period, res


class deduc_rente(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Arrérages et rentes payées à titre obligatoire et gratuit"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        rente = simulation.calculate('rente', period = period)

        return period, rente  # TODO:


class assurance_vie(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Primes afférentes aux contrats d'assurance-vie"

    def function(self, simulation, period):
        '''
        Primes afférentes aux contrats d'assurance-vie collectifs ou individuels
        '''
        period = period.start.offset('first-of', 'month').period('year')
        prime_assurance_vie_holder = simulation.compute('prime_assurance_vie', period = period)
        statut_marital_holder = simulation.compute('statut_marital', period = period)
        nb_enf = simulation.calculate('nb_enf', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.deduc.assurance_vie
        marie = self.filter_role(statut_marital_holder, role = VOUS)  # TODO
        prime_assurance_vie = self.sum_by_entity(prime_assurance_vie_holder)
        deduc = min_(prime_assurance_vie, P.plaf + marie * P.conj_plaf + nb_enf * P.enf_plaf)
        return period, deduc


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
    entity_class = FoyersFiscaux
    label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        chef = simulation.calculate('chef_de_famille', period = period)

        return period, 0 * chef  # TODO: voir avec tspr


class rni(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net imposable"

    def function(self, simulation, period):
        '''
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses
        et charges professionnelles
        et des revenus non soumis à l'impôt
        '''
        period = period.start.offset('first-of', 'month').period('year')
        rng = simulation.calculate('rng', period = period)
        deduction_famille = simulation.calculate('deduction_famille', period = period)
        rente_holder = simulation.compute('rente', period = period)
        assurance_vie = simulation.calculate('assurance_vie', period = period)

        rente = self.filter_role(rente_holder, role = VOUS)
        return period, rng - (deduction_famille + rente + assurance_vie)


class ir_brut(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt avant non-imposabilité"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        rni = simulation.calculate('rni', period = period)
        _P = simulation.legislation_at(period.start)

        bar = _P.impot_revenu.bareme
        # exemption = _P.impot_revenu.reforme.exemption
        # rni_apres_exemption = rni * (exemption.active == 0) + rni * (exemption.active == 1) * (rni > exemption.max)
        rni_apres_exemption = rni
        ir_brut = -bar.calc(rni_apres_exemption)
        return period, ir_brut


class irpp(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu des personnes physiques"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        ir_brut = simulation.calculate('ir_brut', period = period)
        # _P = simulation.legislation_at(period.start)

        irpp = ir_brut
        return period, irpp
