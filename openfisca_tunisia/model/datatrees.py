# -*- coding: utf-8 -*-


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
                    u"""invalide""",
                    u"""jour_xyz""",
                    u"""boursier""",
                    u"""chef_de_famille""",
                    u"""bic_reel""",
                    u"""bic_societes_personnes""",
                    u"""cadre_legal""",
                    u"""bic_reel_res""",
                    u"""bic_forfaitaire_resultat""",
                    u"""bic_societes_personnes_resultat""",
                    u"""structure_declaration_investissement""",
                    u"""bic_res_fiscal""",
                    u"""bic_ca_revente""",
                    u"""bic_ca_autre""",
                    u"""bic_depenses""",
                    u"""bic_pv_cession""",
                    u"""bic_part_benef_sp""",
                    u"""bnc_reel_res_fiscal""",
                    u"""bnc_forfaitaire_recettes_brutes""",
                    u"""bnc_part_benef_sp""",
                    u"""beap_reel_res_fiscal""",
                    u"""beap_reliq_rec""",
                    u"""beap_reliq_stock""",  # Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)
                    u"""beap_reliq_dep_ex""",
                    u"""beap_reliq_benef_fiscal""",
                    u"""beap_monogr""",
                    u"""beap_part_benef_sp""",
                    u"""foncier_reel_resultat_fiscal""",
                    u"""foncier_forfaitaire_batis_recettes""",
                    u"""foncier_forfaitaire_batis_reliquat""",
                    u"""foncier_forfaitaire_batis_frais""",
                    u"""foncier_forfaitaire_batis_taxe""",
                    u"""foncier_forfaitaire_non_batis_recettes""",
                    u"""foncier_forfaitaire_non_batis_depenses""",
                    u"""foncier_forfaitaire_non_batis_taxe""",
                    u"""foncier_societes_personnes""",
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
                    u"""prime_assurance_vie""",
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
