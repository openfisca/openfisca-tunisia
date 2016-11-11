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
                    'date_naissance',  # Année de naissance
                    'statut_marital',
                    'salaire_imposable',
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
                    u"""nom_individu""",
                    u"""categorie_salarie""",
                    u"""inv""",
                    u"""jour_xyz""",
                    u"""boursier""",
                    u"""chef""",
                    u"""bic_reel""",
                    u"""bic_sp""",
                    u"""cadre_legal""",
                    u"""bic_reel_res""",
                    u"""bic_forf_res""",
                    u"""bic_sp_res""",
                    u"""decl_inves""",
                    u"""bic_res_fiscal""",
                    u"""bic_ca_revente""",
                    u"""bic_ca_autre""",
                    u"""bic_depenses""",
                    u"""bic_pv_cession""",
                    u"""bic_part_benef_sp""",
                    u"""bnc_reel_res_fiscal""",
                    u"""bnc_forf_rec_brut""",
                    u"""bnc_part_benef_sp""",
                    u"""beap_reel_res_fiscal""",
                    u"""beap_reliq_rec""",
                    u"""beap_reliq_stock""",  # Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)
                    u"""beap_reliq_dep_ex""",
                    u"""beap_reliq_benef_fiscal""",
                    u"""beap_monogr""",
                    u"""beap_part_benef_sp""",
                    u"""fon_reel_fisc""",
                    u"""fon_forf_bati_rec""",
                    u"""fon_forf_bati_rel""",
                    u"""fon_forf_bati_fra""",
                    u"""fon_forf_bati_tax""",
                    u"""fon_forf_nbat_rec""",
                    u"""fon_forf_nbat_dep""",
                    u"""fon_forf_nbat_tax""",
                    u"""fon_sp""",
                    u"""salaire_en_nature""",
                    u"""smig_dec""",
                    u"""pen""",
                    u"""avantages_nature_assimile_pension""",
                    u"""valm_nreg""",
                    u"""valm_jpres""",
                    u"""valm_aut""",
                    u"""capm_banq""",
                    u"""capm_cent""",
                    u"""capm_caut""",
                    u"""capm_part""",
                    u"""capm_oblig""",
                    u"""capm_caisse""",
                    u"""capm_plfcc""",
                    u"""capm_epinv""",
                    u"""capm_aut""",
                    u"""salaire_etranger""",
                    u"""pension_etranger_non_transferee""",
                    u"""pension_etranger_transferee""",
                    u"""autres_revenus_etranger""",
                    u"""deficits_anterieurs_non_deduits""",
                    u"""deduc_banq""",
                    u"""deduc_cent""",
                    u"""deduc_obli""",
                    u"""deduc_epinv""",
                    u"""rente""",
                    u"""prime_ass_vie""",
                    u"""dons""",
                    u"""pret_univ""",
                    u"""cotis_nonaf""",
                    u"""deduc_logt""",
                    u"""rstbrut""",
                    u"""alv""",
                    u"""rto""",
                    u"""prestations_sociales""",
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
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""nom_menage""",
                    u"""so""",
                    ]),
                ]),
            ]),
        ])),
    ])
