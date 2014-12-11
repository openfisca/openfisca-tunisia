# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import datetime64, logical_or as or_, maximum as max_, minimum as min_

from .base import *


ALL = [x[1] for x in QUIFOY]
PACS = [QUIFOY['pac' + str(i)] for i in range(1, 10)]


###############################################################################
# # Initialisation de quelques variables utiles pour la suite
###############################################################################


@reference_formula
class age(AlternativeFormulaColumn):
    column = AgeCol(val_type = "age")
    entity_class = Individus
    label = u"Âge (en années)"

    @alternative_function()
    def age_from_birth(self, birth, period):
        return (datetime64(period.date) - birth).astype('timedelta64[Y]')

    @alternative_function()
    def age_from_agem(self, agem):
        return agem // 12

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class agem(AlternativeFormulaColumn):
    column = AgeCol(val_type = "months")
    entity_class = Individus
    label = u"Âge (en mois)"

    @alternative_function()
    def agem_from_birth(self, birth, period):
        return (datetime64(period.date) - birth).astype('timedelta64[M]')

    @alternative_function()
    def agem_from_age(self, age):
        return age * 12

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


def _nb_adult(marie, celdiv, veuf):
    return 2 * marie + 1 * (celdiv | veuf)


@reference_formula
class marie(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"marie"

    def function(self, statmarit):
        '''
        Marié (1)
        'foy'
        '''
        return (statmarit == 1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class celdiv(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"celdiv"

    def function(self, statmarit):
        '''
        Célibataire
        'foy'
        '''
        return (statmarit == 2)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class divor(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"divor"

    def function(self, statmarit):
        '''
        Divorcé (3)
        'foy'
        '''
        return (statmarit == 3)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class veuf(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"veuf"

    def function(self, statmarit):
        '''
        Veuf (4)
        'foy'
        '''
        return statmarit == 4

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class nb_enf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_enf"

    def function(self, age_holder, _P):
        '''
        Nombre d'enfants TODO
        '''
        age = self.split_by_roles(age_holder, roles = PACS)

        P = _P.ir.deduc.fam
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
        return res

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class nb_enf_sup(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_enf_sup"

    def function(self, agem, boursier):
        '''
        Nombre d'enfants étudiant du supérieur non boursiers TODO
        '''
        return 0 * agem

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class nb_infirme(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_infirme"

    def function(self, agem, inv):
        '''
        Nombre d'enfants infirmes TODO
        '''
        return 0 * agem

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class nb_par(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_par"

    def function(self, agem_holder):
        '''
        Nombre de parents TODO
        '''
        agem_vous = self.filter_role(agem_holder, role = VOUS)
        agem_conj = self.filter_role(agem_holder, role = CONJ)
        return (agem_vous > 10 * 12) + (agem_conj > 10 * 12)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


###############################################################################
# # Revenus catégoriels
###############################################################################


# 1. Bénéfices industriels et commerciaux
@reference_formula
class bic(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bic"

    def function(self, bic_reel_res):
        '''
        Bénéfices industriels et commerciaux TODO:
        'foy'
        '''
    #    return bic_reel + bic_simpl + bic_forf TODO:
        return bic_reel_res

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# régime réel
# régime réel simplifié
# régime forfaitaire


@reference_formula
class bic_ca_global(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Chiffre d’affaires global (BIC, cession de fond de commerce"

    def function(self, bic_ca_revente, bic_ca_autre):
        """
        Chiffre d’affaires global
        des personnes soumises au régime forfaitaire ayant cédé le fond de commerce
        """
        return bic_ca_revente + bic_ca_autre

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class bic_res_cession(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Résultat (BIC, cession de fond de commerce)"

    def function(self, bic_ca_global, bic_depenses):
        return max_(bic_ca_global - bic_depenses, 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class bic_benef_fiscal_cession(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Bénéfice fiscal (BIC, cession de fond de commerce)"

    def function(self, bic_res_cession, bic_pv_cession):
        """
        Bénéfice fiscal
        """
        return bic_res_cession + bic_pv_cession

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


def _bic_res_net(bic_benef_fiscal_cession, bic_part_benef_sp):
    """
    Résultat net BIC TODO: il manque le régime réel
    """
    return bic_benef_fiscal_cession + bic_part_benef_sp


# 2. Bénéfices des professions non commerciales
@reference_formula
class bnc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bnc"

    def function(self, bnc_reel_res_fiscal, bnc_forf_benef_fiscal, bnc_part_benef_sp):
        '''
        Bénéfices des professions non commerciales TODO:
        'foy'
        '''
        return bnc_reel_res_fiscal + bnc_forf_benef_fiscal + bnc_part_benef_sp

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class bnc_forf_benef_fiscal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)"

    def function(self, bnc_forf_rec_brut, _P):
        """
        Bénéfice fiscal (régime forfaitaire, 70% des recettes brutes TTC)
        """
        part = _P.ir.bnc.forf.part_forf
        return bnc_forf_rec_brut * part

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# 3. Bénéfices de l'exploitation agricole et de pêche
@reference_formula
class beap(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"beap"

    def function(self, beap_reel_res_fiscal, beap_reliq_benef_fiscal, beap_monogr, beap_part_benef_sp):
        """
        Bénéfices de l'exploitation agricole et de pêche TODO:
        'foy'
        """
        return beap_reel_res_fiscal + beap_reliq_benef_fiscal + beap_monogr + beap_part_benef_sp

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# 4. Revenus fonciers
@reference_formula
class rfon(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rfon"

    def function(self, fon_reel_fisc_holder, fon_forf_bati, fon_forf_nbat, fon_sp_holder):
        """
        Revenus fonciers
        'foy'
        """
        fon_reel_fisc = self.filter_role(fon_reel_fisc_holder, role = VOUS)
        fon_sp = self.filter_role(fon_sp_holder, role = VOUS)
        return fon_reel_fisc + fon_forf_bati + fon_forf_nbat + fon_sp

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class fon_forf_bati(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"fon_forf_bati"

    def function(self, fon_forf_bati_rec_holder, fon_forf_bati_rel_holder, fon_forf_bati_fra_holder, fon_forf_bati_tax_holder, _P):
        '''
        Revenus fonciers net des immeubles bâtis
        'foy'
        '''
        P = _P.ir.fon.bati.deduc_frais
        fon_forf_bati_rec = self.filter_role(fon_forf_bati_rec_holder, role = VOUS)
        fon_forf_bati_rel = self.filter_role(fon_forf_bati_rel_holder, role = VOUS)
        fon_forf_bati_fra = self.filter_role(fon_forf_bati_fra_holder, role = VOUS)
        fon_forf_bati_tax = self.filter_role(fon_forf_bati_tax_holder, role = VOUS)
        return max_(0, fon_forf_bati_rec * (1 - P) + fon_forf_bati_rel - fon_forf_bati_fra - fon_forf_bati_tax)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class fon_forf_nbat(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"fon_forf_nbat"

    def function(self, fon_forf_nbat_rec_holder, fon_forf_nbat_dep_holder, fon_forf_nbat_tax_holder, _P):
        '''
        Revenus fonciers net des terrains non bâtis
        'foy'
        '''
        fon_forf_nbat_rec = self.filter_role(fon_forf_nbat_rec_holder, role = VOUS)
        fon_forf_nbat_dep = self.filter_role(fon_forf_nbat_dep_holder, role = VOUS)
        fon_forf_nbat_tax = self.filter_role(fon_forf_nbat_tax_holder, role = VOUS)
        return max_(0, fon_forf_nbat_rec - fon_forf_nbat_dep - fon_forf_nbat_tax)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# 5. Traitements, salaires, indemnités, pensions et rentes viagères
@reference_formula
class tspr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"tspr"

    def function(self, sal_net, pen_net):
        '''
        Traitements, salaires, indemnités, pensions et rentes viagères
        'foy'
        '''
        return sal_net + pen_net

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class sal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Salaires y compris salaires en nature"

    def function(self, sali_holder, sal_nat_holder):
        '''
        Salaires y compris salaires en nature
        'foy'
        '''
        sali = self.sum_by_entity(sali_holder, roles = [VOUS, CONJ])
        sal_nat = self.sum_by_entity(sal_nat_holder, roles = [VOUS, CONJ])
        return (sali + sal_nat)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class smig(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires"

    def function(self, sal, smig_dec_holder, _P):
        '''
        Indicatrice de salariée payé au smig
        'foy'
        '''
        # TODO: should be better implemented
        smig_dec = self.filter_role(smig_dec_holder, role = VOUS)
        smig = or_(smig_dec, sal <= 12 * _P.cotsoc.gen.smig)
        return smig

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class sal_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Salaires nets"

    def function(self, period, sal, smig, tspr = law.ir.tspr):
        '''
        Revenu imposé comme des salaires net des abatements
        'foy'
        '''
        if period.start.year >= 2011:
            res = max_(sal * (1 - tspr.abat_sal) - max_(smig * tspr.smig, (sal <= tspr.smig_ext) * tspr.smig), 0)
        else:
            res = max_(sal * (1 - tspr.abat_sal) - smig * tspr.smig, 0)
        return res

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class pen_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"pen_net"

    def function(self, pen_holder, pen_nat_holder, _P):
        '''
        Pensions et rentes viagères après abattements
        'foy'
        '''
        P = _P.ir.tspr
        pen = self.filter_role(pen_holder, role = VOUS)
        pen_nat = self.filter_role(pen_nat_holder, role = VOUS)
        return (pen + pen_nat) * (1 - P.abat_pen)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# 6. Revenus de valeurs mobilières et de capitaux mobiliers
@reference_formula
class rvcm(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rvcm"

    def function(self, capm_banq_holder, capm_cent_holder, capm_caut_holder, capm_part_holder, capm_oblig_holder, capm_caisse_holder, capm_plfcc_holder, capm_epinv_holder, capm_aut_holder):
        '''
        Revenus de valeurs mobilières et de capitaux mobiliers
        'foy'
        '''
        capm_banq = self.filter_role(capm_banq_holder, role = VOUS)
        capm_cent = self.filter_role(capm_cent_holder, role = VOUS)
        capm_caut = self.filter_role(capm_caut_holder, role = VOUS)
        capm_part = self.filter_role(capm_part_holder, role = VOUS)
        capm_oblig = self.filter_role(capm_oblig_holder, role = VOUS)
        capm_caisse = self.filter_role(capm_caisse_holder, role = VOUS)
        capm_plfcc = self.filter_role(capm_plfcc_holder, role = VOUS)
        capm_epinv = self.filter_role(capm_epinv_holder, role = VOUS)
        capm_aut = self.filter_role(capm_aut_holder, role = VOUS)

        return capm_banq + capm_cent + capm_caut + capm_part + capm_oblig + capm_caisse + capm_plfcc + capm_epinv + capm_aut

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


# 7. revenus de source étrangère
@reference_formula
class retr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"retr"

    def function(self, etr_sal_holder, etr_pen_holder, etr_trans_holder, etr_aut_holder, _P):
        '''
        Autres revenus ie revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine
        'foy'
        '''
        P = _P.ir.tspr
        etr_sal = self.filter_role(etr_sal_holder, role = VOUS)
        etr_pen = self.filter_role(etr_pen_holder, role = VOUS)
        etr_trans = self.filter_role(etr_trans_holder, role = VOUS)
        etr_aut = self.filter_role(etr_aut_holder, role = VOUS)
        return etr_sal * (1 - P.abat_sal) + etr_pen * (1 - P.abat_pen) + etr_trans * (1 - P.abat_pen_etr) + etr_aut

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


@reference_formula
class rng(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu net global"

    def function(self, tspr, rfon, retr, rvcm):
        '''
        Revenu net global  soumis à l'impôt après déduction des abattements
        'foy'
        '''
        return tspr + rfon + +rvcm + retr

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


#############################
#    Déductions
#############################

# # 1/ Au titre des revenus et bénéfices provenant de l’activité

# # 2/ Autres déductions


def _deduc_int(capm_banq, capm_cent, capm_oblig, _P):
    P = _P.deduc
    return max_(
        max_(
            max_(capm_banq, P.banq.plaf) + max_(capm_cent, P.cent.plaf),
            P.banq.plaf
            ) +
        max_(capm_oblig, P.oblig.plaf), P.oblig.plaf
        )


@reference_formula
class deduc_fam(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déductions pour situation et charges de famille"

    def function(self, rng, chef, nb_enf, nb_par, _P):
        '''
        Déductions pour situation et charges de famille
        'foy'
        '''
        P = _P.ir.deduc.fam
        #  chef de famille
        chef = P.chef * (nb_enf > 0)  # TODO

    #    from scipy.stats import rankdata
    #
    #    ages = [a in age.values() if a >= 0 ]
    #    rk = rankdata(age.values())
    #    TODO
    #    rk = rk[-4:]
    #    rk = round(rk + -.01*range(len(rk))) # to properly rank twins
    #
    #
        enf = (nb_enf >= 1) * P.enf1 + (nb_enf >= 2) * P.enf2 + (nb_enf >= 3) * P.enf3 + (nb_enf >= 4) * P.enf4
    #    sup = P.enf_sup*nb_enf_sup
    #    infirme = P.infirme*nb_infirme
    #    parent = min_(P.parent_taux*rng, P.parent_max)

    #    return chef + enf + sup + infirme + parent
        res = chef + enf
        return res

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class deduc_rente(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Arrérages et rentes payées à titre obligatoire et gratuit"

    def function(self, rente):
        '''
        Déductions des arrérages et rentes payées à titre obligatoire et gratuit
        'foy'
        '''
        return rente  # TODO:

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class ass_vie(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Primes afférentes aux contrats d'assurance-vie"

    def function(self, prime_ass_vie_holder, statmarit_holder, nb_enf, _P):
        '''
        Primes afférentes aux contrats d'assurance-vie collectifs ou individuels
        'foy'
        '''
        P = _P.ir.deduc.ass_vie
        marie = self.filter_role(statmarit_holder, role = VOUS)  # TODO
        prime_ass_vie = self.sum_by_entity(prime_ass_vie_holder)
        deduc = min_(prime_ass_vie, P.plaf + marie * P.conj_plaf + nb_enf * P.enf_plaf)
        return deduc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


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


@reference_formula
class deduc_smig(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG"

    def function(self, chef):
        '''
        Déduction supplémentaire pour les salariés payés au « SMIG » et « SMAG »
        'foy'
        '''
        return 0 * chef  # TODO: voir avec tspr

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class rni(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu net imposable"

    def function(self, rng, deduc_fam, rente_holder, ass_vie):
        '''
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses et charges professionnelles
        et des revenus non soumis à l'impôt
        'foy'
        '''
        rente = self.filter_role(rente_holder, role = VOUS)
        return rng - (deduc_fam + rente + ass_vie)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class ir_brut(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt avant non-imposabilité"

    def function(self, rni, _P):
        '''
        Impot sur le revenu avant non imposabilité
        'foy'
        '''
        bar = _P.ir.bareme
        exemption = _P.ir.reforme.exemption
        rni_apres_exemption = rni * (exemption.active == 0) + rni * (exemption.active == 1) * (rni > exemption.max)
        ir_brut = -bar.calc(rni_apres_exemption)
        return ir_brut

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class irpp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu des personnes physiques"

    def function(self, ir_brut, _P):
        '''
        Impot sur le revenu payé TODO:
        'foy'
        '''
        irpp = ir_brut
        return irpp

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
