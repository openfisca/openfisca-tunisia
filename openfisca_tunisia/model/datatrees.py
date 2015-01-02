# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


import collections


columns_name_tree_by_entity = collections.OrderedDict([
    ('ind', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'birth',  # Année de naissance
                    'statmarit',
                    'sali',  # Salaires imposables
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi et rentes"""),
                ('children', [
                    'activite',
                    'alr',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""type_sal""",
                    u"""inv""",  # invalide
                    u"""jour_xyz""",
                    u"""boursier""",
                    u"""so""",
                    u"""chef""",
                    u"""bic_reel""",
                    u"""bic_sp""",
                    u"""cadre_legal""",
                    u"""bic_reel_res""",
                    u"""bic_forf_res""",
                    u"""bic_sp_res""",
                    u"""decl_inves""",
                    u"""bic_res_fiscal""",  # Résultat fiscal (BIC)
                    u"""bic_ca_revente""",  # Chiffre d’affaires global au titre des activités d’achat en vue de la revente et les activités de transformation
                    u"""bic_ca_autre""",  # Chiffre d’affaires global au titre d’autres activités
                    u"""bic_depenses""",  # Total des dépenses (BIC cession de fond de commerce)
                    u"""bic_pv_cession""",  # Plue-value de cession du fond de commerce
                    u"""bic_part_benef_sp""",  # Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur industriel et commercial
                    u"""bnc_reel_res_fiscal""",  # Résultat fiscal (BNC)
                    u"""bnc_forf_rec_brut""",  # Recettes globales brutes TTC (BNC)
                    u"""bnc_part_benef_sp""",  # Part dans le bénéfice ou dans la perte des sociétés de personnes qui réalisent des bénéfices non commerciaux
                    u"""beap_reel_res_fiscal""",  # Résultat fiscal (BEAP, régime réel)
                    u"""beap_reliq_rec""",  # Recettes (BEAP, bénéfice comme reliquat entre recette et dépenses
                    u"""beap_reliq_stock""",  # Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)
                    u"""beap_reliq_dep_ex""",  # Dépenses d’exploitation (BEAP, bénéfice comme reliquat entre recette et dépenses)
                    u"""beap_reliq_benef_fiscal""",  # Bénéfice fiscal (BEAP)
                    u"""beap_monogr""",  # Détermination du bénéfice sur la base de monographies sectorielles (BEAP)
                    u"""beap_part_benef_sp""",  # Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur agricole et de pêche
                    u"""fon_reel_fisc""",
                    u"""fon_forf_bati_rec""",
                    u"""fon_forf_bati_rel""",
                    u"""fon_forf_bati_fra""",
                    u"""fon_forf_bati_tax""",
                    u"""fon_forf_nbat_rec""",
                    u"""fon_forf_nbat_dep""",
                    u"""fon_forf_nbat_tax""",
                    u"""fon_sp""",
                    u"""sal_nat""",  # Avantages en nature assimilables à des salaires
                    u"""smig_dec""",  # Salarié déclarant percevoir le SMIG ou le SMAG
                    u"""pen""",  # Pensions et rentes viagères
                    u"""pen_nat""",  # Avantages en nature assimilables à des pensions
                    u"""valm_nreg""",  # Revenus des valeurs mobilières autres que ceux régulièrement distribués
                    u"""valm_jpres""",  # Jetons de présence
                    u"""valm_aut""",  # Autres rémunérations assimilées
                    u"""capm_banq""",  # Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques
                    u"""capm_cent""",  # Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT
                    u"""capm_caut""",  # Intérêts des créances et intérêts et rémunérations des cautionnements
                    u"""capm_part""",  # Intérêts des titres de participation
                    u"""capm_oblig""",  # Intérêts des emprunts obligataires
                    u"""capm_caisse""",  # Intérêts des bons de caisse
                    u"""capm_plfcc""",  # Revenus des parts et de liquidation du fonds commun des créances
                    u"""capm_epinv""",  # Intérêts des comptes épargne pour l'investissement
                    u"""capm_aut""",  # Autres intérêts
                    u"""etr_sal""",  # Salaires perçus à l'étranger
                    u"""etr_pen""",  # Pensions perçues à l'étranger (non transférées)
                    u"""etr_trans""",  # Pensions perçues à l'étranger (transférées en Tunisie)
                    u"""etr_aut""",  # Autres revenus perçus à l'étranger
                    u"""def_ante""",  # Déficits des années antérieures non déduits
                    u"""deduc_banq""",  # Intérêts des comptes spéciaux d’épargne ouverts auprès des banques
                    u"""deduc_cent""",  # Intérêts des comptes spéciaux d’épargne ouverts auprès de la CENT dans la limite
                    u"""deduc_obli""",  # Intérêts des emprunts obligataires
                    u"""deduc_epinv""",  # Intérêts des comptes épargne pour l'investissement
                    u"""rente""",  # Rentes payées obligatoirement et à titre gratuit
                    u"""prime_ass_vie""",  # Prime d’assurance-vie
                    u"""dons""",  # Dons au profit du fonds national de solidarité 26-26 et du Fonds National de l’Emploi 21-21
                    u"""pret_univ""",  # Remboursement des prêts universitaires en principal et intérêts
                    u"""cotis_nonaf""",  # Les cotisations payées par les travailleurs non salariés affiliés à l’un des régimes légaux de la sécurité sociale
                    u"""deduc_logt""",  # Les intérêts payés au titre des prêts relatifs à l’acquisition ou à la construction d’un logement social
                    u"""rstbrut""",
                    u"""alv""",
                    u"""rto""",
                    u"""psoc""",
                    u"""af""",
                    u"""uc""",
                    ]),
                ]),
            ]),
        ])),
    ('men', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'loyer',
                    'code_postal',
                    ]),
                ]),
            ]),
        ])),
    ])
